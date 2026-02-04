"""
Agent Flow Visualizer

This script helps visualize the flow of agentic AI systems using ASCII diagrams.
It explains the key components and execution patterns.
"""


def print_simple_agent_flow():
    """Visualize the simple agent flow."""
    print("\n" + "=" * 70)
    print("SIMPLE AGENT FLOW")
    print("=" * 70)
    
    diagram = """
    ┌─────────────────────────────────────────────────────────────┐
    │                        START                                │
    └────────────────────────┬────────────────────────────────────┘
                             │
                             │ User Query: "What is 45 * 67?"
                             ▼
    ┌─────────────────────────────────────────────────────────────┐
    │                    AGENT NODE                               │
    │  • Receives query and conversation history                  │
    │  • LLM analyzes what needs to be done                       │
    │  • Decides: use tools OR provide answer                     │
    └────────────────────────┬────────────────────────────────────┘
                             │
                             │ Decision: "Need calculator"
                             ▼
    ┌─────────────────────────────────────────────────────────────┐
    │                 CONDITIONAL ROUTING                         │
    │  • Check if agent wants to use tools                        │
    │  • Route to tools node OR end                               │
    └────────────┬───────────────────────────┬────────────────────┘
                 │                           │
      Has tool calls                    No tool calls
                 │                           │
                 ▼                           ▼
    ┌─────────────────────────┐   ┌──────────────────────┐
    │      TOOL NODE          │   │        END           │
    │  • Execute calculator   │   │  Return final answer │
    │  • Return results       │   └──────────────────────┘
    └────────────┬────────────┘
                 │
                 │ Result: "3015"
                 ▼
    ┌─────────────────────────────────────────────────────────────┐
    │                    AGENT NODE                               │
    │  • Receives tool results                                    │
    │  • LLM processes the calculation                            │
    │  • Formulates final answer                                  │
    └────────────────────────┬────────────────────────────────────┘
                             │
                             │ Decision: "Have answer"
                             ▼
    ┌─────────────────────────────────────────────────────────────┐
    │                         END                                 │
    │              "The result is 3015"                           │
    └─────────────────────────────────────────────────────────────┘
    
    KEY CONCEPTS:
    
    1. AGENT LOOP: The agent can cycle multiple times through:
       Agent → Tools → Agent → Tools ... until satisfied
    
    2. STATE MANAGEMENT: Each node receives and updates the state:
       - Messages (conversation history)
       - Tool call results
       - Any custom metadata
    
    3. CONDITIONAL ROUTING: The should_continue() function decides:
       if last_message.tool_calls exist → go to tools
       else → end the graph
    """
    print(diagram)


def print_research_agent_flow():
    """Visualize the research agent flow."""
    print("\n" + "=" * 70)
    print("RESEARCH AGENT FLOW (with iteration tracking)")
    print("=" * 70)
    
    diagram = """
    ┌─────────────────────────────────────────────────────────────┐
    │                        START                                │
    │              Query: "Explain LangGraph"                     │
    │            State: { search_count: 0 }                       │
    └────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
    ┌─────────────────────────────────────────────────────────────┐
    │                   AGENT NODE                                │
    │  • Check search_count vs max_searches                       │
    │  • Decide on research strategy                              │
    │  • Choose tools to gather info                              │
    └────────────────────────┬────────────────────────────────────┘
                             │
                             │ Decision: "Search for LangGraph info"
                             ▼
    ┌─────────────────────────────────────────────────────────────┐
    │                  TOOL NODE                                  │
    │  • Execute web_search("LangGraph")                          │
    │  • Return search results                                    │
    └────────────────────────┬────────────────────────────────────┘
                             │
                             │ Results received
                             ▼
    ┌─────────────────────────────────────────────────────────────┐
    │                 TRACKER NODE                                │
    │  • Increment search_count: 0 → 1                            │
    │  • Update state metadata                                    │
    └────────────────────────┬────────────────────────────────────┘
                             │
                             │ State: { search_count: 1 }
                             ▼
    ┌─────────────────────────────────────────────────────────────┐
    │                   AGENT NODE                                │
    │  • Review search results                                    │
    │  • Assess if more info needed                               │
    │  • Decide next action                                       │
    └────────────────────────┬────────────────────────────────────┘
                             │
                             │ Decision: "Need info on key features"
                             ▼
                 ┌───────────┴───────────┐
                 │                       │
           Still researching       Have enough info
                 │                       │
                 ▼                       ▼
    ┌──────────────────────┐   ┌──────────────────────┐
    │    TOOL NODE         │   │        END           │
    │  More searches...    │   │  Final synthesis     │
    └──────────┬───────────┘   └──────────────────────┘
               │
               │ LOOP CONTINUES
               └────► TRACKER → AGENT → ...
    
    MAX ITERATIONS PROTECTION:
    
    if search_count >= max_searches:
        Force agent to synthesize and end
        (Prevents infinite research loops)
    
    ADVANTAGES:
    • Multi-step reasoning
    • Iterative refinement
    • Controlled exploration
    • Prevents runaway costs
    """
    print(diagram)


