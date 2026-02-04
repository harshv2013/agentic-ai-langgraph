"""
Agent with Memory and Conversation History

This example demonstrates:
1. Maintaining conversation state across multiple turns
2. Using checkpointing to save and resume conversations
3. Referencing previous context
4. Personalized interactions based on conversation history

The agent "remembers" what was discussed earlier in the conversation.
"""

import os
from typing import TypedDict, Annotated, Sequence
import operator
from dotenv import load_dotenv

from langchain_openai import AzureChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage, AIMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver

# Load environment variables
load_dotenv()

# Initialize Azure OpenAI
llm = AzureChatOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    temperature=0.7,
)


# Define tools for the agent
@tool
def save_user_preference(preference_type: str, value: str) -> str:
    """
    Save a user preference for future reference.
    
    Args:
        preference_type: Type of preference (e.g., "name", "interest", "goal")
        value: The preference value
        
    Returns:
        Confirmation message
    """
    print(f"\n💾 Saving preference: {preference_type} = {value}")
    return f"Saved {preference_type}: {value}"


@tool
def set_reminder(task: str, time: str) -> str:
    """
    Set a reminder for the user.
    
    Args:
        task: What to be reminded about
        time: When to be reminded
        
    Returns:
        Confirmation message
    """
    print(f"\n⏰ Setting reminder: '{task}' at {time}")
    return f"Reminder set: '{task}' at {time}"


@tool
def get_summary() -> str:
    """
    Get a summary of what we've discussed so far.
    
    Returns:
        A summary of the conversation
    """
    print(f"\n📋 Generating conversation summary...")
    return "Summary requested - agent will review conversation history"


# Tools and LLM setup
tools = [save_user_preference, set_reminder, get_summary]
llm_with_tools = llm.bind_tools(tools)


# Define state with conversation metadata
class ConversationState(TypedDict):
    """State that includes conversation history and metadata"""
    messages: Annotated[Sequence[BaseMessage], operator.add]
    user_name: str  # Stored user information
    conversation_id: str  # For tracking separate conversations


# System prompt for conversational agent
CONVERSATIONAL_SYSTEM_PROMPT = """You are a helpful AI assistant with memory.

Your capabilities:
- Remember information from earlier in our conversation
- Reference previous topics and context naturally
- Save user preferences when mentioned
- Set reminders when requested
- Provide personalized responses based on conversation history

Guidelines:
- Be conversational and friendly
- When users share personal information, acknowledge and remember it
- Refer back to earlier topics when relevant
- Use the save_user_preference tool when users share important information
- Use set_reminder tool when users mention tasks or appointments

Maintain context awareness throughout our conversation."""


def conversational_agent_node(state: ConversationState):
    """
    Agent node that maintains conversational context.
    """
    messages = state["messages"]
    
    # Add system prompt if not present
    if not any(isinstance(m, SystemMessage) for m in messages):
        messages = [SystemMessage(content=CONVERSATIONAL_SYSTEM_PROMPT)] + messages
    
    # Add user name context if available
    user_name = state.get("user_name", "")
    if user_name and len(messages) > 1:
        # Inject context about the user
        context_msg = SystemMessage(
            content=f"Note: The user's name is {user_name}. Use this naturally in conversation."
        )
        messages = [messages[0], context_msg] + messages[1:]
    
    print(f"\n💭 Processing conversation (Message #{len(state['messages'])})")
    
    response = llm_with_tools.invoke(messages)
    
    # Log agent actions
    if hasattr(response, 'tool_calls') and response.tool_calls:
        print(f"   Taking {len(response.tool_calls)} action(s)")
    
    return {"messages": [response]}


def should_continue_conversation(state: ConversationState):
    """
    Determine if tools need to be called.
    """
    messages = state["messages"]
    last_message = messages[-1]
    
    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        return "continue"
    return "end"


def extract_user_name(state: ConversationState):
    """
    Extract and store user name from tool calls.
    """
    messages = state["messages"]
    current_name = state.get("user_name", "")
    
    # Check if save_user_preference was called with name
    for msg in messages[-3:]:  # Check recent messages
        if hasattr(msg, 'tool_calls'):
            for tc in msg.tool_calls:
                if tc['name'] == 'save_user_preference':
                    args = tc.get('args', {})
                    if args.get('preference_type') == 'name':
                        return {"user_name": args.get('value', current_name)}
    
    return {"user_name": current_name}


