"""
Data models for Personal Knowledge Navigator.
Implements Foundry IQ principles with proper typing and validation.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from datetime import datetime
from enum import Enum


class Role(str, Enum):
    """User roles for permission system."""
    ADMIN = "admin"
    ANALYST = "analyst"
    VIEWER = "viewer"
    EDITOR = "editor"


class SourceType(str, Enum):
    """Types of knowledge sources."""
    DATABASE = "database"
    API = "api"
    DOCUMENT_STORE = "document_store"
    KNOWLEDGE_GRAPH = "knowledge_graph"
    FILE_SYSTEM = "file_system"


@dataclass
class Citation:
    """
    Citation information for grounded answers.
    Includes source attribution and confidence scoring.
    """
    source_id: str
    source_name: str
    source_type: SourceType
    document_id: str
    document_title: str
    relevant_text: str
    relevance_score: float  # 0.0 - 1.0
    confidence_score: float  # 0.0 - 1.0 (confidence in relevance)
    url: Optional[str] = None
    access_verified: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate citation fields."""
        assert 0.0 <= self.relevance_score <= 1.0, "Relevance score must be 0-1"
        assert 0.0 <= self.confidence_score <= 1.0, "Confidence score must be 0-1"


@dataclass
class UserContext:
    """
    User context for permission enforcement and personalization.
    """
    user_id: str
    roles: List[Role]
    organization: str
    permissions: Dict[str, bool] = field(default_factory=dict)
    attributes: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.utcnow)

    def has_role(self, role: Role) -> bool:
        """Check if user has a specific role."""
        return role in self.roles

    def has_permission(self, permission: str) -> bool:
        """Check if user has a specific permission."""
        return self.permissions.get(permission, False)


@dataclass
class RetrievedDocument:
    """
    A document retrieved from a knowledge source.
    """
    doc_id: str
    source_id: str
    source_type: SourceType
    title: str
    content: str
    metadata: Dict[str, Any]
    relevance_score: float
    embedding: Optional[List[float]] = None
    access_level: str = "public"
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class SearchQuery:
    """
    Query for knowledge retrieval.
    """
    query_text: str
    query_embedding: Optional[List[float]] = None
    filters: Dict[str, Any] = field(default_factory=dict)
    source_types: List[SourceType] = field(default_factory=list)
    top_k: int = 5
    min_relevance_threshold: float = 0.5
    user_context: Optional[UserContext] = None


@dataclass
class SearchResult:
    """
    Result from knowledge retrieval.
    """
    documents: List[RetrievedDocument]
    total_results: int
    query_time_ms: float
    sources_searched: List[str]


@dataclass
class GroundedAnswer:
    """
    An answer grounded in retrieved sources with citations.
    Implements Foundry IQ principle of reducing hallucinations.
    """
    answer: str
    citations: List[Citation]
    confidence_score: float  # Overall confidence in answer
    hallucination_risk: str  # "low", "medium", "high"
    sources_used: List[str]
    generated_at: datetime = field(default_factory=datetime.utcnow)
    model_used: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def has_citations(self) -> bool:
        """Check if answer has citations."""
        return len(self.citations) > 0

    def top_citations(self, n: int = 3) -> List[Citation]:
        """Get top N citations by confidence."""
        return sorted(
            self.citations,
            key=lambda c: c.confidence_score,
            reverse=True
        )[:n]


@dataclass
class SourceConfig:
    """
    Configuration for a knowledge source.
    """
    source_id: str
    source_name: str
    source_type: SourceType
    enabled: bool = True
    priority: int = 1  # Higher = searched first
    credentials: Dict[str, str] = field(default_factory=dict)
    settings: Dict[str, Any] = field(default_factory=dict)
    access_control: Dict[str, List[str]] = field(default_factory=dict)  # role -> permissions


@dataclass
class QueryPlan:
    """
    Query execution plan for the knowledge agent.
    """
    sources_to_search: List[SourceConfig]
    search_strategy: str  # "semantic", "hybrid", "keyword"
    expected_results_count: int
    estimated_time_ms: int
    requires_permission_check: bool = True


@dataclass
class AgentResponse:
    """
    Response from the knowledge agent.
    """
    answer: str
    citations: List[Citation]
    confidence_score: float
    hallucination_risk: str
    reasoning: str  # How the agent arrived at this answer
    query_plan_used: QueryPlan
    execution_time_ms: float
    metadata: Dict[str, Any] = field(default_factory=dict)
