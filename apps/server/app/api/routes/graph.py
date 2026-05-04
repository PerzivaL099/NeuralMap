from fastapi import APIRouter
from app.models.schemas import ViewportQuery, GraphResponse
from app.repositories.node_repo import node_repo
from app.repositories.edge_repo import edge_repo

router = APIRouter()


@router.post("/viewport", response_model=GraphResponse)
async def get_graph_in_viewport(query: ViewportQuery):
    """
    Returns all nodes visible inside a canvas bounding box,
    plus all edges that connect two nodes within that viewport.

    This is the primary query called by the canvas renderer on every
    camera move — keep it fast. Future: replace the Neo4j WHERE filter
    with a Quadtree spatial index for sub-10ms responses at scale.
    """
    nodes = await node_repo.get_in_viewport(
        x_min=query.x_min,
        y_min=query.y_min,
        x_max=query.x_max,
        y_max=query.y_max,
        limit=query.limit,
    )
    node_ids = [n.id for n in nodes]
    edges = await edge_repo.get_edges_for_nodes(node_ids) if node_ids else []
    return GraphResponse(nodes=nodes, edges=edges)
