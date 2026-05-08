from groq import Groq
import streamlit as st

client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)

def chat_with_ai(messages):

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=messages
    )

    return response.choices[0].message.content