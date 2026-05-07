import streamlit as st
from groq import Groq

# -----------------------------
# API
# -----------------------------
client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)

# -----------------------------
# PASSWORD
# -----------------------------
APP_PASSWORD = st.secrets["APP_PASSWORD"]

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:

    password = st.text_input("ادخل الباسورد", type="password")

    if password:
        if password == APP_PASSWORD:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("الباسورد خطأ")

    st.stop()

# -----------------------------
# CHAT HISTORY
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسائل القديمة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------
# USER INPUT
# -----------------------------
prompt = st.chat_input("اكتب رسالتك...")

if prompt:

    # عرض رسالة المستخدم
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    # ارسال الى Groq
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": m["role"],
                "content": m["content"]
            }
            for m in st.session_state.messages
        ]
    )

    reply = response.choices[0].message.content

    # حفظ الرد
    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })

    # عرض الرد
    with st.chat_message("assistant"):
        st.markdown(reply)