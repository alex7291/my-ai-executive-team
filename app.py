import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
import os

# --- SECURITY: API KEY ---
if "GOOGLE_API_KEY" in st.secrets:
    os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
else:
    st.error("⚠️ API Key পাওয়া যায়নি! দয়া করে Secrets-এ GOOGLE_API_KEY যুক্ত করুন।")
    st.stop()

# AI মডেল সেটআপ (Gemini 1.5 Flash - Strong, Fast & Free)
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

# --- AGENT CONFIGURATIONS ---
AGENTS = {
    "CEO 👔": (
        "You are the Visionary CEO. Your goal is to scale the business globally. "
        "You provide strategic frameworks, analyze risks, and think 10 steps ahead. "
        "Your tone is authoritative, inspiring and decisive."
    ),
    "CFO 💰": "You are the CFO. Your tone is analytical and focused on profitability and budgets.",
    "CTO 💻": "You are the CTO. Your tone is technical and focused on scalability and innovation.",
    "CMO 📢": "You are the CMO. Your tone is creative and focused on growth and branding.",
    "Creative Director 🎨": "You are the Creative Director. Your tone is artistic and focused on UX/UI.",
    "HR Manager 👥": "You are the HR Manager. Your tone is empathetic and focused on people and culture."
}

if "messages" not in st.session_state:
    st.session_state.messages = {agent: [] for agent in AGENTS.keys()}

if "current_agent" not in st.session_state:
    st.session_state.current_agent = "CEO 👔"

st.set_page_config(page_title="AI Executive Board", layout="wide", page_icon="🚀")

st.markdown("""
    <style>
        .stApp { background-color: #0E1117; color: white; }
        [data-testid="stSidebar"] { background-color: #161B22; }
        .stChatMessage { border-radius: 15px; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("🏢 My Company")
    st.markdown("---")
    st.subheader("Executive Team")
    for agent_name in AGENTS.keys():
        if st.button(agent_name, use_container_width=True, 
                    type="primary" if st.session_state.current_agent == agent_name else "secondary"):
            st.session_state.current_agent = agent_name
            st.rerun()
    st.markdown("---")
    st.caption("Powered by Google Gemini 1.5 Flash")

current_agent = st.session_state.current_agent
st.title(f"Chat with {current_agent}")
st.markdown(f"*{AGENTS[current_agent]}*")
st.markdown("---")

for message in st.session_state.messages[current_agent]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input(f"Message {current_agent}..."):
    st.session_state.messages[current_agent].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                full_prompt = f"{AGENTS[current_agent]}\n\nUser: {prompt}\nAssistant:"
                response = llm.invoke(full_prompt)
                ai_message = response.content
                st.markdown(ai_message)
                st.session_state.messages[current_agent].append({"role": "assistant", "content": ai_message})
            except Exception as e:
                st.error(f"Error: {e}")
