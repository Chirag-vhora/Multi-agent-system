from langchain.messages import AIMessage
from langchain_core.messages import HumanMessage

from langchain.agents import create_agent
from agent.tools import tools
from agent.llm import llm


from agent.router import route_query
# from agent.llm import llm

summary = ""
messages = []


def summarize_memory(summary, messages):

    prompt = f"""
Previous Summary:
{summary}

Conversation:
{messages}

Update short memory summary.
"""

    return llm.invoke(prompt).content


def run_agent(user):

    global summary, messages

    messages.append({"role": "user", "content": user})

    agent_name, response = route_query(user)

    final_text = f"[{agent_name}]\n\n{response}"

    messages.append({"role": "assistant", "content": final_text})

    if len(messages) > 10:
        summary = summarize_memory(summary, messages[:-5])
        messages[:] = messages[-5:]

    return final_text




    # print("Gemini Chat Ready (type exit to quit)\n")

    # while True:
    #     user = input("YOU: ").strip()

    #     if user.lower() == "exit":
    #         print("Goodbye ! 👋")
    #         break
        
    #     # Add user message
    #     messages.append({
    #         "role": "user",
    #         "content": user
    #     })
        
    #     response = agent.invoke(
    #         {
    #             "messages": (
    #                 [{"role": "system", "content": summary}] if summary else []
    #             ) + messages
    #         }
    #     )
    #     # print(f"answer -- > {response}")
    #     ai_message = response["messages"][-1]

    #     if isinstance(ai_message.content, list):
    #         # print("AI:", ai_message.content[0]["text"])
    #         ai_text = ai_message.content[0]["text"]
    #     else:
    #         # print("AI:", ai_message.content)
    #         ai_text = ai_message.content
            
    #     # Add AI response to memory
    #     messages.append({
    #         "role": "assistant",
    #         "content": ai_text
    #     })
        
    #     # Summarize memory
    #     if len(messages) > 10:
    #         summary = summarize_memory(summary, messages[:-5])
    #         messages = messages[-5:]

    #     print("AI:" , ai_text)
    #     print()