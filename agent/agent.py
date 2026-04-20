from langchain.messages import AIMessage
from langchain_core.messages import HumanMessage

from langchain.agents import create_agent
from agent.tools import tools
from agent.llm import llm

from agent.router import route_query

summary = ""
messages = []


# ---------------- CLEAN OUTPUT ----------------
def clean_output(content):

    # If normal string response
    if isinstance(content, str):
        return content

    # If model returns list format
    if isinstance(content, list):

        texts = []

        for item in content:

            if isinstance(item, dict) and "text" in item:
                texts.append(item["text"])

            else:
                texts.append(str(item))

        return " ".join(texts)

    # Fallback
    return str(content)


# ---------------- MEMORY SUMMARY ----------------
def summarize_memory(summary, messages):

    prompt = f"""
Previous Summary:
{summary}

Conversation:
{messages}

Update short memory summary.
"""

    result = llm.invoke(prompt)

    return clean_output(result.content)


# ---------------- MAIN AGENT ----------------
def run_agent(user):

    global summary, messages

    # Store user message
    messages.append({
        "role": "user",
        "content": user
    })

    # Route query to correct agent
    agent_name, response = route_query(user)

    # Clean model response
    response = clean_output(response)

    # Final formatted response
    final_text = f"[{agent_name}]\n\n{response}"

    # Store assistant response
    messages.append({
        "role": "assistant",
        "content": final_text
    })

    # Summarize memory after long chat
    if len(messages) > 10:
        summary = summarize_memory(summary, messages[:-5])
        messages[:] = messages[-5:]

    return final_text