def print_memory_agent_flow():
    """Visualize the agent with memory flow."""
    print("\n" + "=" * 70)
    print("AGENT WITH MEMORY FLOW (using checkpointing)")
    print("=" * 70)
    
    diagram = """
    ┌─────────────────────────────────────────────────────────────┐
    │                    CONVERSATION 1                           │
    │               User: "Hi, I'm Alex"                          │
    └────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
    ┌─────────────────────────────────────────────────────────────┐
    │                   AGENT NODE                                │
    │  System Prompt: "You are a helpful assistant with memory"  │
    │  • Understand user shared their name                        │
    │  • Use save_user_preference tool                            │
    └────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
    ┌─────────────────────────────────────────────────────────────┐
    │                   TOOL NODE                                 │
    │  save_user_preference("name", "Alex")                       │
    └────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
    ┌─────────────────────────────────────────────────────────────┐
    │                UPDATE CONTEXT NODE                          │
    │  Extract and store: user_name = "Alex"                      │
    │  State: { user_name: "Alex", messages: [...] }              │
    └────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
    ┌─────────────────────────────────────────────────────────────┐
    │                   CHECKPOINT                                │
    │  💾 Save state with thread_id = "conversation-1"            │
    │     { user_name: "Alex", messages: [HumanMessage(...),      │
    │       AIMessage(...)] }                                     │
    └─────────────────────────────────────────────────────────────┘
    
    
    ┌─────────────────────────────────────────────────────────────┐
    │                    CONVERSATION 2                           │
    │          User: "What's my name?"                            │
    └────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
    ┌─────────────────────────────────────────────────────────────┐
    │                   LOAD CHECKPOINT                           │
    │  📂 Load state for thread_id = "conversation-1"             │
    │     Retrieved: { user_name: "Alex", messages: [...] }       │
    └────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
    ┌─────────────────────────────────────────────────────────────┐
    │                   AGENT NODE                                │
    │  • Has access to user_name from state                       │
    │  • Can reference previous messages                          │
    │  • Provides personalized response                           │
    │  Response: "Your name is Alex!"                             │
    └─────────────────────────────────────────────────────────────┘
    
    KEY FEATURES:
    
    1. CHECKPOINTING:
       • State is saved after each interaction
       • Identified by thread_id
       • Can resume from any point
    
    2. STATE ENRICHMENT:
       • Custom fields (user_name, preferences, etc.)
       • Automatically passed between nodes
       • Persistent across sessions
    
    3. CONTEXT AWARENESS:
       • Agent has full conversation history
       • Can reference earlier topics
       • Personalizes responses
    
    4. MEMORY TYPES:
       • Short-term: Current conversation (messages)
       • Long-term: Extracted facts (user_name, etc.)
       • Episodic: Full conversation history
    """
    print(diagram)


def print_state_structure():
    """Explain the state structure."""
    print("\n" + "=" * 70)
    print("STATE STRUCTURE IN LANGGRAPH")
    print("=" * 70)
    
    explanation = """
    STATE is the core data structure that flows through your graph.
    
    ┌─────────────────────────────────────────────────────────────┐
    │                      TYPED STATE                            │
    │                                                             │
    │  class AgentState(TypedDict):                               │
    │      messages: Annotated[Sequence[BaseMessage], add]        │
    │      search_count: int                                      │
    │      user_name: str                                         │
    │      custom_data: Dict[str, Any]                            │
    │                                                             │
    └─────────────────────────────────────────────────────────────┘
    
    STATE ANNOTATIONS:
    
    • Annotated[Sequence[BaseMessage], operator.add]
      → Messages are APPENDED to existing messages
      → Maintains conversation history automatically
    
    • Regular fields (int, str, dict)
      → Updated with latest value (overwrite)
      → Used for metadata, counters, flags
    
    
    STATE FLOW EXAMPLE:
    
    Initial State:
    {
        "messages": [HumanMessage("Hello")],
        "search_count": 0
    }
    
    After Agent Node:
    {
        "messages": [
            HumanMessage("Hello"),
            AIMessage("Hi! How can I help?", tool_calls=[...])
        ],
        "search_count": 0
    }
    
    After Tool Node:
    {
        "messages": [
            HumanMessage("Hello"),
            AIMessage("Hi! How can I help?", tool_calls=[...]),
            ToolMessage("Result: ...")
        ],
        "search_count": 0
    }
    
    After Tracker Node:
    {
        "messages": [...],  # Unchanged
        "search_count": 1   # Updated
    }
    
    
    WHY THIS MATTERS:
    
    ✓ Each node receives FULL state
    ✓ Each node returns PARTIAL state (only updates)
    ✓ State updates are merged automatically
    ✓ Type safety helps catch errors
    ✓ Makes agent behavior predictable
    """
    print(explanation)


