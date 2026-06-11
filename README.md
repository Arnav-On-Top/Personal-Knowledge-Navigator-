# Personal Knowledge Navigator

**Agentic Knowledge Retrieval System – Functional Prototype with Mock Data**

> An AI-powered knowledge navigator that enforces permissions, retrieves relevant information, and delivers cited, grounded answers. Currently runs with a mock knowledge base – extensible to real data sources.

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status: Functional Prototype](https://img.shields.io/badge/Status-Functional%20Prototype-yellowgreen.svg)]()

---

## Quick Start

1. Clone the repository and enter the folder.  
2. Create a virtual environment (recommended).  
3. Install dependencies from `requirements.txt`.  
4. Run the API server with `python main.py`.  

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

{
  "question": "What are the latest architecture decisions?",
  "user": {
    "user_id": "user@example.com",
    "roles": ["analyst"],
    "organization": "engineering"
  },
  "top_k": 3
}

### Example Response

{
  "answer": "Based on the retrieved documents...",
  "citations": [
    {
      "document_title": "System Architecture Principles",
      "confidence_score": 0.92,
      "source_id": "mock_source"
    }
  ],
  "confidence_score": 0.88,
  "hallucination_risk": "low",
  "sources_used": ["mock_source"]
}

---

## Running an Example Script

From the project root, execute:

python -m examples.basic_query

This will initialize the navigator, create a user context, run several queries, and display citations and confidence scores.

---

## Project Structure

Personal-Knowledge-Navigator-/
├── main.py                 # FastAPI server
├── requirements.txt        # Dependencies
├── .env.example            # Environment variables template
├── examples/
│   └── basic_query.py      # Example usage script
└── src/
    ├── __init__.py
    ├── config.py           # Environment configuration
    ├── models.py           # Data models (UserContext, Citation, etc.)
    ├── mock_data.py        # Sample documents and keyword search
    ├── navigator.py        # Main orchestrator
    ├── agents/             # Knowledge agent for conversation
    ├── permissions/        # RBAC and ABAC enforcer
    ├── utils/              # Logging helpers
    ├── connectors/         # Stubs for future real connectors
    ├── retrieval/          # Stubs for semantic search
    └── citation/           # Stubs for advanced grounding

---

## Configuration

Copy `.env.example` to `.env` and adjust values (optional – defaults work with mock data):

API_HOST=0.0.0.0
API_PORT=8000
DEBUG=false
LOG_LEVEL=INFO

---

## Adding Real Data Sources (Roadmap)

The system is designed to be extended. To add a new data source:

1. Implement a connector class in `src/connectors/` (e.g., `database.py`).  
2. Inherit from `BaseConnector` (see placeholder files).  
3. Register the connector with the navigator using `add_source()`.  

Refer to inline comments in the placeholder files for guidance.

---

## Testing (Planned)

Test stubs are located in the `tests/` directory. When ready, run:

pytest
pytest --cov=src

---

## Key Design Principles

- **Multi‑source ready** – Plugin architecture for connectors.  
- **Permission enforcement** – RBAC + ABAC with organization isolation.  
- **Grounded answers** – Citations with confidence scores.  
- **Hallucination reduction** – Risk assessment per answer.  
- **Async/await** – Non‑blocking I/O for scalability.

---

## Contributing

Contributions are welcome, especially for:

- Real connectors (PostgreSQL, REST APIs, Chroma, Neo4j).  
- Semantic search implementation (embeddings + vector store).  
- Unit tests.  
- Additional examples.

---

## License

MIT License – see repository for details.

---

**Built with ❤️ – a functional foundation ready for enterprise AI retrieval.**
