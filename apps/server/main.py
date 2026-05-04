from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.db.neo4j import neo4j_driver
from app.api.routes import nodes, edges, graph


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: verify Neo4j connection & apply schema constraints
    await neo4j_driver.connect()
    await neo4j_driver.apply_schema()
    yield
    # Shutdown: close Neo4j driver
    await neo4j_driver.close()


app = FastAPI(
    title="NeuralMap API",
    description="Graph-based second brain — nodes, edges, and AI-powered connections.",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:1420"],  # Tauri dev port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(nodes.router, prefix="/api/nodes",  tags=["Nodes"])
app.include_router(edges.router, prefix="/api/edges",  tags=["Edges"])
app.include_router(graph.router, prefix="/api/graph",  tags=["Graph"])


@app.get("/health")
async def health():
    return {"status": "ok"}
