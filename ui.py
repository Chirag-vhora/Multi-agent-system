import streamlit as st
import requests
import os

API_URL = "http://127.0.0.1:8000/chat"
UPLOAD_URL = "http://127.0.0.1:8000/upload"

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

        if st.button("Upload File"):

            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    uploaded_file.type
                )
            }

            try:
                response = requests.post(
                    UPLOAD_URL,
                    files=files
                )

                if response.status_code == 200:
                    st.success(f"{uploaded_file.name} uploaded successfully!")

                else:
                    st.error("Upload failed.")

            except:
                st.error("Backend server not running.")

    st.divider()
    st.markdown("Built with Streamlit")

# ---------------- Main UI ----------------
st.title("🤖 AI Chat Assistant")
st.caption("Chat + PDF/TXT RAG + Tools")

# Chat memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show old messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Chat input
user_input = st.chat_input("Ask anything...")

if user_input:

    # User message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.write(user_input)

    # Assistant message
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):

            try:
                response = requests.post(
                    API_URL,
                    json={"message": user_input}
                )

                if response.status_code == 200:
                    bot_reply = response.json()["response"]
                else:
                    bot_reply = "⚠️ Error from backend."

            except:
                bot_reply = "⚠️ Backend server not running."

            st.write(bot_reply)

    st.session_state.messages.append({
        "role": "assistant",
        "content": bot_reply
    })