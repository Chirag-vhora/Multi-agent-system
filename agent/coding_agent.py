from langchain.agents import create_agent
from agent.llm import llm

agent = create_agent(
    model=llm,
    tools=[],
    system_prompt="""
You are an expert coding assistant.
Help with Python, FastAPI, debugging, APIs, clean code.
"""
)

def run_coding_agent(query):
    response = agent.invoke(
        {"messages": [{"role": "user", "content": query}]}
    )

    return response["messages"][-1].content