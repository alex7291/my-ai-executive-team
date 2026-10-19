import streamlit as st
from langchain_groq import ChatGroq
import os

# --- SECURITY: API KEY ---
if "GROQ_API_KEY" in st.secrets:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
else:
    st.error("⚠️ API Key পাওয়া যায়নি! দয়া করে Secrets-এ GROQ_API_KEY যুক্ত করুন।")
    st.stop()

# AI মডেল সেটআপ
llm = ChatGroq(model_name="llama3-70b-8192")

# --- AGENT CONFIGURATIONS ---
AGENTS = {
    "CEO 👔": "You are the CEO. Your tone is visionary, decisive, and strategic. You focus on the big picture.",
    "CFO 💰": "You are the CFO. Your tone is analytical, cautious, and focused on numbers and profitability.",
    "CTO 💻": "You are the CTO. Your tone is technical, innovative, and focused on scalability and architecture.",
    "CMO 📢": "You are the CMO. Your tone is creative, energetic, and focused on growth and branding.",
    "Creative Director 🎨": "You are the Creative Director. Your tone is artistic, detailed, and focused on aesthetics and UX.",
    "HR Manager 👥": "You are the HR Manager. Your tone is empathetic, organized, and focused on people and culture."
}

# --- SESSION STATE INITIALIZATION ---
# চ্যাট হিস্ট্রি সেভ করার জন্য
if "messages" not in st.session_state:
    st.session_state.messages = {agent: [] for agent in AGENTS.keys()}

if "current_agent" not in st.session_state:
    st.session_state.current_agent = "CEO 👔"

# --- UI DESIGN ---
st.set_page_config(page_title="AI Executive Board", layout="wide", page_icon="🚀")

# কাস্টম CSS দিয়ে ইন্টারফেসটি সুন্দর করা (Dark Mode Style)
st.markdown("""
    <style>
        .stApp { background-color: #0E1117; color: white; }
        [data-testid="stSidebar"] { background-color: #161B22; }
        .stChatMessage { border-radius: 15px; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR (The Agent List) ---
with st.sidebar:
    st.title("🏢 My Company")
    st.markdown("---")
    st.subheader("Executive Team")
    
    # এজেন্টের লিস্ট তৈরি এবং সিলেক্ট করা
    for agent_name in AGENTS.keys():
        if st.button(agent_name, use_container_width=True, 
                    type="primary" if st.session_state.current_agent == agent_name else "secondary"):
            st.session_state.current_agent = agent_name
            st.rerun()
    
    st.markdown("---")
    st.caption("Powered by Groq Llama 3")

# --- MAIN CHAT AREA ---
current_agent = st.session_state.current_agent
st.title(f"Chat with {current_agent}")
st.markdown(f"*{AGENTS[current_agent]}*")
st.markdown("---")

# বর্তমান এজেন্টের চ্যাট হিস্ট্রি দেখানো
for message in st.session_state.messages[current_agent]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ইউজার ইনপুট (Chat Input)
if prompt := st.chat_input(f"Message {current_agent}..."):
    # ইউজারের মেসেজ সেভ এবং ডিসপ্লে
    st.session_state.messages[current_agent].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI-এর রেসপন্স তৈরি
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # এজেন্টের ব্যক্তিত্ব অনুযায়ী প্রম্পট তৈরি
                full_prompt = f"{AGENTS[current_agent]}\n\nUser: {prompt}\nAssistant:"
                response = llm.invoke(full_prompt)
                ai_message = response.content
                
                st.markdown(ai_message)
                # AI-এর মেসেজ সেভ করা
                st.session_state.messages[current_agent].append({"role": "assistant", "content": ai_message})
            except Exception as e:
                st.error(f"Error: {e}")

