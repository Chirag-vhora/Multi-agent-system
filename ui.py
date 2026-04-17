import streamlit as st
import requests
import os

API_URL = "http://127.0.0.1:8000/chat"

st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="wide"
)

# ---------------- Sidebar ----------------
with st.sidebar:
    st.title("⚙️ Settings")
    st.markdown("Upload PDF / TXT files for RAG")

    uploaded_file = st.file_uploader(
        "Upload File",
        type=["pdf", "txt"]
    )

    if uploaded_file:
        save_path = f"uploads/{uploaded_file.name}"

        os.makedirs("uploads", exist_ok=True)

        with open(save_path, "wb") as f:
            f.write(uploaded_file.read())

        st.success(f"{uploaded_file.name} uploaded!")

    st.divider()
    st.markdown("Built with Streamlit")

# ---------------- Main UI ----------------
st.title("🤖 AI Chat Assistant")
st.caption("Chat + PDF/TXT RAG + Tools")

# Session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
user_input = st.chat_input("Ask anything...")

if user_input:

    # Show user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    # API Call
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):

            try:
                response = requests.post(
                    API_URL,
                    json={"message": user_input}
                )

                bot_reply = response.json()["response"]

            except:
                bot_reply = "⚠️ Backend server not running."

            st.markdown(bot_reply)

    st.session_state.messages.append(
        {"role": "assistant", "content": bot_reply}
    )