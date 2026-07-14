"""
streamlit_app.py

SmartKart AI Customer Support Chatbot
"""

import streamlit as st

from conversation import ConversationMemory
from tool_executor import execute_customer_query

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="SmartKart AI Assistant",
    page_icon="🛒",
    layout="centered",
)

# --------------------------------------------------
# Session State
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "memory" not in st.session_state:
    st.session_state.memory = ConversationMemory()

# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("🛒 SmartKart AI Customer Support")

st.caption(
    "Powered by Gemini 3.1 Flash Lite • LangChain • FAISS • RAG"
)

# --------------------------------------------------
# Display Chat History
# --------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# --------------------------------------------------
# Chat Input
# --------------------------------------------------

prompt = st.chat_input(
    "Ask me anything about SmartKart..."
)

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    with st.chat_message("user"):

        st.markdown(prompt)

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:

                response = execute_customer_query(
                    query=prompt,
                    memory=st.session_state.memory,
                )

                if not response:

                    response = (
                        "Sorry, I couldn't generate a response."
                    )

            except Exception:

                response = (
                    "An unexpected error occurred."
                )

            st.markdown(response)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response,
        }
    )

# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:

    st.header("🛒 SmartKart AI")

    st.markdown("### Features")

    st.markdown("- ✅ LangChain")
    st.markdown("- ✅ Gemini 3.1 Flash Lite")
    st.markdown("- ✅ Pydantic Structured Output")
    st.markdown("- ✅ Intelligent Routing")
    st.markdown("- ✅ Tool Calling")
    st.markdown("- ✅ FAISS")
    st.markdown("- ✅ HuggingFace Embeddings")
    st.markdown("- ✅ RAG")
    st.markdown("- ✅ Conversation Memory")

    st.divider()

    if st.button("🗑️ Clear Chat"):

        st.session_state.messages = []
        st.session_state.memory = ConversationMemory()

        st.rerun()