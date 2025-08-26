import streamlit as st
from dotenv import load_dotenv, find_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import os

# Load API key from .env
_ = load_dotenv(find_dotenv())

# Sidebar to choose model
st.sidebar.title("⚙️ Settings")
model_choice = st.sidebar.selectbox(
    "Choose a model",
    ["llama3-70b-8192", "mixtral-8x7b-32768"]
)

# Initialize selected model with API key
chat_model = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),  # ✅ FIXED
    model=model_choice
)

# Streamlit app UI
st.set_page_config(page_title="Expert Chat AI", page_icon="🤖")
st.title("🤖 Expert Chat AI - Ask anything")

# Initialize conversation history
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        SystemMessage(content="You are an expert. Answer user questions.")
    ]

# Display conversation history
for msg in st.session_state["messages"]:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user"):
            st.markdown(msg.content)
    elif isinstance(msg, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(msg.content)

# User input box
user_input = st.chat_input("Ask anything...")

if user_input:
    # Append user input
    st.session_state["messages"].append(HumanMessage(content=user_input))

    try:
        # ✅ Wrap in try/except so app won’t crash
        response = chat_model.invoke(st.session_state["messages"])
        ai_message = response.content

        # Append AI response
        st.session_state["messages"].append(AIMessage(content=ai_message))

        # Display AI response
        with st.chat_message("assistant"):
            st.markdown(ai_message)

    except Exception as e:
        st.error("⚠️ Groq API call failed. Please check your API key, quota, or model name.")
        st.info(f"Debug info: {str(e)}")