def print_tool_calling_pattern():
    """Explain the tool calling pattern."""
    print("\n" + "=" * 70)
    print("TOOL CALLING PATTERN")
    print("=" * 70)
    
    explanation = """
    HOW AGENTS DECIDE TO USE TOOLS:
    
    ┌─────────────────────────────────────────────────────────────┐
    │  1. LLM receives messages + tool definitions                │
    │                                                             │
    │     llm_with_tools = llm.bind_tools([calculator, search])   │
    │                                                             │
    │  2. LLM returns one of:                                     │
    │     a) Regular text response (no tools needed)              │
    │     b) Tool calls (structured function calls)               │
    │                                                             │
    │  3. If tool calls present:                                  │
    │     • Extract tool name and arguments                       │
    │     • Execute the actual function                           │
    │     • Return results to LLM                                 │
    │                                                             │
    │  4. LLM processes tool results:                             │
    │     • May call more tools (iterative)                       │
    │     • Or provide final answer                               │
    └─────────────────────────────────────────────────────────────┘
    
    
    EXAMPLE TOOL CALL:
    
    User: "What is 123 * 456?"
    
    Agent Response:
    {
        "type": "ai",
        "content": "",
        "tool_calls": [
            {
                "name": "calculator",
                "args": {"expression": "123 * 456"},
                "id": "call_abc123"
            }
        ]
    }
    
    Tool Execution:
    result = calculator(expression="123 * 456")
    # Returns: "The result is: 56088"
    
    Tool Result Message:
    {
        "type": "tool",
        "content": "The result is: 56088",
        "tool_call_id": "call_abc123"
    }
    
    Agent Final Response:
    {
        "type": "ai",
        "content": "123 multiplied by 456 equals 56,088."
    }
    
    
    MULTI-TOOL CALLS:
    
    User: "Calculate 5+5 and search for Python tutorials"
    
    Agent can return MULTIPLE tool calls in one response:
    {
        "tool_calls": [
            {"name": "calculator", "args": {"expression": "5+5"}},
            {"name": "web_search", "args": {"query": "Python tutorials"}}
        ]
    }
    
    These execute in PARALLEL or SEQUENCE depending on your graph setup!
    """
    print(explanation)


def main():
    """Display all visualizations."""
    print("\n" + "🎨 AGENTIC AI FLOW VISUALIZATIONS" + "\n")
    
    visualizations = [
        ("Simple Agent", print_simple_agent_flow),
        ("Research Agent", print_research_agent_flow),
        ("Agent with Memory", print_memory_agent_flow),
        ("State Structure", print_state_structure),
        ("Tool Calling Pattern", print_tool_calling_pattern),
    ]
    
    print("Available visualizations:")
    for i, (name, _) in enumerate(visualizations, 1):
        print(f"{i}. {name}")
    print(f"{len(visualizations) + 1}. Show all")
    
    choice = input("\nSelect visualization (1-6): ").strip()
    
    try:
        choice_num = int(choice)
        if choice_num == len(visualizations) + 1:
            for _, func in visualizations:
                func()
                input("\nPress Enter for next visualization...")
        elif 1 <= choice_num <= len(visualizations):
            visualizations[choice_num - 1][1]()
        else:
            print("Invalid choice, showing all...")
            for _, func in visualizations:
                func()
                input("\nPress Enter for next visualization...")
    except ValueError:
        print("Invalid input, showing all...")
        for _, func in visualizations:
            func()
            input("\nPress Enter for next visualization...")


if __name__ == "__main__":
    main()
