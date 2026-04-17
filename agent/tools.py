from dotenv import load_dotenv
load_dotenv()

from langchain.tools import tool
from datetime import datetime
from tavily import TavilyClient
import os
from agent.rag import get_retriever

def get_tavily():
    return TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def get_latest_news(query: str) -> str:
    """Get latest news about any topic."""
    tavily = get_tavily()

    response = tavily.search(
        query=f"Latest important news about {query} last 7 days",
        search_depth="basic",
        topic="news",
        max_results=3,
        include_answer=True
    )

    results = response.get("results", [])

    if not results:
        return "No latest news found."

    return "\n\n".join(
        f"Title: {x['title']}\nSource: {x['url']}\nSummary: {x['content']}"
        for x in results
    )

@tool
def get_current_time() -> str:
    """Get current date and time."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@tool
def search_knowledge(query: str) -> str:
    """Search internal knowledge base."""
    retriever = get_retriever()
    docs = retriever.invoke(query)

    if docs:
        return docs[0].page_content
    return "No result found."

tools = [get_current_time, get_latest_news, search_knowledge]