from langchain.agents import create_agent
from agent.llm import llm
from agent.tools import get_latest_news, get_current_time

agent = create_agent(
    model=llm,
    tools=[get_latest_news, get_current_time],
    system_prompt="""
You are a tool assistant.

Use tools when needed for latest info or time.
"""
)

def run_tool_agent(query):
    response = agent.invoke(
        {"messages": [{"role": "user", "content": query}]}
    )

    return response["messages"][-1].content