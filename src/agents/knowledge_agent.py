"""
Knowledge Agent for multi-turn conversation and LLM integration.
"""

from typing import Optional, List
from dataclasses import dataclass, field
from datetime import datetime

from ..navigator import PersonalKnowledgeNavigator
from ..models import UserContext, GroundedAnswer, Citation
from ..utils.logging import get_logger

logger = get_logger("agent")

@dataclass
class AgentConfig:
    agent_name: str = "Knowledge Assistant"
    model: str = "gpt-4"
    max_sources: int = 5
    temperature: float = 0.7
    system_prompt: str = "You are a helpful knowledge assistant that provides accurate, cited answers."

@dataclass
class AgentResponse:
    answer: str
    reasoning: str
    citations: List[Citation]
    confidence_score: float
    hallucination_risk: str
    execution_time_ms: float
    metadata: dict = field(default_factory=dict)

class KnowledgeAgent:
    def __init__(self, navigator: PersonalKnowledgeNavigator, config: Optional[AgentConfig] = None):
        self.navigator = navigator
        self.config = config or AgentConfig()
        self.conversation_history: List[dict] = []
    
    async def answer_question(self, question: str, user_context: UserContext) -> AgentResponse:
        """Answer a question with reasoning trace."""
        import time
        start = time.time()
        
        # Get grounded answer from navigator
        grounded = await self.navigator.query(question, user_context, self.config.max_sources)
        
        # Generate reasoning
        reasoning = f"I searched {len(grounded.sources_used)} source(s) and found {len(grounded.citations)} relevant documents. "
        if grounded.citations:
            top_doc = grounded.citations[0].document_title
            reasoning += f"The most relevant source was '{top_doc}' with {grounded.citations[0].confidence_score:.0%} confidence. "
        reasoning += f"Overall confidence: {grounded.confidence_score:.0%}. Hallucination risk: {grounded.hallucination_risk}."
        
        # Store conversation
        self.conversation_history.append({
            "question": question,
            "answer": grounded.answer,
            "timestamp": datetime.utcnow().isoformat(),
            "user_id": user_context.user_id
        })
        
        execution_time = (time.time() - start) * 1000
        
        return AgentResponse(
            answer=grounded.answer,
            reasoning=reasoning,
            citations=grounded.citations,
            confidence_score=grounded.confidence_score,
            hallucination_risk=grounded.hallucination_risk,
            execution_time_ms=execution_time
        )
    
    def clear_history(self):
        """Clear conversation history."""
        self.conversation_history = []
