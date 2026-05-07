import streamlit as st
from groq import Groq
import requests
import json
import os

# =========================
# الصفحة
# =========================

st.set_page_config(
    page_title="enk8du AI",
    layout="wide"
)

st.title("enk8du AI")

# =========================
# API
# =========================

api_key = st.secrets["GROQ_API_KEY"]

client = Groq(api_key=api_key)

# =========================
# ذاكرة
# =========================

MEMORY_FILE = "memory.json"

def load_memory():

    if os.path.exists(MEMORY_FILE):

        with open(MEMORY_FILE, "r", encoding="utf-8") as f:

            return json.load(f)

    return []

def save_memory(messages):

    with open(MEMORY_FILE, "w", encoding="utf-8") as f:

        json.dump(
            messages,
            f,
            ensure_ascii=False,
            indent=2
        )

# =========================
# بحث ويب
# =========================

def web_search(query):

    try:

        url = f"https://api.duckduckgo.com/?q={query}&format=json"

        response = requests.get(url)

        data = response.json()

        abstract = data.get("AbstractText", "")

        if abstract:
            return abstract

        return "لم أجد نتائج واضحة من الإنترنت."

    except:
        return "حدث خطأ أثناء البحث."

# =========================
# تحميل الذاكرة
# =========================

if "messages" not in st.session_state:

    st.session_state.messages = load_memory()

# =========================
# عرض المحادثة
# =========================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# =========================
# إدخال المستخدم
# =========================

prompt = st.chat_input("اكتب رسالتك...")

if prompt:

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):

        st.markdown(prompt)

    # =========================
    # بحث بالنت
    # =========================

    internet_result = ""

    keywords = [
        "ابحث",
        "بحث",
        "النت",
        "جوجل",
        "google"
    ]

    if any(word in prompt for word in keywords):

        internet_result = web_search(prompt)

    # =========================
    # النظام
    # =========================

    system_prompt = {
        "role": "system",
        "content": f"""
أنت مساعد ذكي اسمك enk8du AI.

تصرف مثل مساعد احترافي متطور.
حلل كلام المستخدم بعمق.
تذكر المحادثة السابقة.
ساعد المستخدم باقتراحات مفيدة.
جاوب بطريقة طبيعية.
لا تكن روبوتيًا.

إذا توجد معلومات من الإنترنت استخدمها:

{internet_result}
"""
    }

    recent_memory = st.session_state.messages[-20:]

    messages = [system_prompt]

    messages.extend(recent_memory)

    with st.chat_message("assistant"):

        try:

            response = client.chat.completions.create(

                model="llama-3.3-70b-versatile",

                messages=messages,

                temperature=0.7,

                max_tokens=1024
            )

            reply = response.choices[0].message.content

            st.markdown(reply)

            st.session_state.messages.append({
                "role": "assistant",
                "content": reply
            })

            save_memory(
                st.session_state.messages
            )

        except Exception as e:

            st.error(f"خطأ: {e}")

# =========================
# حذف الذاكرة
# =========================

if st.sidebar.button("🗑 حذف الذاكرة"):

    st.session_state.messages = []

    if os.path.exists(MEMORY_FILE):

        os.remove(MEMORY_FILE)

    st.rerun()