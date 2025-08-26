import streamlit as st
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# Load local .env (only used for local development)
load_dotenv()

# Get API key (first try .env, then Streamlit secrets)
groq_api_key = os.getenv("GROQ_API_KEY") or st.secrets["GROQ_API_KEY"]

# Sidebar settings
st.sidebar.title("⚙️ Settings")
model_choice = st.sidebar.selectbox(
    "Choose a model",
    ["llama-3.1-70b-versatile", "mixtral-8x7b-32768"]  # ✅ correct names
)

# Initialize Groq chat model
chat_model = ChatGroq(model=model_choice, api_key=groq_api_key)

# Streamlit app setup
st.set_page_config(page_title="Expert Chat AI", page_icon="🤖")
st.title("🤖 Expert Chat AI")

# Initialize conversation history
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        SystemMessage(content="You are an expert assistant. Answer clearly and helpfully.")
    ]

# Display previous messages
for msg in st.session_state["messages"]:
    role = "user" if isinstance(msg, HumanMessage) else "assistant"
    if not isinstance(msg, SystemMessage):
        with st.chat_message(role):
            st.markdown(msg.content)

# User input
user_input = st.chat_input("Ask me anything...")

if user_input:
    # Add user message
    st.session_state["messages"].append(HumanMessage(content=user_input))

    # Get response
    response = chat_model.invoke(st.session_state["messages"])
    ai_message = AIMessage(content=response.content)

    # Add AI response
    st.session_state["messages"].append(ai_message)

    # Show AI response
    with st.chat_message("assistant"):
        st.markdown(ai_message.content)

