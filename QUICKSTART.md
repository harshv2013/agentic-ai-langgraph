# Quick Start Guide

## Get Up and Running in 5 Minutes

This guide will help you set up and run your first agentic AI application with LangGraph and Azure OpenAI.

### Step 1: Prerequisites

Ensure you have:
- Python 3.9 or higher
- An Azure account with OpenAI service
- Azure OpenAI deployment created (GPT-4 or GPT-3.5-Turbo)

### Step 2: Set Up Azure OpenAI

1. **Create Azure OpenAI Resource**
   - Go to [Azure Portal](https://portal.azure.com)
   - Search for "Azure OpenAI"
   - Click "Create" and follow the wizard
   - Note your endpoint URL (e.g., `https://your-resource.openai.azure.com/`)

2. **Deploy a Model**
   - In your Azure OpenAI resource, go to "Model deployments"
   - Click "Create new deployment"
   - Choose a model (GPT-4 or GPT-3.5-Turbo recommended)
   - Give it a deployment name (e.g., "gpt-4")
   - Note this deployment name

3. **Get Your API Key**
   - In your Azure OpenAI resource, go to "Keys and Endpoint"
   - Copy one of the keys

### Step 3: Install Dependencies

```bash
# Navigate to the project directory
cd agentic-ai-langgraph

# Install required packages
pip install -r requirements.txt
```

### Step 4: Configure Environment

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` and fill in your Azure OpenAI credentials:
```env
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment-name
AZURE_OPENAI_API_VERSION=2024-02-15-preview
```

### Step 5: Run Your First Agent

Let's start with the simplest example:

```bash
python simple_agent.py
```

You should see output like:
```
🤖 AGENTIC AI DEMO - Simple Agent with Tools

==============================================================
QUERY: What is 45 * 67 + 123?
==============================================================

--- AGENT REASONING ---
Processing 1 messages
Agent decided to call 1 tool(s)
  - calculator with args: {'expression': '45 * 67 + 123'}

🔧 Executing tool: calculator

--- AGENT REASONING ---
Processing 3 messages
Agent decided to provide final answer

==============================================================
FINAL ANSWER:
==============================================================
The result is 3,138.
```

🎉 **Congratulations!** You just ran your first agentic AI application!

### Step 6: Explore More Examples

Now try the other examples:

1. **Research Agent** (multi-step reasoning):
   ```bash
   python research_agent.py
   ```

2. **Agent with Memory** (conversational context):
   ```bash
   python agent_with_memory.py
   ```

3. **Flow Visualizations** (understand the architecture):
   ```bash
   python visualize_flows.py
   ```

### Understanding What Happened

In the simple agent example:

1. **Agent received query**: "What is 45 * 67 + 123?"

2. **Agent reasoned**: "I need to perform a calculation"

3. **Agent called tool**: `calculator("45 * 67 + 123")`

4. **Tool executed**: Calculated the result

5. **Agent synthesized**: "The result is 3,138"

This is the **agentic loop** in action!

### Common Issues and Solutions

#### Issue: Import Error
```
ModuleNotFoundError: No module named 'langchain'
```
**Solution**: Make sure you installed dependencies: `pip install -r requirements.txt`

#### Issue: Authentication Error
```
Error: Invalid API key
```
**Solution**: 
- Double-check your `.env` file
- Ensure your API key is correct
- Verify your endpoint URL includes `https://`

#### Issue: Model Not Found
```
Error: Deployment not found
```
**Solution**: 
- Verify your deployment name in `.env` matches exactly what's in Azure portal
- Make sure the deployment is fully completed in Azure

#### Issue: Rate Limiting
```
Error: Rate limit exceeded
```
**Solution**:
- Your Azure OpenAI resource has rate limits
- Wait a few moments and try again
- Consider upgrading your Azure OpenAI tier if this happens frequently

### Next Steps

Now that you have a working setup:

1. **Modify the examples**: 
   - Add new tools to `simple_agent.py`
   - Customize the research agent queries
   - Extend the memory agent with new capabilities

2. **Read the README**: 
   - Understand LangGraph concepts deeply
   - Learn about state management
   - Explore advanced patterns

3. **Build your own agent**:
   - Think of a use case (data analysis, content creation, automation)
   - Design your tools
   - Create your agent graph
   - Test and iterate

### Helpful Resources

- **LangGraph Docs**: https://langchain-ai.github.io/langgraph/
- **Azure OpenAI Docs**: https://learn.microsoft.com/en-us/azure/ai-services/openai/
- **LangChain Tools**: https://python.langchain.com/docs/modules/agents/tools/

### Getting Help

If you encounter issues:
1. Check the error message carefully
2. Verify your `.env` configuration
3. Try the visualize_flows.py script to understand the architecture
4. Review the comments in the code examples
5. Consult the LangGraph documentation

---

**Happy Building! 🚀**

The key to understanding agentic AI is experimenting. Try modifying the examples, breaking things, and fixing them. That's the best way to learn!
