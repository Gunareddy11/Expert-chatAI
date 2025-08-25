import os
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

from langchain_groq import ChatGroq

llamaChatModel = ChatGroq(
    model="llama3-70b-8192"
)

mistralChatModel = ChatGroq(
    model="mixtral-8x7b-32768"
)

messages = [
    ("system", "You are an expert tell me about rohit sharma."),
    ("human", "How many runs he scored international odi cricket?"),
]

llamaResponse = llamaChatModel.invoke(messages)
print(llamaResponse.content)