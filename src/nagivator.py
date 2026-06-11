"""
Main orchestrator for Personal Knowledge Navigator.
Coordinates all components: multi-source retrieval, permissions, citation.
"""

import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime

from .models import (
    UserContext, GroundedAnswer, Citation, RetrievedDocument,
    SearchQuery, SearchResult, SourceType, Role
)
from .permissions.enforcer import PermissionEnforcer
from .mock_data import MockDataProvider
from .utils.logging import get_logger

logger = get_logger("navigator")

class PersonalKnowledgeNavigator:
    def __init__(self):
        self.sources: Dict[str, Any] = {}
        self.permission_enforcer = PermissionEnforcer()
        self.query_history: List[Dict] = []
        self._initialized = False
        self.mock_provider = MockDataProvider()
    
    async def initialize(self) -> bool:
        """Initialize navigator with mock data source."""
        self.sources["mock_source"] = {
            "source_id": "mock_source",
            "source_name": "Mock Knowledge Base",
            "source_type": SourceType.DATABASE,
            "is_connected": True,
            "priority": 1
        }
        self._initialized = True
        logger.info("✅ Navigator initialized with mock data source")
        return True
    
    async def shutdown(self):
        """Clean shutdown."""
        self._initialized = False
        logger.info("Navigator shutdown complete")
    
    async def search(self, query: SearchQuery) -> SearchResult:
        """Perform search across all enabled sources."""
        documents = []
        sources_searched = []
        
        # Use mock search for now
        if "mock_source" in self.sources:
            sources_searched.append("mock_source")
            docs = self.mock_provider.search_documents(query.query_text, limit=query.top_k)
            documents.extend(docs)
        
        # Sort by relevance
        documents.sort(key=lambda d: d.relevance_score, reverse=True)
        
        return SearchResult(
            documents=documents[:query.top_k],
            total_results=len(documents),
            query_time_ms=50.0,
            sources_searched=sources_searched
        )
    
    async def query(self, question: str, user_context: UserContext, top_k: int = 5) -> GroundedAnswer:
        """Main query endpoint - retrieve, filter by permissions, generate grounded answer."""
        # Create search query
        search_query = SearchQuery(
            query_text=question,
            top_k=top_k,
            min_relevance_threshold=0.5,
            user_context=user_context
        )
        
        # Retrieve documents
        search_result = await self.search(search_query)
        
        # Filter by permissions
        allowed_docs = []
        for doc in search_result.documents:
            if self.permission_enforcer.enforce_access(user_context, doc.access_level):
                allowed_docs.append(doc)
        
        # Generate grounded answer from allowed documents
        answer, citations = self._generate_grounded_answer(question, allowed_docs)
        
        # Calculate confidence
        if not citations:
            confidence = 0.3
            risk = "high"
        else:
            avg_conf = sum(c.confidence_score for c in citations) / len(citations)
            confidence = avg_conf * 0.8 + (len(citations) / top_k) * 0.2
            risk = "low" if confidence > 0.7 else "medium" if confidence > 0.4 else "high"
        
        grounded = GroundedAnswer(
            answer=answer,
            citations=citations,
            confidence_score=min(1.0, confidence),
            hallucination_risk=risk,
            sources_used=list(set(doc.source_id for doc in allowed_docs)),
            generated_at=datetime.utcnow()
        )
        
        # Log query history
        self.query_history.append({
            "question": question,
            "user_id": user_context.user_id,
            "timestamp": datetime.utcnow().isoformat(),
            "confidence": grounded.confidence_score
        })
        
        return grounded
    
    def _generate_grounded_answer(self, question: str, documents: List[RetrievedDocument]) -> tuple[str, List[Citation]]:
        """Generate answer from retrieved documents with citations."""
        if not documents:
            return "No relevant documents found for your query. Please try a different question or check your permissions.", []
        
        citations = []
        for doc in documents[:3]:  # Use top 3
            citation = Citation(
                source_id=doc.source_id,
                source_name=self.sources.get(doc.source_id, {}).get("source_name", "Unknown"),
                source_type=doc.source_type,
                document_id=doc.doc_id,
                document_title=doc.title,
                relevant_text=doc.content[:200] + "...",
                relevance_score=doc.relevance_score,
                confidence_score=doc.relevance_score * 0.9,
                access_verified=True,
                metadata=doc.metadata
            )
            citations.append(citation)
        
        # Simple answer synthesis (mock)
        answer = f"Based on the retrieved information about '{question}':\n\n"
        for i, doc in enumerate(documents[:2], 1):
            answer += f"{i}. From '{doc.title}': {doc.content[:150]}...\n\n"
        answer += "For full details, please refer to the cited sources."
        
        return answer, citations
    
    def get_sources_info(self) -> List[dict]:
        """Return info about all sources."""
        return [
            {
                "source_id": sid,
                "source_name": info.get("source_name", sid),
                "source_type": info.get("source_type", "database").value if hasattr(info.get("source_type"), "value") else str(info.get("source_type")),
                "is_connected": info.get("is_connected", False)
            }
            for sid, info in self.sources.items()
        ]
    
    def get_query_history(self) -> List[dict]:
        """Return query history for auditing."""
        return self.query_history
    
    async def add_source(self, connector):
        """Add a new data source connector."""
        self.sources[connector.source_id] = {
            "source_id": connector.source_id,
            "source_name": connector.source_name,
            "source_type": connector.source_type,
            "is_connected": await connector.connect(),
            "connector": connector
        }