def create_conversational_agent():
    """
    Create the conversational agent with memory.
    
    Uses checkpointing to maintain state across interactions.
    """
    workflow = StateGraph(ConversationState)
    
    # Add nodes
    workflow.add_node("agent", conversational_agent_node)
    workflow.add_node("tools", ToolNode(tools))
    workflow.add_node("update_context", extract_user_name)
    
    # Set entry point
    workflow.set_entry_point("agent")
    
    # Add edges
    workflow.add_conditional_edges(
        "agent",
        should_continue_conversation,
        {
            "continue": "tools",
            "end": END
        }
    )
    
    workflow.add_edge("tools", "update_context")
    workflow.add_edge("update_context", "agent")
    
    # Compile with memory checkpointing
    memory = MemorySaver()
    return workflow.compile(checkpointer=memory)


def run_conversation():
    """
    Run an interactive conversation with the agent.
    """
    print("\n" + "=" * 70)
    print("💬 CONVERSATIONAL AGENT WITH MEMORY")
    print("=" * 70)
    print("\nThis agent remembers context across the conversation.")
    print("Try mentioning your name, interests, or plans!\n")
    print("Type 'quit' to exit\n")
    
    app = create_conversational_agent()
    
    # Use a thread_id to maintain conversation state
    config = {"configurable": {"thread_id": "conversation-1"}}
    
    # Initial state
    state = {
        "messages": [],
        "user_name": "",
        "conversation_id": "conv-1"
    }
    
    conversation_history = []
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("\nAgent: Goodbye! It was nice talking with you.\n")
            break
        
        if not user_input:
            continue
        
        # Add user message to state
        conversation_history.append(HumanMessage(content=user_input))
        state["messages"] = conversation_history
        
        # Invoke agent
        try:
            result = app.invoke(state, config)
            
            # Update conversation history with full result
            conversation_history = result["messages"]
            state = result
            
            # Print agent response
            last_message = result["messages"][-1]
            if isinstance(last_message, AIMessage):
                print(f"\nAgent: {last_message.content}\n")
        
        except Exception as e:
            print(f"\n❌ Error: {str(e)}\n")
            continue


def run_demo_conversation():
    """
    Run a predefined demo conversation to show memory capabilities.
    """
    print("\n" + "=" * 70)
    print("🎬 DEMO: Conversation with Memory")
    print("=" * 70)
    
    app = create_conversational_agent()
    config = {"configurable": {"thread_id": "demo-conversation"}}
    
    # Predefined conversation
    conversation_turns = [
        "Hi! My name is Alex and I'm learning about agentic AI.",
        "I'm particularly interested in LangGraph for building agents.",
        "Can you remind me to review the LangGraph documentation tomorrow at 2pm?",
        "What have we discussed so far?",  # Tests memory/context
        "Based on what I told you, what topics should I focus on?"  # Tests personalization
    ]
    
    state = {
        "messages": [],
        "user_name": "",
        "conversation_id": "demo-1"
    }
    
    for i, user_msg in enumerate(conversation_turns, 1):
        print(f"\n--- Turn {i} ---")
        print(f"👤 User: {user_msg}")
        
        # Add user message
        state["messages"].append(HumanMessage(content=user_msg))
        
        # Invoke agent
        result = app.invoke(state, config)
        state = result
        
        # Print agent response
        last_message = result["messages"][-1]
        if isinstance(last_message, AIMessage):
            print(f"🤖 Agent: {last_message.content}")
        
        # Small delay for readability
        import time
        time.sleep(1)
    
    print("\n" + "=" * 70)
    print("✅ Demo Complete - Notice how the agent:")
    print("   - Remembered the user's name (Alex)")
    print("   - Referenced earlier topics (agentic AI, LangGraph)")
    print("   - Set a reminder when asked")
    print("   - Provided personalized suggestions based on interests")
    print("=" * 70 + "\n")


def main():
    """
    Main entry point - choose demo or interactive mode.
    """
    print("\n" + "🤖 AGENTIC AI DEMO - Agent with Memory" + "\n")
    
    print("Choose mode:")
    print("1. Run automated demo")
    print("2. Interactive conversation")
    print("3. Both")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == "1":
        run_demo_conversation()
    elif choice == "2":
        run_conversation()
    elif choice == "3":
        run_demo_conversation()
        input("\nPress Enter to start interactive mode...")
        run_conversation()
    else:
        print("Invalid choice. Running demo...")
        run_demo_conversation()


if __name__ == "__main__":
    main()
