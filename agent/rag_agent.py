from langchain.agents import create_agent
from agent.llm import llm
from agent.tools import search_knowledge

agent = create_agent(
    model=llm,
    tools=[search_knowledge],
    system_prompt="""
You are a document assistant.

Always use search_knowledge tool first.
Answer only from retrieved content when possible.
"""
)

def run_rag_agent(query):
    response = agent.invoke(
        {"messages": [{"role": "user", "content": query}]}
    )

    return response["messages"][-1].content