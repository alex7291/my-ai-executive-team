import streamlit as st
from crewai import Agent, Task, Crew, Process
from langchain_groq import ChatGroq
import os

# --- SECURE API KEY HANDLING ---
if "GROQ_API_KEY" in st.secrets:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
else:
    st.error("⚠️ API Key পাওয়া যায়নি! দয়া করে Streamlit Cloud-এর Advanced Settings -> Secrets-এ GROQ_API_KEY যুক্ত করুন।")
    st.stop()

# AI মডেল সেটআপ
llm = ChatGroq(model_name="llama3-70b-8192")

# --- AI AGENTS DEFINITION ---
# এখানে allow_delegation=False করে দেওয়া হয়েছে যেন কনফ্লিক্ট না হয়
ceo = Agent(
    role='CEO',
    goal='Overall strategy, coordination, and final decision making.',
    backstory='You are a visionary leader. You lead the executive team to success.',
    llm=llm, 
    allow_delegation=False 
)

cfo = Agent(
    role='CFO',
    goal='Financial planning and budgeting.',
    backstory='You are a numbers expert and financial strategist.',
    llm=llm,
    allow_delegation=False
)

cto = Agent(
    role='CTO',
    goal='Technology stack and product development.',
    backstory='You are a tech genius and architecture expert.',
    llm=llm,
    allow_delegation=False
)

cmo = Agent(
    role='CMO',
    goal='Marketing and customer acquisition.',
    backstory='You are a marketing mastermind.',
    llm=llm,
    allow_delegation=False
)

creative_director = Agent(
    role='Creative Director',
    goal='Visual identity and design quality.',
    backstory='You are an expert in branding and UI/UX design.',
    llm=llm,
    allow_delegation=False
)

hr = Agent(
    role='HR Manager',
    goal='Company culture and team management.',
    backstory='You are an expert in human resources and organizational growth.',
    llm=llm,
    allow_delegation=False
)

# --- STREAMLIT UI ---
st.set_page_config(page_title="AI Executive Board", layout="wide", page_icon="🚀")
st.title("🚀 My AI Executive Board")
st.markdown("---")

user_input = st.text_area("আপনার বিজনেস আইডিয়া বা সমস্যাটি লিখুন:", height=150)

if st.button("টিমকে কাজ দাও"):
    if user_input:
        with st.spinner('আপনার এক্সিকিউটিভ টিম আলোচনা করছে...'):
            try:
                main_task = Task(
                    description=f"Analyze this request: {user_input}. Provide a detailed report from CEO, CFO, CTO, CMO, Creative Director, and HR.",
                    expected_output="A comprehensive multi-departmental business report.",
                    agent=ceo
                )

                company_crew = Crew(
                    agents=[ceo, cfo, cto, cmo, creative_director, hr],
                    tasks=[main_task],
                    process=Process.sequential
                )

                result = company_crew.kickoff()
                st.success("✅ রিপোর্ট তৈরি হয়েছে!")
                st.markdown(result)
                
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("দয়া করে কিছু লিখুন!")
