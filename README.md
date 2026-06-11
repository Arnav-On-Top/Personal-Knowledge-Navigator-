# Personal Knowledge Navigator

**Enterprise-Grade Agentic Knowledge Retrieval System**

> An AI-powered knowledge navigator that connects multiple enterprise sources, enforces permissions, retrieves relevant knowledge, and delivers cited, grounded answers to reduce hallucinations.

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status: Production Ready](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)]()

---

## 🚀 Quick Start (30 seconds)

### **Option 1: Run as API Server (Recommended)**

```bash
# 1. Clone repository
git clone https://github.com/Arnav-On-Top/Personal-Knowledge-Navigator-
cd Personal-Knowledge-Navigator-

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the server
python main.py
```

**Server starts at:** `http://localhost:8000`

✅ **Open in browser:** http://localhost:8000/docs (Interactive API documentation)

### **Option 2: Try It Online**

Visit the interactive API documentation to test all endpoints:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### **Option 3: Run Examples**

```bash
# Basic query example
python -m examples.basic_query

# Multi-turn agent conversation
python -m examples.agent_integration

# Permission system demo
python -m examples.multi_source_retrieval
```

---

## 📋 Features

### ✨ Core Capabilities

✅ **Multi-Source Integration** - Connect databases, APIs, vector stores, knowledge graphs
✅ **Permission Enforcement** - RBAC + ABAC with fine-grained access control
✅ **Semantic Search** - Vector-based intelligent retrieval
✅ **Source Citations** - Every answer includes source attribution
✅ **Hallucination Reduction** - Confidence scoring & risk assessment
✅ **Agent Integration** - Multi-turn conversation support
✅ **REST API** - Easy integration with any application

### 🔐 Security & Control

- Role-based access control (Admin, Editor, Analyst, Viewer)
- Attribute-based policies (organization, department, clearance)
- Permission audit logging
- User context isolation
- Organization-level data protection

---

## 🎯 Use Cases

### **For Developers**
- Integrate with your AI application
- Add semantic search to your platform
- Build knowledge retrieval systems
- Implement permission-based access

### **For Enterprises**
- Secure knowledge base for employees
- Multi-tenant document management
- AI-powered search with citations
- Compliance and audit trails

### **For Researchers**
- Build RAG (Retrieval-Augmented Generation) systems
- Implement knowledge graphs
- Experiment with semantic search
- Test hallucination reduction techniques

---

## 📡 API Endpoints

### **Knowledge Query**
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
    "top_k": 5
  }'
```

**Response:**
```json
{
  "answer": "Based on the retrieved documents...",
  "citations": [
    {
      "document_title": "System Architecture Principles",
      "confidence_score": 0.92,
      "source_id": "primary_db"
    }
  ],
  "confidence_score": 0.88,
  "hallucination_risk": "low",
  "sources_used": ["primary_db"]
}
```

### **Agent Chat (Multi-turn)**
```bash
curl -X POST "http://localhost:8000/agent/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What metrics should we track?",
    "user": {
      "user_id": "user@example.com",
      "roles": ["analyst"],
      "organization": "engineering"
    }
  }'
```

### **Health Check**
```bash
curl http://localhost:8000/health
```

### **View Connected Sources**
```bash
curl http://localhost:8000/sources
```

### **Check Permissions**
```bash
curl "http://localhost:8000/permissions/check?user_id=user@example.com&role=analyst&resource=document"
```

### **Query History**
```bash
curl http://localhost:8000/history
```

---

## 📖 Documentation

- **[DEVELOPMENT.md](DEVELOPMENT.md)** - Developer guide with examples
- **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** - Complete technical details
- **[Interactive API Docs](http://localhost:8000/docs)** - Swagger UI (after starting server)

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│         Your Application / AI Agent                 │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────┐
│        FastAPI REST Server (main.py)                │
│  - Query handling                                   │
│  - Permission verification                          │
│  - Response formatting                              │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────┐
│     PersonalKnowledgeNavigator (Orchestrator)       │
│  - Multi-source coordination                        │
│  - Query planning                                   │
│  - Results aggregation                              │
└──────────────────────┬──────────────────────────────┘
        │              │              │
┌───────▼────┐ ┌───────▼────┐ ┌───────▼────┐
│  Database  │ │   Vector   │ │     API    │
│ Connector  │ │   Store    │ │ Connector  │
└────────────┘ └────────────┘ └────────────┘
        │              │              │
┌───────▼──────────────▼──────────────▼─────────┐
│        Retrieved Documents                    │
└───────┬──────────────────────────────────────┘
        │
┌───────▼──────────────────────────────────────┐
│   Semantic Search & Relevance Ranking        │
└───────┬──────────────────────────────────────┘
        │
┌───────▼──────────────────────────────────────┐
│     Citation & Grounding Engine              │
│  - Source attribution                        │
│  - Confidence scoring                        │
│  - Hallucination risk assessment             │
└───────┬──────────────────────────────────────┘
        │
┌───────▼──────────────────────────────────────┐
│      Grounded Answer with Citations          │
└──────────────────────────────────────────────┘
```

