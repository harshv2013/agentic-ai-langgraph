"""
Research Agent with Multi-Step Reasoning

This example demonstrates a more advanced agent that can:
1. Break down research tasks into steps
2. Search for information
3. Analyze findings
4. Make follow-up searches
5. Synthesize a comprehensive answer

The agent can loop through multiple search-analyze cycles to gather complete information.
"""

import os
from typing import TypedDict, Annotated, Sequence
import operator
from dotenv import load_dotenv

from langchain_openai import AzureChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

# Load environment variables
load_dotenv()

# Initialize Azure OpenAI with higher temperature for more creative research
llm = AzureChatOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    temperature=0.3,
)


# Mock search tool (replace with real API like Tavily if you have a key)
@tool
def web_search(query: str) -> str:
    """
    Search the web for information.
    
    Args:
        query: The search query
        
    Returns:
        Search results as a string
    """
    # This is a mock implementation
    # In production, use real search APIs like:
    # - Tavily (https://tavily.com)
    # - Serper (https://serper.dev)
    # - Google Custom Search
    
    mock_results = {
        "langgraph": """
        LangGraph is a library for building stateful, multi-actor applications with LLMs.
        Key features:
        - Cycles and Branching: Complex agent workflows with loops
        - Persistence: Built-in state management
        - Human-in-the-Loop: Pause and resume execution
        - Streaming: Real-time output
        Released by LangChain in 2024.
        """,
        "azure openai": """
        Azure OpenAI Service provides REST API access to OpenAI's models including:
        - GPT-4 and GPT-3.5-Turbo for text generation
        - DALL-E for image generation
        - Whisper for speech-to-text
        Key benefits:
        - Enterprise-grade security and compliance
        - Regional availability
        - Integration with Azure services
        - Content filtering and responsible AI features
        """,
        "agentic ai": """
        Agentic AI refers to autonomous systems that can:
        - Plan sequences of actions
        - Use tools to interact with environments
        - Adapt based on feedback
        - Maintain state across interactions
        
        Key patterns:
        - ReAct (Reasoning + Acting)
        - Plan-and-Execute
        - Reflection and self-correction
        
        Applications: research assistants, coding agents, task automation
        """,
        "default": """
        Search results for: {query}
        
        Multiple relevant sources found. Key points:
        1. Recent developments in the field
        2. Technical implementations and best practices
        3. Real-world applications and case studies
        4. Expert opinions and analysis
        
        For specific information, please refine your search query.
        """
    }
    
    # Simple keyword matching for mock results
    query_lower = query.lower()
    for key, result in mock_results.items():
        if key in query_lower and key != "default":
            print(f"\n🔍 Searching: '{query}'")
            print(f"✓ Found relevant information")
            return result.strip()
    
    print(f"\n🔍 Searching: '{query}'")
    print(f"✓ Found general information")
    return mock_results["default"].format(query=query)


@tool
def analyze_content(content: str, focus: str) -> str:
    """
    Analyze content with a specific focus.
    
    Args:
        content: The content to analyze
        focus: What aspect to focus on (e.g., "technical details", "benefits", "limitations")
        
    Returns:
        Analysis results
    """
    print(f"\n📊 Analyzing content with focus: '{focus}'")
    
    # In a real implementation, this could use another LLM call or specialized analysis
    analysis = f"""
    Analysis focusing on: {focus}
    
    Based on the provided content:
    - Key insights extracted based on the focus area
    - Relevant patterns and themes identified
    - Important details highlighted for the research question
    
    (Note: This is a simplified mock analysis. In production, this would perform deeper analysis)
    """
    return analysis.strip()


# Create tools list and bind to LLM
tools = [web_search, analyze_content]
llm_with_tools = llm.bind_tools(tools)


# Define enhanced state with metadata
class ResearchState(TypedDict):
    """State for research agent with tracking"""
    messages: Annotated[Sequence[BaseMessage], operator.add]
    search_count: int  # Track number of searches performed
    max_searches: int  # Limit searches to prevent infinite loops


# System prompt for the research agent
RESEARCH_SYSTEM_PROMPT = """You are a research assistant that helps users find and synthesize information.

Your approach:
1. Break down complex questions into researchable components
2. Use web_search to find relevant information
3. Optionally use analyze_content to extract specific insights
4. Synthesize findings into a comprehensive answer

Guidelines:
- Be thorough but efficient with searches
- Cite that information came from searches
- If you find sufficient information, provide a complete answer
- If information is incomplete, make targeted follow-up searches
- Limit yourself to 3-4 searches per query to stay focused

Provide clear, well-organized answers based on your research."""


