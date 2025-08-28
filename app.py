import streamlit as st
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

load_dotenv()

groq_api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
if not groq_api_key or not groq_api_key.startswith("gsk_"):
    st.error("🚨 Groq API key is missing or invalid. Please check your secrets and .env file.")
    st.stop()

st.sidebar.title("⚙️ Settings")
model_choice = st.sidebar.selectbox(
    "Choose a model",
    ["mistral-saba-24b", "llama-3.3-70b-versatile"]  #  Updated models
)

chat_model = ChatGroq(model=model_choice, api_key=groq_api_key)

st.set_page_config(page_title="Expert Chat AI", page_icon="🤖")
st.title("🤖 Expert Chat AI")

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        SystemMessage(content="You are an expert assistant. Answer clearly and helpfully.")
    ]

for msg in st.session_state["messages"]:
    role = "user" if isinstance(msg, HumanMessage) else "assistant"
    if not isinstance(msg, SystemMessage):
        with st.chat_message(role):
            st.markdown(msg.content)

user_input = st.chat_input("Ask me anything...")

if user_input:
    st.session_state["messages"].append(HumanMessage(content=user_input))
    try:
        response = chat_model.invoke(st.session_state["messages"])
        ai_message = AIMessage(content=response.content)
        st.session_state["messages"].append(ai_message)
        with st.chat_message("assistant"):
            st.markdown(ai_message.content)
    except Exception as e:
        st.error(f"🚨 Error: {e}")

