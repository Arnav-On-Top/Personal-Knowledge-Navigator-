"""
Mock data provider for demonstration purposes.
Provides sample documents and knowledge for testing without real data sources.
"""

from typing import List, Dict, Any
from src.models import RetrievedDocument, SourceType
from datetime import datetime


class MockDataProvider:
    """Provides mock data for demonstrations."""

    @staticmethod
    def get_sample_documents() -> List[RetrievedDocument]:
        """Get sample documents for testing."""
        return [
            RetrievedDocument(
                doc_id="doc_001",
                source_id="mock_source",
                source_type=SourceType.DATABASE,
                title="System Architecture Principles",
                content="""
                Our system architecture is built on microservices principles:
                
                1. Scalability: Each service can scale independently
                2. Resilience: Failure in one service doesn't crash the system
                3. Maintainability: Services are loosely coupled and highly cohesive
                4. Observability: Comprehensive logging and monitoring across services
                
                Key architectural decisions:
                - Use async/await for non-blocking operations
                - Implement circuit breakers for fault tolerance
                - Use event-driven communication where appropriate
                - Maintain clear separation of concerns
                
                These principles have been in place since 2023 and have significantly
                improved our system reliability and developer productivity.
                """,
                metadata={
                    "author": "Architecture Team",
                    "date": "2024-01-15",
                    "category": "Architecture",
                    "version": "2.1"
                },
                relevance_score=0.92,
                access_level="internal"
            ),
            RetrievedDocument(
                doc_id="doc_002",
                source_id="mock_source",
                source_type=SourceType.DATABASE,
                title="Performance Monitoring Metrics",
                content="""
                Key metrics we track for system performance:
                
                Response Time Metrics:
                - API Response Time: Target <100ms (p99)
                - Database Query Time: Target <50ms
                - Cache Hit Rate: Target >80%
                
                Resource Metrics:
                - CPU Utilization: Monitor for >80% sustained usage
                - Memory Usage: Alert if >85% sustained
                - Disk I/O: Monitor for bottlenecks
                
                Application Metrics:
                - Request Error Rate: Target <0.1%
                - Service Availability: Target 99.99%
                - Transaction Success Rate: Target >99.9%
                
                We use Prometheus for metrics collection and Grafana for visualization.
                All metrics are stored for 30 days for trend analysis.
                """,
                metadata={
                    "author": "DevOps Team",
                    "date": "2024-02-10",
                    "category": "Operations",
                    "version": "1.5"
                },
                relevance_score=0.88,
                access_level="internal"
            ),
            RetrievedDocument(
                doc_id="doc_003",
                source_id="mock_source",
                source_type=SourceType.DATABASE,
                title="Data Consistency Strategies",
                content="""
                Ensuring data consistency across distributed services:
                
                1. Eventual Consistency Pattern:
                   - Used for non-critical operations
                   - Services communicate via message queues
                   - Conflict resolution is handled at the application level
                
                2. Strong Consistency:
                   - Required for financial transactions
                   - Implemented using distributed transactions
                   - Uses two-phase commit protocol
                
                3. Saga Pattern:
                   - For long-running transactions
                   - Each service handles its own transaction
                   - Compensating transactions for rollback
                
                Best Practices:
                - Always define consistency requirements per feature
                - Use idempotent operations
                - Implement proper error handling
                - Monitor consistency violations
                
                Implementation tools:
                - PostgreSQL with ACID guarantees
                - Redis for caching with TTL
                - Message queues for asynchronous updates
                """,
                metadata={
                    "author": "Database Team",
                    "date": "2024-01-20",
                    "category": "Data Management",
                    "version": "2.0"
                },
                relevance_score=0.85,
                access_level="internal"
            ),
            RetrievedDocument(
                doc_id="doc_004",
                source_id="mock_source",
                source_type=SourceType.DATABASE,
                title="Deployment Procedures",
                content="""
                Standard deployment procedures for production systems:
                
                Pre-Deployment Checklist:
                1. All tests passing (unit, integration, e2e)
                2. Code review approved
                3. Security scan passed
                4. Performance benchmarks acceptable
                5. Documentation updated
                
                Deployment Steps:
                1. Create release branch from main
                2. Run full test suite
                3. Build Docker image
                4. Push to staging environment
                5. Run smoke tests
                6. If all pass, promote to production
                
                Canary Deployment:
                - Deploy to 5% of traffic first
                - Monitor error rates and performance
                - If healthy, increase to 25%, 50%, 100%
                - Rollback if issues detected
                
                Post-Deployment:
                - Monitor error logs
                - Check performance metrics
                - Be ready to rollback within 15 minutes
                - Full validation takes 1 hour
                """,
                metadata={
                    "author": "DevOps Team",
                    "date": "2024-02-01",
                    "category": "Deployment",
                    "version": "3.0"
                },
                relevance_score=0.89,
                access_level="internal"
            ),
            RetrievedDocument(
                doc_id="doc_005",
                source_id="mock_source",
                source_type=SourceType.DATABASE,
                title="API Authentication & Security",
                content="""
                Security best practices for API authentication:
                
                Authentication Methods:
                1. OAuth 2.0: For third-party integrations
                2. JWT Tokens: For API clients
                3. API Keys: For service-to-service
                4. Basic Auth: Deprecated, avoid if possible
                
                Token Management:
                - Short-lived tokens (15 minutes)
                - Refresh tokens (7 days)
                - Token rotation on each refresh
                - Revocation on logout
                
                Security Headers:
                - X-Frame-Options: DENY
                - X-Content-Type-Options: nosniff
                - Strict-Transport-Security: max-age=31536000
                - Content-Security-Policy: appropriate restrictions
                
                Rate Limiting:
                - 1000 requests per hour per user
                - 10000 requests per hour per API key
                - Implement exponential backoff for clients
                
                CORS Configuration:
                - Only allow trusted origins
                - Specify allowed methods and headers
                - No credentials in wildcard origins
                """,
                metadata={
                    "author": "Security Team",
                    "date": "2024-02-05",
                    "category": "Security",
                    "version": "2.2"
                },
                relevance_score=0.87,
                access_level="internal"
            ),
        ]

    @staticmethod
    def get_knowledge_base() -> Dict[str, Any]:
        """Get complete knowledge base for the system."""
        return {
            "documents": MockDataProvider.get_sample_documents(),
            "categories": {
                "Architecture": ["doc_001"],
                "Operations": ["doc_002"],
                "Data Management": ["doc_003"],
                "Deployment": ["doc_004"],
                "Security": ["doc_005"],
            },
            "total_documents": 5,
            "last_updated": datetime.now().isoformat()
        }

    @staticmethod
    def search_documents(query: str, limit: int = 5) -> List[RetrievedDocument]:
        """Search documents by keyword (simple implementation)."""
        all_docs = MockDataProvider.get_sample_documents()
        query_lower = query.lower()
        
        scored_docs = []
        for doc in all_docs:
            score = 0
            # Check title
            if query_lower in doc.title.lower():
                score += 3
            # Check content
            if query_lower in doc.content.lower():
                score += 1
            
            if score > 0:
                doc.relevance_score = min(1.0, score / 4.0)
                scored_docs.append(doc)
        
        # Sort by relevance
        scored_docs.sort(key=lambda d: d.relevance_score, reverse=True)
        return scored_docs[:limit]
