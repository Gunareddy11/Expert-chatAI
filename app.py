import os
import streamlit as st
from groq import Groq

# Load API key from environment variable
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    st.error("❌ GROQ_API_KEY not found. Please set it in .env or GitHub Secrets.")
    st.stop()

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

# ✅ Page setup
st.set_page_config(page_title="EXPERT Chat AI", page_icon="🤖", layout="centered")

# ✅ Static heading (always on top)
st.markdown(
    """
    <h1 style='text-align: center; color: #4CAF50;'>🤖 EXPERT Chat AI</h1>
    <hr>
    """,
    unsafe_allow_html=True
)

# Store chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display previous messages (scrollable)
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Type your message..."):
    # Add user message
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get AI response
    with st.chat_message("assistant"):
        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state["messages"]],
                temperature=0.7,
                max_tokens=512
            )
            reply = response.choices[0].message.content
            st.markdown(reply)

            # Save assistant reply
            st.session_state["messages"].append({"role": "assistant", "content": reply})

        except Exception as e:
            st.error(f"🚨 Error: {e}")
