# app.py
import streamlit as st

from assistant import (
    get_answer,
    get_categories,
    get_feedback_stats,
    save_feedback,
    df,
)
from auth import register_user, verify_user

st.set_page_config(page_title="College AI Assistant", page_icon="🎓", layout="centered")

CATEGORY_STYLE = {
    "General": ("🏫", "#6C5CE7"),
    "Academics": ("📚", "#0984E3"),
    "Exams": ("📝", "#E17055"),
    "Fees": ("💳", "#00B894"),
    "Scholarships": ("🎖️", "#FDCB6E"),
    "Library": ("📖", "#A29BFE"),
    "Certificates": ("📜", "#FD79A8"),
    "Hostel": ("🏠", "#00CEC9"),
    "Placements": ("💼", "#D63031"),
    "Transport": ("🚌", "#E84393"),
    "Clubs": ("🎯", "#55EFC4"),
}

QUICK_QUESTIONS = {
    "📝 Exam dates": "When are the semester exams held?",
    "💳 Fee deadline": "What is the last date to pay the semester fee?",
    "📖 Library timings": "What are the library timings?",
    "✅ Attendance rule": "What is the minimum attendance required to write exams?",
    "🎖️ Scholarships": "What scholarships are available?",
    "💼 Placements": "When do campus placements start?",
    "🏠 Hostel": "Is hostel accommodation available?",
    "🚌 Bus facility": "Does the college provide a bus facility?",
}


def style_for(cat):
    return CATEGORY_STYLE.get(cat, ("✨", "#636E72"))


def handle_query(query):
    answer, cat, score = get_answer(query)
    st.session_state.messages.append({"role": "user", "content": query})
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "category": cat,
            "question": query,
            "rating": None,
        }
    )


st.markdown(
    """
<style>
.stApp {
    background: linear-gradient(135deg, #f5f7ff 0%, #fdf2ff 50%, #fff5f0 100%);
}
.hero {
    background: linear-gradient(90deg, #6C5CE7, #0984E3, #00CEC9);
    padding: 28px 20px;
    border-radius: 18px;
    text-align: center;
    color: white;
    box-shadow: 0 8px 24px rgba(108, 92, 231, 0.35);
    margin-bottom: 22px;
}
.hero h1 { margin: 0; font-size: 2.2rem; color: white; }
.hero p { margin: 6px 0 0 0; opacity: 0.95; font-size: 1.05rem; }
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #2d3436 0%, #6C5CE7 100%);
}
section[data-testid="stSidebar"] * { color: white !important; }
[data-testid="stChatMessage"] {
    background: white;
    border-radius: 16px;
    padding: 12px 16px;
    margin-bottom: 10px;
    box-shadow: 0 3px 12px rgba(0, 0, 0, 0.08);
}
.badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 999px;
    color: white;
    font-size: 0.8rem;
    font-weight: 600;
    margin-top: 8px;
}
.chip {
    display: inline-block;
    padding: 6px 12px;
    margin: 4px 4px 0 0;
    border-radius: 12px;
    background: rgba(255, 255, 255, 0.18);
    font-size: 0.85rem;
}
.stButton > button, .stFormSubmitButton > button {
    border-radius: 999px;
    border: 1.5px solid #6C5CE7;
    background: white;
    color: #6C5CE7;
    font-weight: 600;
}
.stButton > button:hover, .stFormSubmitButton > button:hover {
    background: #6C5CE7;
    color: white;
    border-color: #6C5CE7;
}

/* ===== NEW: Logout button colour ===== */
.st-key-logout_btn .stButton > button {
    background: linear-gradient(90deg, #ff512f, #dd2476) !important;
    color: white !important;
    border: none !important;
}
.st-key-logout_btn .stButton > button:hover {
    background: linear-gradient(90deg, #dd2476, #ff512f) !important;
    transform: scale(1.02);
}

/* ===== NEW: "Choose a category" selectbox colour ===== */
section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
    background-color: #ffe9a8 !important;
    border: 2px solid #f5b700 !important;
    border-radius: 12px !important;
}
section[data-testid="stSidebar"] div[data-baseweb="select"] * {
    color: #333 !important;
}
section[data-testid="stSidebar"] div[data-baseweb="select"] svg {
    fill: #333 !important;
}

/* Dropdown list (opens outside the sidebar) */
ul[role="listbox"] { background-color: #fff7d6 !important; }
ul[role="listbox"] li { color: #333 !important; }
ul[role="listbox"] li:hover { background-color: #ffd54f !important; }
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="hero">
    <h1>🎓 College AI Assistant</h1>
    <p>Your quick guide to exams, fees, library, hostel, placements and more ✨</p>
</div>
""",
    unsafe_allow_html=True,
)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "user" not in st.session_state:
    st.session_state.user = None


