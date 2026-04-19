from agent.llm import llm

from agent.general_agent import run_general_agent
from agent.rag_agent import run_rag_agent
from agent.tool_agent import run_tool_agent
from agent.coding_agent import run_coding_agent


def classify_query(query):

    prompt = f"""
Classify user query into ONLY one category:

general
rag
tool
coding

User Query:
{query}

Reply only one word.
"""

    result = llm.invoke(prompt)

    content = result.content

    # Handle list response
    if isinstance(content, list):
        route = content[0]["text"].strip().lower()

    else:
        route = content.strip().lower()

    return route


def route_query(query):

    route = classify_query(query)

    if route == "rag":
        return "RAG Agent", run_rag_agent(query)

    elif route == "tool":
        return "Tool Agent", run_tool_agent(query)

    elif route == "coding":
        return "Coding Agent", run_coding_agent(query)

    return "General Agent", run_general_agent(query)