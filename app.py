import streamlit as st
from groq import Groq

# =========================
# إعداد الصفحة
# =========================
st.set_page_config(
    page_title="enk8du AI",
    page_icon="🤖",
    layout="centered"
)

# =========================
# جلب المفاتيح من Secrets
# =========================
api_key = st.secrets["GROQ_API_KEY"]
app_password = st.secrets["APP_PASSWORD"]

# =========================
# حماية بكلمة مرور
# =========================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:

    st.title("🔒 تسجيل الدخول")

    password = st.text_input(
        "ادخل كلمة المرور",
        type="password"
    )

    if st.button("دخول"):
        if password == app_password:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("كلمة المرور خطأ")

    st.stop()

# =========================
# تشغيل Groq
# =========================
client = Groq(api_key=api_key)

# =========================
# واجهة التطبيق
# =========================
st.title("enk8du AI")

if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسائل
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# إدخال المستخدم
prompt = st.chat_input("اكتب رسالتك...")

if prompt:

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    # رد الذكاء
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {
                "role": m["role"],
                "content": m["content"]
            }
            for m in st.session_state.messages
        ]
    )

    reply = response.choices[0].message.content

    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })

    with st.chat_message("assistant"):
        st.markdown(reply)