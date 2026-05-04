import uuid
from datetime import datetime, timezone
from typing import Optional

from app.db.neo4j import neo4j_driver
from app.models.schemas import NodeCreate, NodeUpdate, NodeResponse


def _row_to_node(row: dict) -> NodeResponse:
    n = row["n"]
    return NodeResponse(
        id=n["id"],
        title=n["title"],
        type=n["type"],
        content=n.get("content"),
        tags=list(n.get("tags", [])),
        x=n.get("x", 0.0),
        y=n.get("y", 0.0),
        asset_key=n.get("asset_key"),
        created_at=n["created_at"].to_native(),
        updated_at=n["updated_at"].to_native(),
    )


class NodeRepository:

    async def create(self, data: NodeCreate) -> NodeResponse:
        now = datetime.now(timezone.utc)
        node_id = str(uuid.uuid4())
        cypher = """
        CREATE (n:Node {
            id:         $id,
            title:      $title,
            type:       $type,
            content:    $content,
            tags:       $tags,
            x:          $x,
            y:          $y,
            asset_key:  $asset_key,
            created_at: $now,
            updated_at: $now
        })
        RETURN n
        """
        params = {
            "id":        node_id,
            "title":     data.title,
            "type":      data.type,
            "content":   data.content,
            "tags":      data.tags,
            "x":         data.x,
            "y":         data.y,
            "asset_key": data.asset_key,
            "now":       now,
        }
        async with neo4j_driver.get_session() as session:
            result = await session.run(cypher, params)
            record = await result.single()
        return _row_to_node(dict(record))

    async def get_by_id(self, node_id: str) -> Optional[NodeResponse]:
        cypher = "MATCH (n:Node {id: $id}) RETURN n"
        async with neo4j_driver.get_session() as session:
            result = await session.run(cypher, {"id": node_id})
            record = await result.single()
        if not record:
            return None
        return _row_to_node(dict(record))

    async def list_all(self, skip: int = 0, limit: int = 100) -> list[NodeResponse]:
        cypher = "MATCH (n:Node) RETURN n ORDER BY n.created_at DESC SKIP $skip LIMIT $limit"
        async with neo4j_driver.get_session() as session:
            result = await session.run(cypher, {"skip": skip, "limit": limit})
            records = await result.data()
        return [_row_to_node(r) for r in records]

    async def update(self, node_id: str, data: NodeUpdate) -> Optional[NodeResponse]:
        # Build SET clause only for provided fields
        updates = {k: v for k, v in data.model_dump().items() if v is not None}
        if not updates:
            return await self.get_by_id(node_id)

        set_clause = ", ".join(f"n.{k} = ${k}" for k in updates)
        cypher = f"""
        MATCH (n:Node {{id: $id}})
        SET {set_clause}, n.updated_at = $updated_at
        RETURN n
        """
        params = {"id": node_id, "updated_at": datetime.now(timezone.utc), **updates}
        async with neo4j_driver.get_session() as session:
            result = await session.run(cypher, params)
            record = await result.single()
        if not record:
            return None
        return _row_to_node(dict(record))

    async def delete(self, node_id: str) -> bool:
        """Delete node and all its relationships."""
        cypher = """
        MATCH (n:Node {id: $id})
        DETACH DELETE n
        RETURN count(n) AS deleted
        """
        async with neo4j_driver.get_session() as session:
            result = await session.run(cypher, {"id": node_id})
            record = await result.single()
        return record["deleted"] > 0

    async def get_in_viewport(
        self, x_min: float, y_min: float, x_max: float, y_max: float, limit: int = 200
    ) -> list[NodeResponse]:
        """Spatial query — returns nodes whose canvas position is inside the bounding box."""
        cypher = """
        MATCH (n:Node)
        WHERE n.x >= $x_min AND n.x <= $x_max
          AND n.y >= $y_min AND n.y <= $y_max
        RETURN n
        ORDER BY n.created_at DESC
        LIMIT $limit
        """
        params = {"x_min": x_min, "y_min": y_min, "x_max": x_max, "y_max": y_max, "limit": limit}
        async with neo4j_driver.get_session() as session:
            result = await session.run(cypher, params)
            records = await result.data()
        return [_row_to_node(r) for r in records]


node_repo = NodeRepository()
