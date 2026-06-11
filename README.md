# Personal Knowledge Navigator

**Agentic Knowledge Retrieval System – Functional Prototype with Mock Data**

> An AI-powered knowledge navigator that enforces permissions, retrieves relevant information, and delivers cited, grounded answers. Currently runs with a mock knowledge base – extensible to real data sources.

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status: Functional Prototype](https://img.shields.io/badge/Status-Functional%20Prototype-yellowgreen.svg)]()

---

## Quick Start

1. **Clone the repository** and enter the folder.  
2. **Create a virtual environment** (recommended).  
3. **Install dependencies** from `requirements.txt`.  
4. **Run the API server** with `python main.py`.  

The server starts at `http://localhost:8000`. Open `http://localhost:8000/docs` in your browser to see the interactive Swagger UI.

---

## What Works Now

### Core Features (Implemented)

- **REST API** – Full FastAPI server with automatic documentation.  
- **Mock Knowledge Base** – Five sample documents covering architecture, performance metrics, data consistency, deployment, and security.  
- **Permission Enforcement** – Role‑based (Admin, Editor, Analyst, Viewer) plus attribute‑based policies.  
- **Keyword Search** – Simple text matching (easily upgradeable to semantic search).  
- **Source Citations** – Every answer includes document titles, relevance, and confidence scores.  
- **Hallucination Risk Assessment** – Low / Medium / High based on confidence.  
- **Multi‑turn Agent** – Knowledge agent with reasoning trace and conversation history.  
- **Query History** – Automatic audit logging of all queries.

### Ready for Extension

- **Connector placeholders** – Add real databases, APIs, or vector stores via the `src/connectors/` directory.  
- **Semantic search stubs** – Replace keyword matching with embeddings.  
- **Test directory** – Structure is ready for unit tests.

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check – returns status and connected sources. |
| GET | `/sources` | Lists all connected data sources. |
| GET | `/history` | Returns query history for auditing. |
| POST | `/query` | Ask a natural language question; returns grounded answer with citations. |
| POST | `/agent/chat` | Multi‑turn conversation with the knowledge agent. |
| GET | `/permissions/check` | Check if a user has access to a resource. |

### Example Request to `/query`

Send a JSON payload:

```json
{
  "question": "What are the latest architecture decisions?",
  "user": {
    "user_id": "user@example.com",
    "roles": ["analyst"],
    "organization": "engineering"
  },
  "top_k": 3
}
