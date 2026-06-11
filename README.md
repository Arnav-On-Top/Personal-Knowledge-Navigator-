# Personal Knowledge Navigator

Agentic Knowledge Retrieval System (Functional Prototype)

A knowledge retrieval system that enforces permissions, searches a knowledge base, and returns grounded answers with citations. The current implementation uses a mock knowledge base and keyword-based retrieval.

---

## Features

### Implemented

* FastAPI REST API
* Mock knowledge base with sample documents
* Role-Based Access Control (RBAC)
* Attribute-Based Access Control (ABAC)
* Keyword search retrieval
* Source citations and confidence scoring
* Hallucination risk assessment
* Multi-turn conversational agent
* Query history and audit logging

### Current Limitations

* Uses mock data only
* No external database connectors
* No vector database integration
* No semantic embedding search
* Limited sample dataset

---

## Requirements

* Python 3.9+
* pip

---

## Installation

1. Clone the repository

```bash
git clone https://github.com/Arnav-On-Top/Personal-Knowledge-Navigator-
cd Personal-Knowledge-Navigator-
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Start the server

```bash
python main.py
```

Server URL:

```text
http://localhost:8000
```

API Documentation:

```text
http://localhost:8000/docs
```

---

## API Endpoints

### Health Check

```bash
GET /health
```

Example:

```bash
curl http://localhost:8000/health
```

---

### Query Knowledge Base

```bash
POST /query
```

Example:

```bash
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
```

---

### Agent Chat

```bash
POST /agent/chat
```

Example:

```bash
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
```

---

### List Sources

```bash
GET /sources
```

Example:

```bash
curl http://localhost:8000/sources
```

---

### Permission Check

```bash
GET /permissions/check
```

Example:

```bash
curl "http://localhost:8000/permissions/check?user_id=user@example.com&role=analyst&resource=document"
```

---

### Query History

```bash
GET /history
```

Example:

```bash
curl http://localhost:8000/history
```

---

## Example Usage

Run the included example:

```bash
python -m examples.basic_query
```

The example demonstrates:

* Creating a user context
* Running queries
* Viewing citations
* Viewing confidence scores

---

## Project Structure

```text
Personal-Knowledge-Navigator-/
│
├── main.py
├── requirements.txt
├── .env.example
│
├── examples/
│   └── basic_query.py
│
└── src/
    ├── config.py
    ├── models.py
    ├── mock_data.py
    ├── navigator.py
    │
    ├── agents/
    ├── permissions/
    ├── connectors/
    ├── retrieval/
    ├── citation/
    └── utils/
```

---

## Configuration

Create a `.env` file (optional).

```env
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=false
LOG_LEVEL=INFO
```

Default values work without additional configuration.

---

## Architecture

```text
User Request
      │
      ▼
 Permission Check
      │
      ▼
 Keyword Retrieval
      │
      ▼
 Knowledge Agent
      │
      ▼
 Citation Generation
      │
      ▼
 Response + Confidence Score
```

---

## License

MIT License

```
```
