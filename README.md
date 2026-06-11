Personal Knowledge Navigator
Agentic Knowledge Retrieval System – Functional Prototype with Mock Data

An AI-powered knowledge navigator that enforces permissions, retrieves relevant information, and delivers cited, grounded answers. Currently runs with a mock knowledge base – extensible to real data sources.

https://img.shields.io/badge/python-3.9+-blue.svg
https://img.shields.io/badge/License-MIT-yellow.svg
https://img.shields.io/badge/Status-Functional%2520Prototype-yellowgreen.svg

🚀 Quick Start (30 seconds)
bash
# 1. Clone repository
git clone https://github.com/Arnav-On-Top/Personal-Knowledge-Navigator-
cd Personal-Knowledge-Navigator-

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the API server
python main.py
Server starts at: http://localhost:8000

✅ Open in browser: http://localhost:8000/docs – Interactive API documentation

📋 What Works Now
✅ Core Features (Implemented)
REST API – Full FastAPI server with Swagger UI

Mock Knowledge Base – 5 sample documents on architecture, metrics, security, etc.

Permission Enforcement – RBAC (Admin, Editor, Analyst, Viewer) + ABAC policies

Keyword Search – Simple text matching (easily upgradeable to semantic search)

Source Citations – Every answer includes document titles and confidence scores

Hallucination Risk Assessment – Low/Medium/High based on confidence

Multi‑turn Agent – Knowledge agent with reasoning and conversation history

Query History – Audit logging of all queries

🔜 Ready for Extension
Connector placeholders – Add real databases, APIs, vector stores via src/connectors/

Semantic search stubs – Replace keyword search with embeddings

Test directory – Structure ready for unit tests

📡 API Endpoints
Health Check
bash
curl http://localhost:8000/health
Query Knowledge Base
bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What are the latest architecture decisions?",
    "user": {
      "user_id": "user@example.com",
      "roles": ["analyst"],
      "organization": "engineering"
    },
    "top_k": 3
  }'
Agent Chat (multi‑turn)
bash
curl -X POST "http://localhost:8000/agent/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What metrics should we track for API performance?",
    "user": {
      "user_id": "user@example.com",
      "roles": ["analyst"],
      "organization": "engineering"
    }
  }'
View Connected Sources
bash
curl http://localhost:8000/sources
Check Permissions
bash
curl "http://localhost:8000/permissions/check?user_id=user@example.com&role=analyst&resource=document"
Query History
bash
curl http://localhost:8000/history
🧪 Run an Example
bash
python -m examples.basic_query
This will:

Initialize the navigator

Create a user context

Run several example queries

Show citations and confidence scores

📁 Project Structure
text
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
🔧 Configuration
Copy .env.example to .env and adjust values (optional – defaults work with mock data):

env
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=false
LOG_LEVEL=INFO
🔌 Adding Real Data Sources (Roadmap)
The system is designed to be extended:

Database Connector – Implement src/connectors/database.py

API Connector – Implement src/connectors/api.py

Vector Store – Implement src/retrieval/search.py with embeddings

Knowledge Graph – Implement src/connectors/knowledge_graph.py

See inline comments in placeholder files for guidance.

🧪 Testing (Planned)
Test files are stubbed in tests/. When ready:

bash
pytest
pytest --cov=src
🌟 Key Design Principles
Multi‑source ready – Plugin architecture for connectors

Permission enforcement – RBAC + ABAC, organization isolation

Grounded answers – Citations with confidence scores

Hallucination reduction – Risk assessment per answer

Async/await – Non‑blocking I/O for scalability

🤝 Contributing
Contributions welcome! Especially:

Real connectors (PostgreSQL, REST APIs, Chroma)

Semantic search implementation

Unit tests

Additional examples

📄 License
MIT License – see repository for details.

Built with ❤️ – a functional foundation ready for enterprise AI retrieval.

