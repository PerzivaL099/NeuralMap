@"
# NeuralMap

> A graph-based second brain — store, map, and discover hidden connections between your knowledge.

NeuralMap treats **relationships as first-class citizens**. Unlike linear note-taking apps, it uses a graph database and NLP embeddings to reveal connections between isolated pieces of knowledge — rendered on an infinite, zoomable canvas.

---

## Current Status

| Layer | Status | Details |
|-------|--------|---------|
| Infrastructure | ✅ Running | Neo4j, MinIO, PostgreSQL, Redis, Activepieces via Docker |
| Backend API | ✅ Working | FastAPI + Neo4j, nodes/edges CRUD, viewport query |
| Frontend Canvas | 🚧 In Progress | React + Vite, pan/zoom/drag, node cards, edge rendering |
| Auth | ⬜ Pending | GitHub OAuth + JWT |
| AI Pipeline | ⬜ Pending | Embeddings + HITL suggestions |
| Tauri Wrapper | ⬜ Pending | Desktop app packaging |

---

## Tech Stack

**Architecture:** Decoupled Monorepo (Clean Architecture)

| Layer | Technology |
|-------|-----------|
| Frontend | React + TypeScript + Vite |
| Desktop Wrapper | Tauri (Rust) |
| Canvas Rendering | HTML5 Canvas + SVG (PixiJS planned) |
| State Management | Zustand |
| Backend API | FastAPI (Python) |
| Graph Database | Neo4j 5 Community + APOC |
| Object Storage | MinIO (S3-compatible) |
| Automation | Activepieces (self-hosted) |
| Automation DB | PostgreSQL 15 + pgvector |
| Message Broker | Redis 7 |

---

## Repository Structure


NeuralMap/
├── apps/
│   ├── desktop/              # React + Vite frontend
│   │   └── src/
│   │       ├── components/   # Canvas, NodeCard, EdgeLayer, CreateNodePanel
│   │       ├── store/        # Zustand canvas store
│   │       ├── api/          # Axios client for FastAPI
│   │       └── styles/       # Global CSS design system
│   └── server/               # FastAPI backend
│       └── app/
│           ├── api/routes/   # nodes.py, edges.py, graph.py
│           ├── db/           # Neo4j async driver + schema bootstrap
│           ├── models/       # Pydantic schemas
│           └── repositories/ # Cypher queries (node_repo, edge_repo)
├── infra/
│   └── docker-compose.yml    # All infrastructure containers
├── .env.example              # Secrets template (copy to .env)
├── PROGRESS.md               # Session-by-session dev log
└── README.md

---

## Getting Started

### 1. Prerequisites
- Docker Desktop with WSL2 integration
- Python 3.13+
- Node.js 20+

### 2. Infrastructure
``````bash
docker compose -f infra/docker-compose.yml up -d
``````

### 3. Backend
``````bash
cd apps/server
cp .env.example .env        # Fill in your credentials
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
``````

API docs available at: http://127.0.0.1:8000/docs

### 4. Frontend
``````bash
cd apps/desktop
npm install
npm run dev
``````

Canvas available at: http://localhost:5173

---

## Core Features

### Infinite Canvas
- Pan (click + drag), zoom (scroll wheel, zooms toward cursor)
- Double-click anywhere to create a new node
- Drag nodes to reposition — position persisted to Neo4j automatically

### Node Types
| Type | Icon | Use |
|------|------|-----|
| note | ◈ | Text notes and ideas |
| code | ⟨/⟩ | Code snippets |
| image | ⬡ | Images and visuals |
| file | ▤ | Documents and files |
| journal | ◎ | Journal entries |
| url | ⬗ | Web links |

### Graph API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/nodes/ | Create a node |
| GET | /api/nodes/ | List all nodes |
| PATCH | /api/nodes/{id} | Update a node |
| DELETE | /api/nodes/{id} | Delete a node |
| POST | /api/edges/ | Create an edge |
| POST | /api/graph/viewport | Spatial query by bounding box |

---

## Roadmap

- [ ] Fix frontend dev server (backtick issue in client.ts)
- [ ] Full canvas flow: create → display → connect nodes
- [ ] GitHub OAuth + JWT middleware
- [ ] Edge creation UI (click source → click target)
- [ ] AI embeddings pipeline (sentence-transformers)
- [ ] Semantic zoom LOD (macro/mid/micro levels)
- [ ] Quadtree spatial index for viewport queries at scale
- [ ] Activepieces ingestion pipelines
- [ ] Tauri desktop wrapper
- [ ] RAG: chat with your brain

---

## Design Patterns

- **Repository Pattern** — All Cypher queries isolated in repo layer, zero SQL/Cypher in routes
- **Proxy Pattern** — Nodes lazy-load rich content only when interacted with
- **Observer Pattern** — Camera zoom state triggers LOD transitions
- **Strategy Pattern** — LocalAnalysisStrategy vs CloudAnalysisStrategy based on user tier
- **HITL Loop** — AI suggestions staged as pending, written to Neo4j only on approval

---

## Infrastructure Ports

| Service | Port | UI |
|---------|------|----|
| FastAPI | 8000 | http://localhost:8000/docs |
| Neo4j Browser | 7474 | http://localhost:7474 |
| MinIO Console | 9001 | http://localhost:9001 |
| Activepieces | 8081 | http://localhost:8081 |
| Redis | 6379 | — |
"@ | Set-Content "C:\Users\mario\OneDrive\Desktop\Codigos\NeuralMap\README.md"

Write-Host "README.md updated!" -ForegroundColor Green
``````

Luego haz commit:

```powershell
cd C:\Users\mario\OneDrive\Desktop\Codigos\NeuralMap
git add README.md
git commit -m "docs: update README with current stack, structure, and roadmap"
git push
```