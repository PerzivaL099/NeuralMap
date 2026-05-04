from fastapi import APIRouter, HTTPException, Query
from app.models.schemas import NodeCreate, NodeUpdate, NodeResponse
from app.repositories.node_repo import node_repo

router = APIRouter()


@router.post("/", response_model=NodeResponse, status_code=201)
async def create_node(data: NodeCreate):
    return await node_repo.create(data)


@router.get("/", response_model=list[NodeResponse])
async def list_nodes(
    skip:  int = Query(default=0,   ge=0),
    limit: int = Query(default=100, le=500),
):
    return await node_repo.list_all(skip=skip, limit=limit)


@router.get("/{node_id}", response_model=NodeResponse)
async def get_node(node_id: str):
    node = await node_repo.get_by_id(node_id)
    if not node:
        raise HTTPException(status_code=404, detail=f"Node '{node_id}' not found.")
    return node


@router.patch("/{node_id}", response_model=NodeResponse)
async def update_node(node_id: str, data: NodeUpdate):
    node = await node_repo.update(node_id, data)
    if not node:
        raise HTTPException(status_code=404, detail=f"Node '{node_id}' not found.")
    return node


@router.delete("/{node_id}", status_code=204)
async def delete_node(node_id: str):
    deleted = await node_repo.delete(node_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Node '{node_id}' not found.")
