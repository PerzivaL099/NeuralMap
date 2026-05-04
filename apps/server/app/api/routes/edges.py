from fastapi import APIRouter, HTTPException
from app.models.schemas import EdgeCreate, EdgeResponse
from app.repositories.edge_repo import edge_repo

router = APIRouter()


@router.post("/", response_model=EdgeResponse, status_code=201)
async def create_edge(data: EdgeCreate):
    try:
        return await edge_repo.create(data)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.get("/{edge_id}", response_model=EdgeResponse)
async def get_edge(edge_id: str):
    edge = await edge_repo.get_by_id(edge_id)
    if not edge:
        raise HTTPException(status_code=404, detail=f"Edge '{edge_id}' not found.")
    return edge


@router.get("/node/{node_id}", response_model=list[EdgeResponse])
async def list_edges_for_node(node_id: str):
    return await edge_repo.list_for_node(node_id)


@router.delete("/{edge_id}", status_code=204)
async def delete_edge(edge_id: str):
    deleted = await edge_repo.delete(edge_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Edge '{edge_id}' not found.")
