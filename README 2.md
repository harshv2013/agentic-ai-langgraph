# 🤖 Agentic AI with LangGraph & Azure OpenAI

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![LangGraph](https://img.shields.io/badge/LangGraph-latest-green.svg)](https://github.com/langchain-ai/langgraph)

A beginner-friendly guide to understanding and building **Agentic AI systems** using LangGraph and Azure OpenAI. This project demonstrates how AI agents can autonomously reason, use tools, and solve complex problems through practical, hands-on examples.

## 🎯 What You'll Learn

- **What is Agentic AI?** Understanding autonomous agents vs. simple chatbots
- **How agents think** - The reasoning-action loop that powers intelligent systems
- **Tool use** - How agents decide when and how to use tools
- **State management** - Maintaining context and memory across interactions
- **Multi-step reasoning** - Breaking down complex tasks into solvable steps

## 🌟 Key Features

- ✅ **Three Progressive Examples** - From simple to advanced agent patterns
- 📊 **Interactive Visualizations** - ASCII diagrams to understand agent flow
- 💾 **Memory & State** - Learn how agents remember context
- 🔧 **Real Tool Integration** - Calculator, search, and custom tools
- 📚 **Comprehensive Documentation** - Every concept explained clearly
- 🚀 **Production Ready** - Error handling, retries, and best practices

## 🏗️ Project Structure

```
agentic-ai-langgraph/
├── simple_agent.py           # Basic agent with calculator tool
├── research_agent.py          # Multi-step research with iteration control
├── agent_with_memory.py       # Conversational agent with memory
├── minimal_agent.py           # Simplified version (no LangGraph)
├── visualize_flows.py         # Interactive flow visualizations
├── requirements.txt           # Main dependencies
├── requirements-minimal.txt   # Minimal dependencies
├── QUICKSTART.md             # 5-minute setup guide
└── TROUBLESHOOTING.md        # Installation help
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- Azure OpenAI account with a deployed model
- 5 minutes of your time!

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/agentic-ai-langgraph.git
cd agentic-ai-langgraph
```

2. **Create virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure Azure OpenAI**
```bash
cp .env.example .env
# Edit .env with your Azure OpenAI credentials
```

Your `.env` should look like:
```env
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key
AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment-name
AZURE_OPENAI_API_VERSION=2024-02-15-preview
```

5. **Run your first agent!**
```bash
python simple_agent.py
```

## 📖 Examples Walkthrough

### 1. Simple Agent (`simple_agent.py`)

Your first agentic AI! This agent can:
- Perform calculations using a calculator tool
- Determine word lengths
- Decide when to use tools vs. answer directly

**Try it:**
```bash
python simple_agent.py
```

**What you'll see:**
```
QUERY: What is 45 * 67 + 123?

--- AGENT REASONING ---
Agent decided to call 1 tool(s)
  - calculator with args: {'expression': '45 * 67 + 123'}

--- AGENT REASONING ---
Agent decided to provide final answer

FINAL ANSWER: The result is 3,138.
```

**Key Concept:** The agent loops through reasoning → tool use → reasoning until it has the answer.

---

### 2. Research Agent (`research_agent.py`)

A more sophisticated agent that can:
- Conduct multi-step research
- Make follow-up searches based on findings
- Synthesize information from multiple sources
- Limit iterations to prevent infinite loops

**Try it:**
```bash
python research_agent.py
```

**Key Concept:** Agents can break down complex questions and iteratively gather information.

---

### 3. Agent with Memory (`agent_with_memory.py`)

An interactive conversational agent that:
- Remembers your name and preferences
- References earlier parts of the conversation
- Maintains context across multiple interactions
- Sets reminders and saves information

**Try it:**
```bash
python agent_with_memory.py
```

**Example conversation:**
```
You: Hi! My name is Alex and I'm learning about AI.
Agent: Nice to meet you, Alex! AI is a fascinating field...

You: What did I tell you my name was?
Agent: Your name is Alex!
```

**Key Concept:** State management and checkpointing enable persistent memory.

---

### 4. Visualize Flows (`visualize_flows.py`)

Interactive ASCII diagrams showing:
- How agent graphs are structured
- State flow through nodes
- Tool calling patterns
- Decision points and loops

**Try it:**
```bash
python visualize_flows.py
```

## 🧠 Understanding Agentic AI

### What Makes an Agent "Agentic"?

Unlike traditional chatbots that simply respond to prompts, agentic AI systems can:

1. **Plan** - Break down complex goals into steps
2. **Act** - Use tools to gather information or take actions
3. **Observe** - Process results from their actions
4. **Adapt** - Adjust their approach based on feedback
5. **Loop** - Iterate until the goal is achieved

### The Agent Loop

```
┌─────────────────────────────────────┐
│  User Query: "What's 123 * 456?"   │
└──────────────┬──────────────────────┘
               │
               ▼
┌──────────────────────────────────────┐
│  Agent Reasoning:                    │
│  "I need to calculate this"          │
└──────────────┬───────────────────────┘
               │
               ▼
┌──────────────────────────────────────┐
│  Tool Execution:                     │
│  calculator("123 * 456")             │
└──────────────┬───────────────────────┘
               │
               ▼
┌──────────────────────────────────────┐
│  Agent Reasoning:                    │
│  "Got result: 56,088"                │
└──────────────┬───────────────────────┘
               │
               ▼
┌──────────────────────────────────────┐
│  Final Answer:                       │
│  "123 × 456 = 56,088"                │
└──────────────────────────────────────┘
```

## 🛠️ Key Technologies

- **[LangGraph](https://github.com/langchain-ai/langgraph)** - State management and agent orchestration
- **[Azure OpenAI](https://azure.microsoft.com/en-us/products/ai-services/openai-service)** - Enterprise-grade LLM access
- **[LangChain](https://github.com/langchain-ai/langchain)** - LLM application framework
- **Python 3.9+** - Programming language

## 📚 Learning Path

1. **Start with `QUICKSTART.md`** - Get everything running in 5 minutes
2. **Run `simple_agent.py`** - Understand the basic agentic loop
3. **Study the code** - Each file is heavily commented
4. **Run `visualize_flows.py`** - See how graphs are structured
5. **Experiment with `research_agent.py`** - Learn multi-step reasoning
6. **Try `agent_with_memory.py`** - Explore state management
7. **Build your own agent!** - Apply what you've learned

## 🔧 Customization

### Adding Your Own Tools

```python
from langchain_core.tools import tool

@tool
def your_custom_tool(input: str) -> str:
    """Description of what your tool does."""
    # Your logic here
    return result

# Add to tools list
tools = [calculator, your_custom_tool]
```

### Modifying Agent Behavior

Edit the system prompt in any example:
```python
SYSTEM_PROMPT = """You are a helpful assistant that...
Your behavior:
- Be concise
- Use tools when needed
- Explain your reasoning
"""
```

## 🐛 Troubleshooting

Having installation issues? Check out `TROUBLESHOOTING.md` for:
- Common installation errors and fixes
- Alternative installation methods
- Platform-specific issues (Mac M1/M2, Windows, Linux)
- Minimal installation options

**Quick Fix:** If full installation fails, try minimal version:
```bash
pip install -r requirements-minimal.txt
python minimal_agent.py
```

## 📖 Additional Resources

- [QUICKSTART.md](QUICKSTART.md) - Detailed setup guide
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Installation help
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Azure OpenAI Documentation](https://learn.microsoft.com/en-us/azure/ai-services/openai/)

## 🎓 What's Next?

After mastering these examples, explore:

- **Multi-agent systems** - Multiple agents working together
- **Human-in-the-loop** - Approval workflows
- **Custom state management** - Complex data structures
- **Production deployment** - Docker, monitoring, scaling
- **Advanced patterns** - ReAct, Plan-and-Execute, Reflection

## 🤝 Contributing

Contributions are welcome! Whether it's:
- 🐛 Bug fixes
- 📚 Documentation improvements
- ✨ New examples
- 💡 Feature suggestions

Please feel free to open an issue or submit a pull request.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [LangGraph](https://github.com/langchain-ai/langgraph) by LangChain
- Powered by [Azure OpenAI](https://azure.microsoft.com/en-us/products/ai-services/openai-service)
- Inspired by the growing agentic AI community

## 💬 Questions or Feedback?

- Open an issue on GitHub
- Share what you build with this project!
- Star ⭐ this repo if you find it helpful

---

**Ready to build your first agent?** Start with `QUICKSTART.md` and run `python simple_agent.py`! 🚀
