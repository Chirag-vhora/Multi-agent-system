from langchain.agents import create_agent
from agent.llm import llm

agent = create_agent(
    model=llm,
    tools=[],
    system_prompt="""
You are a helpful general AI assistant.
Answer clearly and concisely.
"""
)

def run_general_agent(query):
    response = agent.invoke(
        {"messages": [{"role": "user", "content": query}]}
    )

    return response["messages"][-1].content