def research_agent_node(state: ResearchState):
    """
    Research agent that decides on next actions.
    """
    print("\n--- RESEARCH AGENT REASONING ---")
    
    # Add system prompt if this is the first message
    messages = state["messages"]
    if not any(isinstance(m, SystemMessage) for m in messages):
        messages = [SystemMessage(content=RESEARCH_SYSTEM_PROMPT)] + messages
    
    search_count = state.get("search_count", 0)
    max_searches = state.get("max_searches", 3)
    
    print(f"Searches performed: {search_count}/{max_searches}")
    
    # Check if we've hit search limit
    if search_count >= max_searches:
        print("⚠️  Search limit reached, agent will synthesize findings")
        # Force the agent to provide final answer by not allowing more tool calls
        response = llm.invoke(messages + [SystemMessage(
            content="You have completed your research. Now provide a comprehensive final answer based on all the information gathered."
        )])
    else:
        response = llm_with_tools.invoke(messages)
    
    # Log agent decision
    if hasattr(response, 'tool_calls') and response.tool_calls:
        print(f"Agent decided to use {len(response.tool_calls)} tool(s):")
        for tc in response.tool_calls:
            print(f"  - {tc['name']}")
    else:
        print("Agent providing final answer")
    
    return {"messages": [response]}


def should_continue_research(state: ResearchState):
    """
    Decide whether to continue researching or end.
    """
    messages = state["messages"]
    last_message = messages[-1]
    search_count = state.get("search_count", 0)
    max_searches = state.get("max_searches", 3)
    
    # Check for tool calls and search limit
    has_tool_calls = hasattr(last_message, 'tool_calls') and last_message.tool_calls
    within_limit = search_count < max_searches
    
    if has_tool_calls and within_limit:
        return "continue"
    return "end"


def track_searches(state: ResearchState):
    """
    Update search count after tool execution.
    """
    search_count = state.get("search_count", 0)
    messages = state["messages"]
    
    # Count search tool calls in the last message
    if messages:
        last_message = messages[-2] if len(messages) >= 2 else None  # Check message before tool results
        if last_message and hasattr(last_message, 'tool_calls'):
            new_searches = sum(1 for tc in last_message.tool_calls if tc['name'] == 'web_search')
            search_count += new_searches
    
    return {"search_count": search_count}


def create_research_agent():
    """
    Create the research agent workflow.
    
    Graph structure:
        START → agent → tools → tracker → agent → ... → END
    """
    workflow = StateGraph(ResearchState)
    
    # Add nodes
    workflow.add_node("agent", research_agent_node)
    workflow.add_node("tools", ToolNode(tools))
    workflow.add_node("tracker", track_searches)
    
    # Set entry point
    workflow.set_entry_point("agent")
    
    # Add conditional edges
    workflow.add_conditional_edges(
        "agent",
        should_continue_research,
        {
            "continue": "tools",
            "end": END
        }
    )
    
    # Tools → tracker → agent (creates the research loop)
    workflow.add_edge("tools", "tracker")
    workflow.add_edge("tracker", "agent")
    
    return workflow.compile()


def run_research(query: str, max_searches: int = 3):
    """
    Run a research query.
    """
    print("\n" + "=" * 70)
    print(f"📚 RESEARCH QUERY: {query}")
    print("=" * 70)
    
    app = create_research_agent()
    
    initial_state = {
        "messages": [HumanMessage(content=query)],
        "search_count": 0,
        "max_searches": max_searches
    }
    
    result = app.invoke(initial_state)
    
    print("\n" + "=" * 70)
    print("📝 RESEARCH FINDINGS:")
    print("=" * 70)
    print(result["messages"][-1].content)
    print(f"\nTotal searches performed: {result.get('search_count', 0)}")
    print("\n")


def main():
    """
    Run research examples.
    """
    print("\n" + "🤖 AGENTIC AI DEMO - Research Agent" + "\n")
    
    # Example 1: Single focused topic
    run_research("What is LangGraph and what are its key features?", max_searches=2)
    
    # Example 2: Comparative research
    run_research(
        "Compare the benefits of using Azure OpenAI versus standard OpenAI API for enterprise applications",
        max_searches=3
    )
    
    # Example 3: Multi-faceted research
    run_research(
        "Explain agentic AI, its key patterns, and how it differs from traditional chatbots",
        max_searches=3
    )


if __name__ == "__main__":
    main()
