# Personal Knowledge Navigator

An enterprise-grade Personal Knowledge Navigator implementation following **Foundry IQ** principles for Agentic Knowledge Retrieval.

## Overview

The Personal Knowledge Navigator is designed to:
- **Connect Multiple Enterprise Sources**: Integrate with diverse data sources (databases, APIs, document stores)
- **Enforce Permissions**: Implement role-based access control and permission verification
- **Retrieve Relevant Knowledge**: Use semantic search and relevance ranking
- **Deliver Cited, Grounded Answers**: Provide responses with source attribution to reduce hallucinations
- **Reduce AI Hallucinations**: Ground all answers in retrieved documents with full citations

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    User Agent/Application                   │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│              Knowledge Navigator API Layer                   │
│  - Query Processing & Intent Understanding                  │
│  - Permission Enforcement                                   │
└──────────────────────────┬──────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
┌───────▼────────┐ ┌───────▼────────┐ ┌───────▼────────┐
│ Source 1:      │ │ Source 2:      │ │ Source 3:      │
│ Database       │ │ Document Store │ │ Knowledge Base │
│ Connector      │ │ Connector      │ │ Connector      │
└────────────────┘ └────────────────┘ └────────────────┘
        │                  │                  │
┌───────▼──────────────────▼──────────────────▼─────────┐
│              Retrieval & Ranking Engine                │
│  - Semantic Search                                    │
│  - Relevance Scoring                                  │
│  - Source Validation                                  │
└───────┬──────────────────────────────────────────────┘
        │
┌───────▼──────────────────────────────────────────────┐
│         Citation & Grounding Engine                  │
│  - Source Attribution                               │
│  - Confidence Scoring                               │
│  - Answer Generation with Citations                 │
└──────────────────────────────────────────────────────┘
```

## Key Components

### 1. **Source Connectors** (`src/connectors/`)
- Database Connector: SQL databases, NoSQL stores
- API Connector: REST/GraphQL APIs
- Document Store Connector: Vector databases, file systems
- Knowledge Base Connector: Structured knowledge graphs

### 2. **Permission Engine** (`src/permissions/`)
- Role-Based Access Control (RBAC)
- Attribute-Based Access Control (ABAC)
- Permission Verification & Enforcement

### 3. **Retrieval Engine** (`src/retrieval/`)
- Semantic Search Implementation
- Relevance Ranking
- Source Aggregation & Deduplication

### 4. **Citation Engine** (`src/citation/`)
- Source Attribution
- Confidence Scoring
- Answer Generation with Citations

### 5. **Agent Integration** (`src/agents/`)
- Knowledge Agent for AI assistants
- Query Planning
- Response Formatting

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file with your source configurations:

```env
# Database Source
DB_HOST=localhost
DB_PORT=5432
DB_NAME=knowledge_base
DB_USER=admin
DB_PASSWORD=your_password

# Vector Database (for semantic search)
VECTOR_DB_URL=http://localhost:6333
VECTOR_DB_COLLECTION=knowledge

# API Source
API_BASE_URL=https://api.example.com
API_KEY=your_api_key

# Permissions
RBAC_ENABLED=true
DEFAULT_ROLE=viewer
```

## Usage

### Basic Query

```python
from src.navigator import PersonalKnowledgeNavigator
from src.models import UserContext

# Initialize navigator
navigator = PersonalKnowledgeNavigator(config_path=".env")

# Create user context
user_context = UserContext(
    user_id="user123",
    roles=["analyst", "viewer"],
    organization="engineering"
)

# Query knowledge base
query = "What are the latest architecture decisions?"
response = navigator.query(
    question=query,
    user_context=user_context,
    top_k=5
)

# Response includes citations
print(response.answer)
for citation in response.citations:
    print(f"- Source: {citation.source}")
    print(f"  Document: {citation.document_id}")
    print(f"  Confidence: {citation.confidence_score}")
```

### Agent Integration

```python
from src.agents import KnowledgeAgent

# Create agent
agent = KnowledgeAgent(navigator=navigator)

# Get grounded answer
agent_response = agent.answer_question(
    question="What are the performance metrics?",
    user_context=user_context
)

print(agent_response.answer)
print(f"Hallucination Risk: {agent_response.hallucination_risk}")
```

## Features

✅ **Multi-Source Integration**: Connect to databases, APIs, document stores, and knowledge graphs
✅ **Permission Enforcement**: RBAC/ABAC with fine-grained access control
✅ **Semantic Search**: Vector-based similarity for intelligent retrieval
✅ **Source Attribution**: Complete citation trails for all answers
✅ **Confidence Scoring**: Understand answer reliability
✅ **Hallucination Mitigation**: All responses grounded in actual sources
✅ **Agent-Ready**: Designed for AI agent integration
✅ **Extensible**: Plugin architecture for custom connectors

## File Structure

```
Personal-Knowledge-Navigator-/
├── README.md
├── requirements.txt
├── .env.example
├── src/
│   ├── __init__.py
│   ├── navigator.py              # Main orchestrator
│   ├── models.py                 # Data models
│   ├── config.py                 # Configuration management
│   ├── connectors/
│   │   ├── __init__.py
│   │   ├── base.py              # Base connector interface
│   │   ├── database.py          # Database connector
│   │   ├── api.py               # API connector
│   │   ├── vector_store.py      # Vector database connector
│   │   └── knowledge_graph.py   # Knowledge graph connector
│   ├── permissions/
│   │   ├── __init__.py
│   │   ├── rbac.py              # Role-based access control
│   │   ├── abac.py              # Attribute-based access control
│   │   └── enforcer.py          # Permission enforcement
│   ├── retrieval/
│   │   ├── __init__.py
│   │   ├── search.py            # Semantic search
│   │   ├── ranker.py            # Relevance ranking
│   │   └── aggregator.py        # Source aggregation
│   ├── citation/
│   │   ├── __init__.py
│   │   ├── grounding.py         # Answer grounding
│   │   ├── attribution.py       # Source attribution
│   │   └── confidence.py        # Confidence scoring
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── knowledge_agent.py   # Knowledge agent
│   │   └── tools.py             # Agent tools
│   └── utils/
│       ├── __init__.py
│       ├── embeddings.py        # Embedding generation
│       ├── preprocessing.py     # Text preprocessing
│       └── logging.py           # Logging utilities
├── tests/
│   ├── __init__.py
│   ├── test_connectors.py
│   ├── test_permissions.py
│   ├── test_retrieval.py
│   └── test_citation.py
└── examples/
    ├── basic_query.py
    ├── agent_integration.py
    └── multi_source_retrieval.py
```

## Foundry IQ Principles

This implementation adheres to Foundry IQ's Agentic Knowledge Retrieval framework:

1. **Enterprise Source Integration**: Multiple data source connectors
2. **Permission Enforcement**: Role-based and attribute-based access control
3. **Intelligent Retrieval**: Semantic search with relevance ranking
4. **Cited Answers**: Every response includes source attribution
5. **Hallucination Reduction**: Confidence scoring and grounding verification
6. **Agent-Native Design**: Built for AI agent integration

## License

MIT

## Author

Arnav-On-Top
