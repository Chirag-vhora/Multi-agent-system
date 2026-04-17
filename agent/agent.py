from langchain.messages import AIMessage
from langchain_core.messages import HumanMessage

from langchain.agents import create_agent
from agent.tools import tools
from agent.llm import llm



agent = create_agent(
    model=llm,
    tools = tools ,
    system_prompt="""
You are a helpful AI assistant.

You have access to:
- Internal knowledge base (search_knowledge tool)
- Conversation memory

Rules:

1. Always use search_knowledge tool when:
- user asks about RAG
- user asks factual questions
- user asks about internal knowledge
- user asks something you are unsure about

2. Personalization:
- If you know user's name, use it naturally in responses
- Be friendly and conversational

3. Memory:
- Remember important user details
- Use previous conversation context when helpful

4. Tool Usage:
- Prefer using tools before answering
- Use tools when accuracy is important

Be concise, helpful, and friendly.
""",
)

def summarize_memory(summary, messages):
    prompt = f"""
    You are a memory summarizer.

    Previous Summary:
    {summary}

    New Conversation:
    {messages}

    Update the summary briefly.
    Keep important facts only.
    """

    response = llm.invoke(prompt)

    return response.content

    
# summary = ""
# messages = []
# def run_agent():


summary = ""
messages = []

def run_agent(user: str):
    global summary, messages

    # Add user message
    messages.append({
        "role": "user",
        "content": user
    })

    response = agent.invoke(
        {
            "messages": (
                [{"role": "system", "content": summary}] if summary else []
            ) + messages
        }
    )

    ai_message = response["messages"][-1]

    if isinstance(ai_message.content, list):
        ai_text = ai_message.content[0]["text"]
    else:
        ai_text = ai_message.content

    # Add AI response to memory
    messages.append({
        "role": "assistant",
        "content": ai_text
    })

    # Summarize memory
    if len(messages) > 10:
        summary = summarize_memory(summary, messages[:-5])
        messages = messages[-5:]

    return ai_text

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