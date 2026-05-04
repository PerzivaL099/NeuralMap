import uuid
from datetime import datetime, timezone
from typing import Optional

from app.db.neo4j import neo4j_driver
from app.models.schemas import EdgeCreate, EdgeResponse


def _row_to_edge(row: dict) -> EdgeResponse:
    r = row["r"]
    return EdgeResponse(
        id=r["id"],
        source_id=row["source_id"],
        target_id=row["target_id"],
        label=r.get("label"),
        weight=r.get("weight", 1.0),
        kind=r.get("kind", "manual"),
        created_at=r["created_at"].to_native(),
    )


class EdgeRepository:

    async def create(self, data: EdgeCreate) -> EdgeResponse:
        now = datetime.now(timezone.utc)
        edge_id = str(uuid.uuid4())
        cypher = """
        MATCH (a:Node {id: $source_id}), (b:Node {id: $target_id})
        CREATE (a)-[r:RELATES_TO {
            id:         $id,
            label:      $label,
            weight:     $weight,
            kind:       $kind,
            created_at: $now
        }]->(b)
        RETURN r, a.id AS source_id, b.id AS target_id
        """
        params = {
            "id":        edge_id,
            "source_id": data.source_id,
            "target_id": data.target_id,
            "label":     data.label,
            "weight":    data.weight,
            "kind":      data.kind,
            "now":       now,
        }
        async with neo4j_driver.get_session() as session:
            result = await session.run(cypher, params)
            record = await result.single()
        if not record:
            raise ValueError(
                f"Could not create edge: one or both nodes not found "
                f"(source={data.source_id}, target={data.target_id})"
            )
        return _row_to_edge(dict(record))

    async def get_by_id(self, edge_id: str) -> Optional[EdgeResponse]:
        cypher = """
        MATCH (a)-[r:RELATES_TO {id: $id}]->(b)
        RETURN r, a.id AS source_id, b.id AS target_id
        """
        async with neo4j_driver.get_session() as session:
            result = await session.run(cypher, {"id": edge_id})
            record = await result.single()
        if not record:
            return None
        return _row_to_edge(dict(record))

    async def list_for_node(self, node_id: str) -> list[EdgeResponse]:
        """Return all edges where the given node is source or target."""
        cypher = """
        MATCH (a:Node {id: $node_id})-[r:RELATES_TO]->(b)
        RETURN r, a.id AS source_id, b.id AS target_id
        UNION
        MATCH (a)-[r:RELATES_TO]->(b:Node {id: $node_id})
        RETURN r, a.id AS source_id, b.id AS target_id
        """
        async with neo4j_driver.get_session() as session:
            result = await session.run(cypher, {"node_id": node_id})
            records = await result.data()
        return [_row_to_edge(r) for r in records]

    async def delete(self, edge_id: str) -> bool:
        cypher = """
        MATCH ()-[r:RELATES_TO {id: $id}]->()
        DELETE r
        RETURN count(r) AS deleted
        """
        async with neo4j_driver.get_session() as session:
            result = await session.run(cypher, {"id": edge_id})
            record = await result.single()
        return record["deleted"] > 0

    async def get_edges_for_nodes(self, node_ids: list[str]) -> list[EdgeResponse]:
        """Fetch all edges between a specific set of node ids (for viewport graph query)."""
        cypher = """
        MATCH (a:Node)-[r:RELATES_TO]->(b:Node)
        WHERE a.id IN $ids AND b.id IN $ids
        RETURN r, a.id AS source_id, b.id AS target_id
        """
        async with neo4j_driver.get_session() as session:
            result = await session.run(cypher, {"ids": node_ids})
            records = await result.data()
        return [_row_to_edge(r) for r in records]


edge_repo = EdgeRepository()