# ---------- Login / Sign up page ----------
def show_login():
    tab_login, tab_signup = st.tabs(["🔑 Login", "📝 Sign up"])

    with tab_login:
        with st.form("login_form"):
            email = st.text_input("📧 Email", placeholder="you@example.com")
            password = st.text_input("🔒 Password", type="password")
            submitted = st.form_submit_button("Login", use_container_width=True)
        if submitted:
            if verify_user(email, password):
                st.session_state.user = email.strip().lower()
                st.rerun()
            else:
                st.error("Invalid email or password.")

    with tab_signup:
        with st.form("signup_form"):
            new_email = st.text_input("📧 Email", placeholder="you@example.com", key="su_email")
            new_pass = st.text_input("🔒 Password (min 8 characters)", type="password", key="su_pass")
            confirm = st.text_input("🔒 Confirm password", type="password", key="su_confirm")
            created = st.form_submit_button("Create account", use_container_width=True)
        if created:
            ok, msg = register_user(new_email, new_pass, confirm)
            if ok:
                st.success(msg)
            else:
                st.error(msg)


if not st.session_state.user:
    show_login()
    st.stop()

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown(f"👤 **{st.session_state.user}**")
    if st.button("🚪 Logout", use_container_width=True, key="logout_btn"):  # key added
        st.session_state.user = None
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.markdown("## 🧭 Browse Topics")
    category = st.selectbox("Choose a category", ["All"] + get_categories())
    subset = df if category == "All" else df[df["category"] == category]

    st.markdown("### 💡 Sample questions")
    for q in subset["question"].head(5):
        st.markdown(f'<span class="chip">❓ {q}</span>', unsafe_allow_html=True)

    st.markdown("---")
    total, helpful = get_feedback_stats()
    st.markdown("### 📊 Feedback")
    if total:
        st.markdown(f"{total} ratings · {helpful / total:.0%} helpful")
    else:
        st.markdown("No ratings yet")

    st.markdown("---")
    if st.button("🗑️ Clear chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


def render(idx, m):
    role = m["role"]
    avatar = "🧑‍🎓" if role == "user" else "🤖"
    with st.chat_message(role, avatar=avatar):
        st.markdown(m["content"])

        cat = m.get("category")
        if cat:
            icon, color = style_for(cat)
            st.markdown(
                f'<span class="badge" style="background:{color}">{icon} {cat}</span>',
                unsafe_allow_html=True,
            )

        if role == "assistant" and "question" in m:
            if m.get("rating") is None:
                c1, c2, _ = st.columns([1, 1, 6])
                if c1.button("👍", key=f"up_{idx}"):
                    save_feedback(m["question"], m["content"], cat, "helpful")
                    m["rating"] = "helpful"
                    st.rerun()
                if c2.button("👎", key=f"down_{idx}"):
                    save_feedback(m["question"], m["content"], cat, "not helpful")
                    m["rating"] = "not helpful"
                    st.rerun()
            else:
                st.caption("Thanks for your feedback! 🙏")


# ---------- Chat ----------
if not st.session_state.messages:
    with st.chat_message("assistant", avatar="🤖"):
        st.markdown("Hi! 👋 I'm your college assistant. Ask me anything about college life.")

    st.markdown("#### ⚡ Quick questions")
    items = list(QUICK_QUESTIONS.items())
    for row_start in range(0, len(items), 2):
        cols = st.columns(2)
        for col, (label, question) in zip(cols, items[row_start:row_start + 2]):
            if col.button(label, key=f"quick_{label}", use_container_width=True):
                handle_query(question)
                st.rerun()

for i, m in enumerate(st.session_state.messages):
    render(i, m)

if query := st.chat_input("Ask about college... 💬"):
    handle_query(query)
    st.rerun()