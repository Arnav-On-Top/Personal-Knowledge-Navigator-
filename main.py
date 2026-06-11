"""
Main entry point and API server for Personal Knowledge Navigator.
Run this to start the application server.
"""

import asyncio
import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from pydantic import BaseModel

from src.navigator import PersonalKnowledgeNavigator
from src.models import UserContext, Role, GroundedAnswer, Citation
from src.agents import KnowledgeAgent, AgentConfig
from src.config import get_config
from src.utils import get_logger

# Initialize logger
logger = get_logger("api")

# Create FastAPI app
app = FastAPI(
    title="Personal Knowledge Navigator API",
    description="Enterprise-grade agentic knowledge retrieval system",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global navigator instance
navigator: Optional[PersonalKnowledgeNavigator] = None
agent: Optional[KnowledgeAgent] = None


# Request/Response Models
class UserRequest(BaseModel):
    """User context for API requests."""
    user_id: str
    roles: List[str] = ["viewer"]
    organization: str = "default"


class QueryRequest(BaseModel):
    """Knowledge query request."""
    question: str
    user: UserRequest
    top_k: int = 5


class CitationResponse(BaseModel):
    """Citation information."""
    source_id: str
    source_name: str
    document_id: str
    document_title: str
    relevant_text: str
    relevance_score: float
    confidence_score: float


class AnswerResponse(BaseModel):
    """Answer with citations."""
    answer: str
    citations: List[CitationResponse]
    confidence_score: float
    hallucination_risk: str
    sources_used: List[str]


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    sources_connected: int
    version: str


class SourceInfo(BaseModel):
    """Information about a connected source."""
    source_id: str
    source_name: str
    source_type: str
    is_connected: bool


# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    """Initialize navigator on startup."""
    global navigator, agent
    try:
        logger.info("Initializing Personal Knowledge Navigator...")
        navigator = PersonalKnowledgeNavigator()
        
        # Initialize data sources
        initialized = await navigator.initialize()
        
        if initialized:
            logger.info("✅ Navigator initialized successfully")
        else:
            logger.warning("⚠️  Navigator initialized with some issues")
        
        # Create agent
        agent_config = AgentConfig(
            agent_name="Enterprise Knowledge Assistant",
            model="gpt-4",
            max_sources=5
        )
        agent = KnowledgeAgent(navigator, agent_config)
        
        logger.info("✅ Application ready to serve requests")
    except Exception as e:
        logger.error(f"❌ Startup error: {e}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    global navigator
    if navigator:
        try:
            await navigator.shutdown()
            logger.info("✅ Navigator shutdown gracefully")
        except Exception as e:
            logger.error(f"Shutdown error: {e}")


# Helper functions
def create_user_context(user_req: UserRequest) -> UserContext:
    """Convert API request to UserContext."""
    role_map = {
        "admin": Role.ADMIN,
        "editor": Role.EDITOR,
        "analyst": Role.ANALYST,
        "viewer": Role.VIEWER,
    }
    
    roles = [role_map.get(r, Role.VIEWER) for r in user_req.roles]
    
    return UserContext(
        user_id=user_req.user_id,
        roles=roles,
        organization=user_req.organization
    )


def citation_to_response(citation: Citation) -> CitationResponse:
    """Convert Citation to API response."""
    return CitationResponse(
        source_id=citation.source_id,
        source_name=citation.source_name,
        document_id=citation.document_id,
        document_title=citation.document_title,
        relevant_text=citation.relevant_text,
        relevance_score=citation.relevance_score,
        confidence_score=citation.confidence_score
    )


# API Endpoints

@app.get("/", tags=["Info"])
async def root():
    """Root endpoint with API information."""
    return {
        "name": "Personal Knowledge Navigator API",
        "version": "1.0.0",
        "description": "Enterprise-grade agentic knowledge retrieval system",
        "documentation": "/docs",
        "endpoints": {
            "health": "GET /health",
            "query": "POST /query",
            "sources": "GET /sources",
            "history": "GET /history"
        }
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Check API and navigator health."""
    if not navigator:
        raise HTTPException(status_code=503, detail="Navigator not initialized")
    
    sources_info = navigator.get_sources_info()
    connected_count = sum(1 for s in sources_info if s["is_connected"])
    
    return HealthResponse(
        status="healthy",
        sources_connected=connected_count,
        version="1.0.0"
    )


@app.get("/sources", response_model=List[SourceInfo], tags=["Sources"])
async def get_sources():
    """Get information about connected sources."""
    if not navigator:
        raise HTTPException(status_code=503, detail="Navigator not initialized")
    
    sources = navigator.get_sources_info()
    return [
        SourceInfo(
            source_id=s["source_id"],
            source_name=s["source_name"],
            source_type=s["source_type"],
            is_connected=s["is_connected"]
        )
        for s in sources
    ]


@app.post("/query", response_model=AnswerResponse, tags=["Query"])
async def query_knowledge(request: QueryRequest):
    """
    Query the knowledge base with a natural language question.
    Returns grounded answer with citations and confidence scores.
    
    **Foundry IQ Principles:**
    - Connects to multiple enterprise sources
    - Enforces user permissions
    - Retrieves relevant knowledge
    - Delivers cited, grounded answers
    - Reduces hallucinations through confidence assessment
    """
    if not navigator:
        raise HTTPException(status_code=503, detail="Navigator not initialized")
    
    try:
        # Create user context
        user_context = create_user_context(request.user)
        
        logger.info(f"Query from {user_context.user_id}: {request.question}")
        
        # Query knowledge base
        grounded_answer = await navigator.query(
            question=request.question,
            user_context=user_context,
            top_k=request.top_k
        )
        
        # Convert response
        return AnswerResponse(
            answer=grounded_answer.answer,
            citations=[citation_to_response(c) for c in grounded_answer.citations],
            confidence_score=grounded_answer.confidence_score,
            hallucination_risk=grounded_answer.hallucination_risk,
            sources_used=grounded_answer.sources_used
        )
    
    except Exception as e:
        logger.error(f"Query error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/agent/chat", tags=["Agent"])
async def agent_chat(request: QueryRequest):
    """
    Chat with the knowledge agent.
    Supports multi-turn conversation with reasoning.
    """
    if not agent:
        raise HTTPException(status_code=503, detail="Agent not initialized")
    
    try:
        user_context = create_user_context(request.user)
        
        logger.info(f"Agent chat from {user_context.user_id}: {request.question}")
        
        # Get agent response
        agent_response = await agent.answer_question(
            question=request.question,
            user_context=user_context
        )
        
        return {
            "answer": agent_response.answer,
            "reasoning": agent_response.reasoning,
            "citations": [citation_to_response(c) for c in agent_response.citations],
            "confidence_score": agent_response.confidence_score,
            "hallucination_risk": agent_response.hallucination_risk,
            "execution_time_ms": agent_response.execution_time_ms
        }
    
    except Exception as e:
        logger.error(f"Agent chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/history", tags=["History"])
async def get_query_history():
    """Get query history for auditing."""
    if not navigator:
        raise HTTPException(status_code=503, detail="Navigator not initialized")
    
    history = navigator.get_query_history()
    return {
        "total_queries": len(history),
        "history": history[-10:]  # Return last 10 queries
    }


@app.get("/permissions/check", tags=["Permissions"])
async def check_permission(user_id: str, role: str, resource: str):
    """Check if user has permission for resource."""
    if not navigator:
        raise HTTPException(status_code=503, detail="Navigator not initialized")
    
    try:
        role_map = {
            "admin": Role.ADMIN,
            "editor": Role.EDITOR,
            "analyst": Role.ANALYST,
            "viewer": Role.VIEWER,
        }
        
        user_context = UserContext(
            user_id=user_id,
            roles=[role_map.get(role, Role.VIEWER)],
            organization="default"
        )
        
        has_access = navigator.permission_enforcer.enforce_access(
            user_context, resource
        )
        
        return {
            "user_id": user_id,
            "role": role,
            "resource": resource,
            "has_access": has_access
        }
    
    except Exception as e:
        logger.error(f"Permission check error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Error handlers
@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions."""
    logger.error(f"Unhandled exception: {exc}")
    return {
        "error": "Internal server error",
        "detail": str(exc)
    }


if __name__ == "__main__":
    config = get_config()
    host = config.get("API_HOST", "0.0.0.0")
    port = int(config.get("API_PORT", 8000))
    debug = config.is_debug()
    
    logger.info(f"Starting Personal Knowledge Navigator API on {host}:{port}")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=debug,
        log_level="info"
    )
