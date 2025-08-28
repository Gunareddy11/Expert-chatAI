import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# Initialize Groq client
client = Groq(api_key=api_key)

# Streamlit UI setup
st.set_page_config(page_title="Chatbot with Groq", page_icon="🤖", layout="wide")
st.title("🤖 Chatbot (Groq + Streamlit)")

# Session state for chat messages
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "You are a helpful AI assistant."}
    ]

# Display previous chat history
for message in st.session_state["messages"]:
    if message["role"] == "user":
        st.chat_message("user").markdown(message["content"])
    elif message["role"] == "assistant":
        st.chat_message("assistant").markdown(message["content"])

# User input
if prompt := st.chat_input("Ask me anything..."):
    # Save user input
    st.session_state["messages"].append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)

    # ✅ Token truncation fix (avoid 413 error)
    MAX_HISTORY = 8  # keep system + last 7 turns
    if len(st.session_state["messages"]) > MAX_HISTORY:
        st.session_state["messages"] = (
            [st.session_state["messages"][0]]  # keep system
            + st.session_state["messages"][-(MAX_HISTORY - 1):]
        )

    try:
        # Call Groq API
        chat_completion = client.chat.completions.create(
            messages=st.session_state["messages"],
            model="llama-3.3-70b-versatile",  # You can switch to mistral-saba-24b if still heavy
            temperature=0.7,
            max_tokens=800,
        )

        # Extract response
        reply = chat_completion.choices[0].message["content"]
        st.session_state["messages"].append({"role": "assistant", "content": reply})
        st.chat_message("assistant").markdown(reply)

    except Exception as e:
        st.error(f"🚨 Error: {str(e)}")
