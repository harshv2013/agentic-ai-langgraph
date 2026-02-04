# Agentic AI with LangGraph and Azure OpenAI

## Overview

This project demonstrates how to build **agentic AI systems** using LangGraph and Azure OpenAI. It provides hands-on examples to understand the flow of autonomous agents that can reason, plan, and take actions.

## What is Agentic AI?

Agentic AI refers to AI systems that can:
- **Reason** about problems and break them down into steps
- **Plan** sequences of actions to achieve goals
- **Use tools** to interact with external systems
- **Maintain state** across multiple interactions
- **Self-correct** based on feedback from actions

Unlike simple chat applications, agents can loop through reasoning cycles, call tools, and adapt their approach based on results.

## What is LangGraph?

LangGraph is a framework for building stateful, multi-actor applications with LLMs. Key concepts:

### 1. **State Graph**
- Nodes represent computation steps (agent decisions, tool calls)
- Edges define the flow between nodes
- State is passed and updated between nodes

### 2. **Core Components**
- **State**: Shared data structure that flows through the graph
- **Nodes**: Functions that process state (e.g., agent_node, tool_node)
- **Edges**: Connections between nodes (conditional or direct)
- **Checkpointing**: Save and resume state at any point

### 3. **Agent Flow Pattern**
```
START → Agent Reasoning → Tool Execution → Agent Reasoning → END
          ↑_______________|
           (feedback loop)
```

## Project Structure

```
agentic-ai-langgraph/
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variables template
├── simple_agent.py              # Basic agent example
├── research_agent.py            # Multi-step research agent
└── agent_with_memory.py         # Agent with conversation memory
```

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Azure OpenAI

Create a `.env` file in the project root:

```env
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment-name
AZURE_OPENAI_API_VERSION=2024-02-15-preview
```

### 3. Run Examples

```bash
# Simple agent with calculator tool
python simple_agent.py

# Research agent with web search
python research_agent.py

# Agent with memory
python agent_with_memory.py
```

## Examples Explained

### 1. Simple Agent (`simple_agent.py`)
Demonstrates basic agent flow with a calculator tool. Shows how the agent:
- Receives a query
- Decides to use tools
- Executes tool calls
- Reasons about results
- Provides final answer

### 2. Research Agent (`research_agent.py`)
Multi-step agent that can:
- Search for information
- Analyze results
- Make follow-up searches
- Synthesize findings

### 3. Agent with Memory (`agent_with_memory.py`)
Shows how to maintain conversation history and context across multiple interactions.

## Key LangGraph Patterns

### State Definition
```python
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage
import operator

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    # Add more state fields as needed
```

### Creating Nodes
```python
def agent_node(state: AgentState):
    # Agent reasoning logic
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

def tool_node(state: AgentState):
    # Execute tools
    results = execute_tools(state["messages"][-1].tool_calls)
    return {"messages": results}
```

### Building the Graph
```python
from langgraph.graph import StateGraph, END

workflow = StateGraph(AgentState)
workflow.add_node("agent", agent_node)
workflow.add_node("tools", tool_node)

# Add conditional edges
workflow.add_conditional_edges(
    "agent",
    should_continue,  # Function that decides next step
    {"continue": "tools", "end": END}
)

app = workflow.compile()
```

## Agent Execution Flow

1. **Input**: User query enters the graph
2. **Agent Node**: LLM analyzes query, decides on actions
3. **Conditional Routing**: Should use tools or provide answer?
4. **Tool Node** (if needed): Execute tool calls, get results
5. **Back to Agent**: Agent processes tool results
6. **Loop or End**: Continue for more tools or provide final answer

## Best Practices

1. **Define clear state schema** - Makes debugging easier
2. **Use type hints** - Helps catch errors early
3. **Add logging** - Track agent reasoning process
4. **Implement checkpointing** - Save state for complex workflows
5. **Handle errors gracefully** - Tools can fail, agent should recover
6. **Limit iterations** - Prevent infinite loops with max_iterations

## Resources

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Azure OpenAI Documentation](https://learn.microsoft.com/en-us/azure/ai-services/openai/)
- [LangChain Tools](https://python.langchain.com/docs/modules/agents/tools/)

## Next Steps

After understanding these examples, explore:
- Custom tool creation
- Multi-agent systems
- Human-in-the-loop workflows
- Advanced error handling and retries
- Streaming responses
- Production deployment patterns
