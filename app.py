import streamlit as st
from dotenv import load_dotenv, find_dotenv
from langchain_groq import ChatGroq




# Load API key from .env
_ = load_dotenv(find_dotenv())

# Sidebar to choose model
st.sidebar.title("⚙️ Settings")
model_choice = st.sidebar.selectbox(
    "Choose a model",
    ["llama3-70b-8192", "mixtral-8x7b-32768"]
)

# Initialize selected model
chat_model = ChatGroq(model=model_choice)

# Streamlit app UI
st.set_page_config(page_title="Expert Chat AI", page_icon="🤖")


st.title( "🤖Expert Chat AI - Ask anything")

# Initialize conversation history
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        ("system", "You are an expert . Answer user asking questions.")
    ]

# Display conversation history
for role, content in st.session_state["messages"]:
    if role == "human":
        with st.chat_message("user"):
            st.markdown(content)
    elif role == "ai":
        with st.chat_message("assistant"):
            st.markdown(content)

# User input box
user_input = st.chat_input("Ask anything...")

if user_input:
    # Append user input
    st.session_state["messages"].append(("human", user_input))

    # Get response
    response = chat_model.invoke(st.session_state["messages"])
    ai_message = response.content

    # Append AI response
    st.session_state["messages"].append(("ai", ai_message))

    # Display AI response
    with st.chat_message("assistant"):
        st.markdown(ai_message)
