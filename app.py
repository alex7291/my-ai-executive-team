import streamlit as st
import google.generativeai as genai
import os

# --- SECURITY: API KEY ---
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
else:
    st.error("⚠️ API Key missing!")
    st.stop()

# গুগল জেমিনাই কনফিগারেশন
genai.configure(api_key=api_key)

# মডেলের নাম পরিবর্তন করা হয়েছে (গুগলের অফিসিয়াল ফুল পাথ ব্যবহার করা হয়েছে)
try:
    model = genai.GenerativeModel('models/gemini-1.5-flash')
except Exception as e:
    st.error(f"Model Initialization Error: {e}")
    st.stop()

# --- AGENT CONFIGURATIONS ---
AGENTS = {
    "CEO ◈": "You are the Visionary CEO. Your tone is authoritative, inspiring, and decisive. You provide high-level strategic frameworks.",
    "CFO ⌬": "You are the CFO. Your tone is analytical and focused on financial architecture and profitability.",
    "CTO ⌂": "You are the CTO. Your tone is technical, innovative, and focused on infrastructure and scalability.",
    "CMO ⎈": "You are the CMO. Your tone is creative and focused on hyper-growth and brand dominance.",
    "Creative Director ✧": "You are the Creative Director. Your tone is artistic and focused on aesthetic perfection and UX.",
    "HR Manager ☊": "You are the HR Manager. Your tone is empathetic and focused on human capital and culture."
}

if "messages" not in st.session_state:
    st.session_state.messages = {agent: [] for agent in AGENTS.keys()}

if "current_agent" not in st.session_state:
    st.session_state.current_agent = "CEO ◈"

st.set_page_config(page_title="AI Executive Suite", layout="wide", page_icon="🌌")

# --- PREMIUM CSS ---
st.markdown("""
    <style>
        .stApp { background: radial-gradient(circle at top left, #1a1a1a, #000000); color: #E0E0E0; font-family: 'Inter', sans-serif; }
        [data-testid="stSidebar"] { background-color: rgba(10, 10, 10, 0.8) !important; backdrop-filter: blur(10px); border-right: 1px solid rgba(255, 255, 255, 0.1); }
        div.stButton > button { background-color: rgba(255, 255, 255, 0.05); color: #BBBBBB; border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 12px 20px; transition: all 0.4s; text-align: left; font-weight: 400; margin-bottom: 8px; }
        div.stButton > button:hover { background-color: rgba(255, 255, 255, 0.1); border-color: rgba(255, 255, 255, 0.3); color: #FFFFFF; transform: translateX(5px); }
        div.stButton > button[data-testid="stBaseButton-primary"] { background: linear-gradient(45deg, #FFFFFF, #BDBDBD) !important; color: #000000 !important; border: none !important; font-weight: 700 !important; box-shadow: 0 0 20px rgba(255, 255, 255, 0.3); }
        .stChatMessage { background-color: rgba(255, 255, 255, 0.03) !important; border-radius: 20px !important; border: 1px solid rgba(255, 255, 255, 0.05) !important; padding: 15px !important; margin-bottom: 20px !important; backdrop-filter: blur(5px); }
        h1 { font-weight: 800 !important; letter-spacing: -1px !important; background: linear-gradient(to right, #FFFFFF, #888888); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    </style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("🌌 Executive Suite")
    st.markdown("---")
    st.subheader("Board of Directors")
    for agent_name in AGENTS.keys():
        if st.button(agent_name, use_container_width=True, type="primary" if st.session_state.current_agent == agent_name else "secondary"):
            st.session_state.current_agent = agent_name
            st.rerun()
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("---")
    st.caption("Quantum Core: Gemini 1.5 Flash")

current_agent = st.session_state.current_agent
st.title(f"Interacting with {current_agent}")
st.markdown(f"*{AGENTS[current_agent]}*")
st.markdown("---")

for message in st.session_state.messages[current_agent]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input(f"Transmit message to {current_agent}..."):
    st.session_state.messages[current_agent].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Processing Quantum Intelligence..."):
            try:
                full_prompt = f"{AGENTS[current_agent]}\n\nUser: {prompt}\nAssistant:"
                response = model.generate_content(full_prompt)
                ai_message = response.text
                st.markdown(ai_message)
                st.session_state.messages[current_agent].append({"role": "assistant", "content": ai_message})
            except Exception as e:
                st.error(f"Transmission Error: {e}")
