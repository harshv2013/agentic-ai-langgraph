"""
Minimal Agent Example - No LangGraph Required

This is a simplified version that demonstrates agentic AI concepts
using just the openai package directly. Use this if you're having
trouble installing LangGraph.

Requirements: pip install openai python-dotenv
"""

import os
import json
from dotenv import load_dotenv
from openai import AzureOpenAI

# Load environment variables
load_dotenv()

# Initialize Azure OpenAI client
client = AzureOpenAI(
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
)

DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")


# Define tools as functions
def calculator(expression: str) -> str:
    """Evaluate a mathematical expression."""
    try:
        allowed_chars = set("0123456789+-*/(). ")
        if not all(c in allowed_chars for c in expression):
            return "Error: Expression contains invalid characters"
        result = eval(expression)
        return f"The result is: {result}"
    except Exception as e:
        return f"Error calculating: {str(e)}"


def get_word_length(word: str) -> str:
    """Get the length of a word."""
    return f"The word '{word}' has {len(word)} characters"


# Tool definitions for OpenAI
tools = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Evaluate a mathematical expression",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "A mathematical expression (e.g., '2 + 2', '10 * 5')",
                    }
                },
                "required": ["expression"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_word_length",
            "description": "Get the length of a word",
            "parameters": {
                "type": "object",
                "properties": {
                    "word": {
                        "type": "string",
                        "description": "The word to measure",
                    }
                },
                "required": ["word"],
            },
        },
    },
]

# Map function names to actual functions
available_functions = {
    "calculator": calculator,
    "get_word_length": get_word_length,
}


def run_agent(user_query: str, max_iterations: int = 5):
    """
    Run the agent with a query.
    
    This implements the basic agentic loop:
    1. Agent reasons about the query
    2. Agent decides to use tools or answer
    3. Tools are executed
    4. Results feed back to agent
    5. Loop continues until agent has final answer
    """
    print("=" * 70)
    print(f"QUERY: {user_query}")
    print("=" * 70)
    
    # Start conversation with user query
    messages = [{"role": "user", "content": user_query}]
    
    iteration = 0
    while iteration < max_iterations:
        iteration += 1
        print(f"\n--- ITERATION {iteration} ---")
        
        # Call LLM with tools
        print("Agent is thinking...")
        response = client.chat.completions.create(
            model=DEPLOYMENT_NAME,
            messages=messages,
            tools=tools,
            tool_choice="auto",
            temperature=0,
        )
        
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        print(f"response_message : {response_message}")
        print(f"tool_calls : {tool_calls}")


        
        # Add assistant's response to messages
        messages.append(response_message)
        
        # Check if agent wants to use tools
        if tool_calls:
            print(f"Agent decided to use {len(tool_calls)} tool(s):")
            
            # Execute each tool call
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                print(f"  → Calling {function_name} with args: {function_args}")
                
                # Execute the function
                function_to_call = available_functions[function_name]
                function_response = function_to_call(**function_args)
                
                print(f"  ← Tool result: {function_response}")
                
                # Add tool response to messages
                messages.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": function_response,
                    }
                )
        else:
            # Agent provided final answer
            print("Agent has final answer")
            break
    
    # Print final answer
    print("\n" + "=" * 70)
    print("FINAL ANSWER:")
    print("=" * 70)
    final_answer = messages[-1].content if hasattr(messages[-1], 'content') else response_message.content
    print(final_answer)
    print("\n")


def main():
    """Run example queries."""
    print("\n🤖 MINIMAL AGENTIC AI DEMO\n")
    print("This example uses only the openai package directly.\n")
    
    # Test queries
    queries = [
        "What is 45 * 67 + 123?",
        # "Calculate (15 + 25) * 3, and tell me how long the word 'artificial' is",
        # "What is the capital of France?",
    ]
    
    for query in queries:
        run_agent(query)
        input("Press Enter for next example...")


if __name__ == "__main__":
    main()
