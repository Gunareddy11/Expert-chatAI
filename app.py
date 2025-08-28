import streamlit as st
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# ---------------------------
# Load environment variables
# ---------------------------
load_dotenv()  # loads .env if running locally

# Try to load key from .env first, then Streamlit secrets
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    try:
        groq_api_key = st.secrets["GROQ_API_KEY"]
    except Exception:
        st.error("🚨 Missing GROQ_API_KEY. Please set it in .env (local) or Streamlit Cloud secrets.")
        st.stop()

# ---------------------------
# Streamlit page setup
# ---------------------------
st.set_page_config(page_title="Expert Chat AI", page_icon="🤖")
st.title("🤖 Expert Chat AI")

# ---------------------------
# Sidebar settings
# ---------------------------
st.sidebar.title("⚙️ Settings")
model_choice = st.sidebar.selectbox(
    "Choose a model",
    ["llama-3.1-70b-versatile", "mixtral-8x7b-32768"]  # ✅ valid Groq models
)

# Initialize Groq model
chat_model = ChatGroq(model=model_choice, api_key=groq_api_key)

# ---------------------------
# Conversation history
# ---------------------------
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        SystemMessage(content="You are an expert assistant. Answer clearly and helpfully.")
    ]

# Show conversation so far
for msg in st.session_state["messages"]:
    role = "user" if isinstance(msg, HumanMessage) else "assistant"
    if not isinstance(msg, SystemMessage):  # don’t show system prompt
        with st.chat_message(role):
            st.markdown(msg.content)

# ---------------------------
# User input & AI response
# ---------------------------
user_input = st.chat_input("Ask me anything...")

if user_input:
    # Add user message
    st.session_state["messages"].append(HumanMessage(content=user_input))

    # Get response from Groq model
    try:
        response = chat_model.invoke(st.session_state["messages"])
        ai_message = AIMessage(content=response.content)

        # Save AI response
        st.session_state["messages"].append(ai_message)

        # Display AI response
        with st.chat_message("assistant"):
            st.markdown(ai_message.content)

    except Exception as e:
        st.error(f"🚨 Error: {e}")

