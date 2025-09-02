import os
import streamlit as st
from groq import Groq

# Load API key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    st.error("❌ GROQ_API_KEY not found. Please set it in .env or GitHub Secrets.")
    st.stop()

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

# Streamlit Page Setup
st.set_page_config(page_title="EXPERT Chat AI", page_icon="🤖", layout="centered")

# 🔹 Always show heading (sticky header)
st.markdown(
    """
    <div style="position:fixed; top:0; width:100%; background:white; padding:10px; 
    border-bottom:2px solid #eee; z-index:1000; text-align:center;">
        <h2>🤖 EXPERT Chat AI</h2>
    </div>
    <div style="margin-top:80px;"></div>
    """,
    unsafe_allow_html=True
)

# Store chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display chat history
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Type your message..."):
    # Add user input
    st.session_state["messages"].append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # Use full history (instead of just last 5) but cap at 30 messages
    history = st.session_state["messages"][-30:]

    with st.chat_message("assistant"):
        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": m["role"], "content": m["content"]} for m in history],
                temperature=0.5,   # lower = more focused, factual
                max_tokens=1200    # allow longer answers
            )

            reply = response.choices[0].message.content
            st.markdown(reply)

            # Save assistant response
            st.session_state["messages"].append({"role": "assistant", "content": reply})

        except Exception as e:
            st.error(f"🚨 Error: {e}")
