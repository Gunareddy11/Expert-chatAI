explain the code import os
import streamlit as st
from groq import Groq

# Load API key from environment variable
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    st.error("❌ GROQ_API_KEY not found. Please set it in .env or GitHub Secrets.")
    st.stop()

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

# Streamlit UI
st.set_page_config(page_title="EXPERT Chat AI", page_icon="🤖", layout="centered")
st.title("🤖 EXPERT Chat AI")

# Store chat history in Streamlit session
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display previous messages
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])   # ✅ fixed (no object subscript issue)

# Chat input
if prompt := st.chat_input("Type your message..."):
    # Add user message to session
    st.session_state["messages"].append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response from Groq
    with st.chat_message("assistant"):
        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",   # ✅ safe model
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state["messages"]
                ],
                temperature=0.7,
                max_tokens=512
            )

            reply = response.choices[0].message.content  # ✅ fixed
            st.markdown(reply)

            # Add assistant response to session
            st.session_state["messages"].append({"role": "assistant", "content": reply})

        except Exception as e:
            st.error(f"🚨 Error: {e}")


