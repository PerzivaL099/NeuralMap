from pydantic import BaseModel, Field
from typing import Optional, Literal, Any
from datetime import datetime
import uuid


# ─── Node Models ──────────────────────────────────────────────────────────────

NodeType = Literal["note", "code", "image", "file", "journal", "url"]


class NodeCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=256)
    type: NodeType = "note"
    content: Optional[str] = None
    tags: list[str] = []
    # Spatial position on the infinite canvas
    x: float = 0.0
    y: float = 0.0
    # Optional: path to a MinIO object (images, PDFs, etc.)
    asset_key: Optional[str] = None


class NodeUpdate(BaseModel):
    title:     Optional[str]       = None
    content:   Optional[str]       = None
    tags:      Optional[list[str]] = None
    x:         Optional[float]     = None
    y:         Optional[float]     = None
    asset_key: Optional[str]       = None


class NodeResponse(BaseModel):
    id:         str
    title:      str
    type:       NodeType
    content:    Optional[str]
    tags:       list[str]
    x:          float
    y:          float
    asset_key:  Optional[str]
    created_at: datetime
    updated_at: datetime


# ─── Edge Models ──────────────────────────────────────────────────────────────

EdgeKind = Literal["manual", "ai_suggested", "approved"]


class EdgeCreate(BaseModel):
    source_id: str = Field(..., description="id of the source Node")
    target_id: str = Field(..., description="id of the target Node")
    label:     Optional[str] = None
    weight:    float = Field(default=1.0, ge=0.0, le=1.0,
                             description="AI similarity score, 1.0 for manual edges")
    kind:      EdgeKind = "manual"


class EdgeResponse(BaseModel):
    id:        str
    source_id: str
    target_id: str
    label:     Optional[str]
    weight:    float
    kind:      EdgeKind
    created_at: datetime


# ─── Graph Models (viewport fetch) ────────────────────────────────────────────

class ViewportQuery(BaseModel):
    x_min: float
    y_min: float
    x_max: float
    y_max: float
    limit: int = Field(default=200, le=1000)


class GraphResponse(BaseModel):
    nodes: list[NodeResponse]
    edges: list[EdgeResponse]
