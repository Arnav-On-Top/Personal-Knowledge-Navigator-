"""
Example: Basic query usage of Personal Knowledge Navigator.
Demonstrates Foundry IQ principles in action.
"""

import asyncio
from src.navigator import PersonalKnowledgeNavigator
from src.models import UserContext, Role


async def main():
    """Run basic query example."""
    
    # Initialize navigator
    navigator = PersonalKnowledgeNavigator()
    
    try:
        # Initialize data sources
        await navigator.initialize()
        
        # Create user context with permissions
        user_context = UserContext(
            user_id="user123",
            roles=[Role.ANALYST, Role.VIEWER],
            organization="engineering",
            attributes={
                "department": "data-science",
                "level": "senior"
            }
        )
        
        # Example queries
        queries = [
            "What are the latest architecture decisions?",
            "What metrics should we track for API performance?",
            "How do we handle authentication across services?",
        ]
        
        print("=" * 60)
        print("Personal Knowledge Navigator - Basic Query Example")
        print("=" * 60)
        print()
        
        for query in queries:
            print(f"Query: {query}")
            print("-" * 60)
            
            # Query knowledge base
            response = await navigator.query(
                question=query,
                user_context=user_context,
                top_k=3
            )
            
            # Display answer with citations
            print(f"\nAnswer:\n{response.answer}\n")
            
            print(f"Confidence: {response.confidence_score:.1%}")
            print(f"Hallucination Risk: {response.hallucination_risk}")
            print(f"Sources Used: {', '.join(response.sources_used)}\n")
            
            if response.citations:
                print("Top Citations:")
                for i, citation in enumerate(response.top_citations(3), 1):
                    print(f"  {i}. {citation.document_title}")
                    print(f"     Confidence: {citation.confidence_score:.1%}")
            
            print("\n" + "=" * 60 + "\n")
        
        # Display source information
        print("Connected Sources:")
        for source_info in navigator.get_sources_info():
            print(f"  - {source_info['source_name']}: {source_info['source_type']}")
        
        print("\nQuery Statistics:")
        history = navigator.get_query_history()
        print(f"  Total Queries: {len(history)}")
        
        if history:
            avg_confidence = sum(h['confidence_score'] for h in history) / len(history)
            print(f"  Avg Confidence: {avg_confidence:.1%}")
    
    finally:
        await navigator.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
