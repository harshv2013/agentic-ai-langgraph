"""
Simple Agent Example with Calculator Tool

This example demonstrates the basic flow of an agentic AI system:
1. Agent receives a query
2. Agent decides if it needs tools
3. Agent calls tools if needed
4. Agent processes results
5. Agent provides final answer

The agent will loop through steps 2-4 until it has enough information to answer.
"""

import os
from typing import TypedDict, Annotated, Sequence
import operator
from dotenv import load_dotenv

from langchain_openai import AzureChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

# Load environment variables
load_dotenv()

# Initialize Azure OpenAI
llm = AzureChatOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    temperature=0,
)

# Define tools
@tool
def calculator(expression: str) -> str:
    """
    Evaluate a mathematical expression. 
    Use this for any math calculations.
    
    Args:
        expression: A mathematical expression as a string (e.g., "2 + 2", "10 * 5 + 3")
    
    Returns:
        The result of the calculation
    """
    try:
        # Safety: only allow basic math operations
        allowed_chars = set("0123456789+-*/(). ")
        if not all(c in allowed_chars for c in expression):
            return "Error: Expression contains invalid characters"
        
        result = eval(expression)
        return f"The result is: {result}"
    except Exception as e:
        return f"Error calculating: {str(e)}"

@tool
def get_word_length(word: str) -> str:
    """
    Get the length of a word.
    
    Args:
        word: The word to measure
        
    Returns:
        The number of characters in the word
    """
    return f"The word '{word}' has {len(word)} characters"


# Bind tools to the LLM
tools = [calculator, get_word_length]
llm_with_tools = llm.bind_tools(tools)


# Define the state
class AgentState(TypedDict):
    """State that flows through the agent graph"""
    messages: Annotated[Sequence[BaseMessage], operator.add]


# Define the agent node
def agent_node(state: AgentState):
    """
    The agent reasoning node. This is where the LLM:
    1. Analyzes the current state
    2. Decides whether to use tools or provide an answer
    3. Returns the decision
    """
    print("\n--- AGENT REASONING ---")
    messages = state["messages"]
    print(f"Processing {len(messages)} messages")
    
    # Call LLM with tools
    response = llm_with_tools.invoke(messages)
    
    # Print what the agent decided
    if response.tool_calls:
        print(f"Agent decided to call {len(response.tool_calls)} tool(s)")
        for tool_call in response.tool_calls:
            print(f"  - {tool_call['name']} with args: {tool_call['args']}")
    else:
        print("Agent decided to provide final answer")
    
    return {"messages": [response]}


# Define conditional routing function
def should_continue(state: AgentState):
    """
    Determine if the agent should continue to tools or end.
    
    This is the key decision point that creates the agentic loop.
    """
    messages = state["messages"]
    last_message = messages[-1]
    
    # If the LLM makes a tool call, route to tools
    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        return "continue"
    # Otherwise, end the graph
    return "end"


# Build the graph
def create_agent_graph():
    """
    Create the agent workflow graph.
    
    Graph structure:
        START → agent → tools → agent → ... → END
                  ↓                       ↓
                 END                    END
    """
    # Initialize the graph
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", ToolNode(tools))
    
    # Set entry point
    workflow.set_entry_point("agent")
    
    # Add conditional edges from agent
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "continue": "tools",  # If tools are needed, go to tools node
            "end": END           # If done, end the graph
        }
    )
    
    # Add edge from tools back to agent
    # This creates the loop: agent → tools → agent
    workflow.add_edge("tools", "agent")
    
    # Compile the graph
    return workflow.compile()


def run_agent(query: str):
    """
    Run the agent with a query and print the execution flow.
    """
    print("=" * 60)
    print(f"QUERY: {query}")
    print("=" * 60)
    
    app = create_agent_graph()
    
    # Initial state
    initial_state = {
        "messages": [HumanMessage(content=query)]
    }
    
    # Run the agent
    result = app.invoke(initial_state)
    
    # Print final answer
    print("\n" + "=" * 60)
    print("FINAL ANSWER:")
    print("=" * 60)
    final_message = result["messages"][-1]
    print(final_message.content)
    print("\n")
    
    return result


def main():
    """
    Run example queries to demonstrate agent flow.
    """
    print("\n" + "🤖 AGENTIC AI DEMO - Simple Agent with Tools" + "\n")
    
    # Example 1: Requires calculator tool
    run_agent("What is 45 * 67 + 123?")
    
    # Example 2: Requires multiple tool calls
    run_agent("Calculate (15 + 25) * 3, and also tell me how long the word 'artificial' is")
    
    # Example 3: No tools needed
    run_agent("What is the capital of France?")
    
    # Example 4: Complex reasoning with tools
    run_agent("If I have 5 apples and buy 3 more, then give away 2, how many do I have? Also, how many letters are in 'mathematics'?")


if __name__ == "__main__":
    main()
