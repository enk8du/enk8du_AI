
import json
import os
import streamlit as st

from chat.chat_handler import chat_with_ai
from video.video_handler import handle_video_request
from image.image_handler import handle_image_request

# --------------------------------
# PASSWORD
# --------------------------------

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


# --------------------------------
# MEMORY
# --------------------------------

MEMORY_FILE = "memory.json"

if os.path.exists(MEMORY_FILE):

    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        st.session_state.messages = json.load(f)

else:
    st.session_state.messages = []


# --------------------------------
# CHAT HISTORY
# --------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# --------------------------------
# USER INPUT
# --------------------------------

prompt = st.chat_input("اكتب رسالتك...")

if prompt:

    # رسالة المستخدم
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(
            st.session_state.messages,
            f,
            ensure_ascii=False,
            indent=2
        )

    with st.chat_message("user"):
        st.markdown(prompt)

    # --------------------------------
    # TASK ROUTER
    # --------------------------------

if "صورة" in prompt:

    reply = handle_image_request(prompt)

elif "فيديو" in prompt:

    reply = handle_video_request(prompt)

else:

    reply = chat_with_ai(
        st.session_state.messages
    )

    # --------------------------------
    # ASSISTANT REPLY
    # --------------------------------

    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })

    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(
            st.session_state.messages,
            f,
            ensure_ascii=False,
            indent=2
        )

    with st.chat_message("assistant"):
        st.markdown(reply)