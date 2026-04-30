================================================================================
PROJECT: NeuralMap - Master Context Document
================================================================================

1. PROJECT VISION
--------------------------------------------------------------------------------
NeuralMap is a multiplatform "second brain" and neural visualizer designed to store, map, and analyze diverse information types (text, notes, journal entries, code snippets, images, and files). 
Unlike linear note-taking apps, NeuralMap treats relationships (edges) as first-class citizens. It utilizes a graph-based structure and AI (NLP embeddings) to reveal hidden connections between isolated pieces of knowledge.

2. TECHNOLOGY STACK
--------------------------------------------------------------------------------
Architecture Pattern: Decoupled Monorepo (Clean Architecture)
Environment: WSL2 (Ubuntu) & Docker

- Frontend (Visualizer): React + TypeScript + Vite.
- Desktop Wrapper: Tauri (Rust-based, native OS webviews for high performance).
- Rendering Engine: Custom WebGL/Canvas (e.g., PixiJS) to handle Semantic Zoom and physics without DOM lag.
- Backend API: FastAPI (Python) - Handles CRUD, ML logic, and API routes.
- Graph Database: Neo4j - Stores nodes (metadata) and edges (relationships).
- Object Storage: MinIO (S3-compatible) - Stores heavy assets (images, markdown files, PDFs).
- Automation/Ingestion: Activepieces (Self-hosted via Docker) - Handles data pipelines and webhooks.

3. CORE MECHANICS & FEATURES
--------------------------------------------------------------------------------
A. Semantic Zoom (Spatial Rendering)
- The UI operates as an infinite canvas (World Space vs. Screen Space).
- Backend uses a Quadtree spatial index to serve only nodes visible in the current viewport bounding box.
- Level of Detail (LOD): Nodes visually transition based on camera Z-distance:
  - Macro: Tiny dots or basic labels.
  - Mid: Bounding boxes with titles and preview icons.
  - Micro: Full rich-text editors or expanded internal sub-graphs.

B. Dual-Mode Grouping & AI Integration
- Manual (Deterministic): Drag-and-drop nodes into parent container nodes. Updates DB instantly.
- Automated (Probabilistic): 
  - FastAPI passes node text through an NLP transformer (e.g., BERT/PyTorch) to generate dense vector embeddings.
  - Clustering algorithms (DBSCAN/K-Means) run periodically to find similarities.
  - HITL (Human-in-the-Loop): The system creates "Pending Connections" in an Inbox. AI suggestions are only written to Neo4j upon user approval.

C. Authentication & Security
- Third-Party OAuth: GitHub integration (ideal for developers).
- Stateless Auth: FastAPI issues a JWT upon successful OAuth callback. Frontend attaches JWT to the Authorization header.
- Multi-tenant Design: All nodes and files enforce strict `owner_id` policies.

4. AUTOMATION PIPELINE (ACTIVEPIECES)
--------------------------------------------------------------------------------
Activepieces acts as the nervous system, capturing external data and pushing it to the backend.
- Workflow: External Event (GitHub commit, web scraper) -> Activepieces formats data -> HTTP POST to FastAPI Ingestion Endpoint -> Embeddings Generated -> Saved to Neo4j.
- Communication between Activepieces and FastAPI is secured via an internal API Key/JWT.

5. DEPLOYMENT & SCALING STRATEGY (FREE VS PREMIUM)
--------------------------------------------------------------------------------
- Free/Local Tier: 
  - Storage: Local OS filesystem (managed by Tauri).
  - AI: Basic keyword tagging, localized small models.
  - Automation: Manual input only.
- Premium/Cloud Tier:
  - Storage: Cloud-hosted Neo4j and MinIO for cross-device syncing.
  - AI: Full semantic similarity matching, RAG (Retrieval-Augmented Generation) to "chat" with the brain.
  - Automation: Unlocked Activepieces background ingestion pipelines.

6. REPOSITORY STRUCTURE (MONOREPO)
--------------------------------------------------------------------------------
NeuralMap/
├── apps/
│   ├── desktop/          # Tauri + React/Vite (Frontend & Rendering)
│   └── server/           # FastAPI + PyTorch/NLP (Backend API)
├── infra/
│   ├── docker-compose.yml # Orchestration (Neo4j, MinIO, Activepieces)
│   └── neo4j/             # Database initialization scripts
├── packages/
│   └── shared-types/      # TS interfaces shared across frontend/backend
├── .env.example           # Secrets template
└── README.md              # Entry point documentation

7. DESIGN PATTERNS IN USE
--------------------------------------------------------------------------------
- Proxy Pattern: Frontend visually represents nodes that lazy-load rich text/images only when interacted with.
- Observer Pattern: Rendering engine observes camera zoom state to trigger LOD changes.
- Decorator Pattern: Attaching visual modifiers (like an image thumbnail ring) to base node UI components.
- Strategy Pattern: Toggling between LocalAnalysisStrategy and CloudAnalysisStrategy based on user tier.
================================================================================