import os
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, AIMessage

# Load environment variables
load_dotenv()

# Initialize Groq model
chat_model = ChatGroq(model="llama3-8b-8192")

# Streamlit UI
st.title("💬 Expert Chatbot (Groq + LangChain)")
st.write("Ask me anything!")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display chat history
for msg in st.session_state["messages"]:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user"):
            st.markdown(msg.content)
    elif isinstance(msg, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(msg.content)

# User input
if prompt := st.chat_input("Type your question..."):
    # Add user message
    user_msg = HumanMessage(content=prompt)
    st.session_state["messages"].append(user_msg)

    with st.chat_message("user"):
        st.markdown(prompt)

    # Get response from Groq model
    try:
        response = chat_model.invoke(st.session_state["messages"])
        bot_msg = AIMessage(content=response.content)
        st.session_state["messages"].append(bot_msg)

        with st.chat_message("assistant"):
            st.markdown(response.content)

    except Exception as e:
        st.error(f"Error: {e}")

