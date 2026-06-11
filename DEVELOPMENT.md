# Personal Knowledge Navigator - Development Guide

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/Arnav-On-Top/Personal-Knowledge-Navigator-
cd Personal-Knowledge-Navigator-

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

1. Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

2. Update `.env` with your database and API credentials

### Running Examples

#### Basic Query Example
```bash
python -m examples.basic_query
```

This demonstrates:
- Initializing the navigator
- Creating user contexts
- Querying the knowledge base
- Receiving grounded answers with citations

#### Agent Integration Example
```bash
python -m examples.agent_integration
```

This demonstrates:
- Multi-turn conversation
- Agent reasoning
- Hallucination risk assessment

#### Multi-Source Retrieval Example
```bash
python -m examples.multi_source_retrieval
```

This demonstrates:
- Connecting multiple sources
- Permission enforcement
- Role-based access control

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_permissions.py

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=src tests/
```

## Architecture Overview

### Core Components

1. **Navigator** (`src/navigator.py`)
   - Main orchestrator
   - Coordinates all components
   - Manages data sources
   - Executes queries

2. **Connectors** (`src/connectors/`)
   - Base connector interface
   - Database connector
   - Extensible for APIs, document stores, etc.

3. **Permissions** (`src/permissions/`)
   - RBAC engine with 4 roles
   - Permission enforcer
   - Access control decisions

4. **Retrieval** (`src/retrieval/`)
   - Semantic search
   - Document ranking
   - Relevance scoring

5. **Citation** (`src/citation/`)
   - Grounding engine
   - Citation creation
   - Hallucination risk assessment

6. **Agents** (`src/agents/`)
   - Knowledge agent for LLMs
   - Multi-turn conversation support
   - Reasoning generation

## Development Workflow

### Adding a New Data Source Connector

1. Create a new file in `src/connectors/` (e.g., `api_connector.py`)

2. Extend `BaseConnector`:
```python
from src.connectors.base import BaseConnector
from src.models import SourceType

class APIConnector(BaseConnector):
    def __init__(self, source_id, source_name, api_url, credentials):
        super().__init__(
            source_id, 
            source_name, 
            SourceType.API,
            credentials
        )
        self.api_url = api_url
    
    async def connect(self) -> bool:
        # Implement connection logic
        pass
    
    async def search(self, query, user_context=None):
        # Implement search logic
        pass
    
    # Implement other abstract methods...
```

3. Register the connector in `PersonalKnowledgeNavigator`:
```python
connector = APIConnector(...)
navigator.add_source(connector)
```

### Adding Custom Permission Rules

```python
from src.permissions.enforcer import PermissionEnforcer

enforcer = PermissionEnforcer()

# Add custom attribute rule
def check_department_access(user_context, resource_attributes):
    user_dept = user_context.attributes.get("department")
    resource_dept = resource_attributes.get("department")
    return user_dept == resource_dept or user_context.has_role("admin")

enforcer.add_attribute_rule("department_check", check_department_access)
```

### Extending Citation/Grounding

```python
from src.citation.grounding import GroundingEngine

class CustomGroundingEngine(GroundingEngine):
    def _assess_hallucination_risk(self, answer, citations, confidence):
        # Custom hallucination risk logic
        pass
```

## Key Design Principles

### Foundry IQ Principles

1. **Multi-Source Integration**
   - Plugin architecture for connectors
   - Support for databases, APIs, document stores
   - Unified search interface

2. **Permission Enforcement**
   - RBAC with role hierarchies
   - ABAC with custom rules
   - Fine-grained access control

3. **Intelligent Retrieval**
   - Semantic search with embeddings
   - Relevance ranking
   - Source aggregation

4. **Cited Answers**
   - Source attribution
   - Confidence scoring
   - Citation formatting

5. **Hallucination Reduction**
   - Grounding in retrieved documents
   - Risk assessment
   - Confidence thresholds

### Async/Await Pattern

All I/O operations use async/await:
```python
async def query(self, question, user_context):
    documents = await self.search(question)
    answer = self.generate_answer(documents)
    return answer
```

### Type Safety

Full type hints throughout:
```python
async def search(
    self,
    query: SearchQuery,
    user_context: Optional[UserContext] = None
) -> List[RetrievedDocument]:
```

## Testing Strategy

### Unit Tests

Located in `tests/`:
- `test_connectors.py` - Connector tests
- `test_permissions.py` - Permission enforcement tests
- `test_retrieval.py` - Search and grounding tests

### Running Tests

```bash
# All tests
pytest

# Specific test class
pytest tests/test_permissions.py::TestRBAC

# Specific test method
pytest tests/test_permissions.py::TestRBAC::test_admin_permissions

# With coverage
pytest --cov=src --cov-report=html
```

### Fixtures

Common test fixtures in `conftest.py`:
- `sample_user_context` - Basic user for testing
- `admin_user_context` - Admin user for testing
- `viewer_user_context` - Viewer user for testing
- `sample_document` - Sample document for testing

## Performance Considerations

### Embedding Caching
```python
# Embeddings are cached to avoid redundant computation
semantic_search.embedding_cache
```

### Source Prioritization
```python
# Sources are searched in priority order
# Configure via SourceConfig.priority
```

### Result Limiting
```python
# Control maximum results per query
search_query.top_k = 5
search_query.min_relevance_threshold = 0.5
```

## Troubleshooting

### Database Connection Issues
```python
# Check if source is connected
if navigator.sources["primary_db"].is_connected:
    print("Connected!")
else:
    await navigator.sources["primary_db"].connect()
```

### Low Confidence Scores
- Check `min_relevance_threshold`
- Verify documents have good embeddings
- Check source quality

### Permission Denials
```python
# Debug permission issues
enforcer.audit_access_decision(
    user_context, "resource", "action", False,
    reason="Debug info"
)
```

## Deployment

### Production Checklist

- [ ] Environment variables configured
- [ ] Database connections tested
- [ ] API credentials secured
- [ ] Logging configured
- [ ] Tests passing (100% coverage preferred)
- [ ] Documentation updated
- [ ] Security review completed

### Docker Deployment

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src src/
COPY examples examples/

CMD ["python", "-m", "examples.basic_query"]
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT
