from groq import Groq
import streamlit as st

client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)

def chat_with_ai(messages):

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"ERROR: {str(e)}"