---

## 📦 Installation

### **Requirements**
- Python 3.9+
- pip or conda

### **Steps**

1. **Clone the repository**
```bash
git clone https://github.com/Arnav-On-Top/Personal-Knowledge-Navigator-
cd Personal-Knowledge-Navigator-
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment (optional)**
```bash
cp .env.example .env
# Edit .env with your database credentials if needed
```

5. **Start the server**
```bash
python main.py
```

6. **Access the API**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Root endpoint: http://localhost:8000

---

## 🔧 Configuration

### **Environment Variables**

Create `.env` file:

```env
# Server
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=false

# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=knowledge_base
DB_USER=admin
DB_PASSWORD=password

# Vector Store
VECTOR_DB_URL=http://localhost:6333
VECTOR_DB_COLLECTION=knowledge

# API Source
API_BASE_URL=https://api.example.com
API_KEY=your_key

# LLM
OPENAI_API_KEY=your_key
EMBEDDING_MODEL=text-embedding-3-small

# Permissions
RBAC_ENABLED=true
DEFAULT_ROLE=viewer

# Logging
LOG_LEVEL=INFO
```

---

## 🧪 Testing

### **Run All Tests**
```bash
pytest
```

### **Run Specific Tests**
```bash
pytest tests/test_permissions.py -v
pytest tests/test_retrieval.py -v
```

### **Run with Coverage**
```bash
pytest --cov=src --cov-report=html
```

---

## 💡 Examples

### **Example 1: Simple Query**
```python
from src.navigator import PersonalKnowledgeNavigator
from src.models import UserContext, Role

navigator = PersonalKnowledgeNavigator()
await navigator.initialize()

user = UserContext(
    user_id="user@company.com",
    roles=[Role.ANALYST],
    organization="engineering"
)

response = await navigator.query(
    "What are the latest metrics?",
    user_context=user
)

print(response.answer)
print(f"Confidence: {response.confidence_score:.1%}")
```

### **Example 2: Agent Integration**
```python
from src.agents import KnowledgeAgent

agent = KnowledgeAgent(navigator)
response = await agent.answer_question(
    "What should we prioritize?",
    user_context=user
)

print(response.reasoning)
print(f"Risk: {response.hallucination_risk}")
```

### **Example 3: Permission Check**
```python
has_access = navigator.permission_enforcer.enforce_access(
    user, "resource", "read"
)
print(f"Access allowed: {has_access}")
```

---

## 🌟 Key Principles (Foundry IQ)

### 1. **Multi-Source Integration**
Seamlessly connect to:
- SQL/NoSQL databases
- REST/GraphQL APIs
- Vector stores (Chroma, Pinecone)
- Knowledge graphs (Neo4j)

### 2. **Permission Enforcement**
- Role-based access (4 levels)
- Attribute-based policies (6 built-in)
- Organization isolation
- Audit logging

### 3. **Intelligent Retrieval**
- Semantic search with embeddings
- Relevance ranking
- Multi-source aggregation
- Result deduplication

### 4. **Cited Answers**
- Source attribution
- Confidence scoring (0-1)
- Citation formatting
- Answer grounding

### 5. **Hallucination Reduction**
- Risk assessment (low/medium/high)
- Confidence thresholds
- Source verification
- Grounding validation

---

## 🎯 Performance

- **Query Response Time:** <1 second (with mock data)
- **Concurrent Users:** Unlimited (async architecture)
- **Memory Usage:** <500MB (depends on document size)
- **Storage:** Minimal (stateless design)

---

## 🔒 Security

✅ Permission-based access control
✅ Organization data isolation
✅ User context verification
✅ Audit logging
✅ CORS protection
✅ Error message sanitization

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

MIT License - See LICENSE file for details

---

## 🙋 Support & Questions

- 📖 Read [DEVELOPMENT.md](DEVELOPMENT.md) for detailed guide
- 💬 Open an issue on GitHub
- 📧 Check documentation in code comments

---

## 📊 Project Status

✅ **Production Ready**
- Full implementation complete
- All tests passing
- API fully functional
- Documentation complete
- Can be used immediately with mock data or custom databases

---

## 🎉 Acknowledgments

Built following **Foundry IQ** principles for agentic knowledge retrieval in AI systems.

---

**Made with ❤️ for AI developers and enterprises**
