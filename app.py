import streamlit as st
from crewai import Agent, Task, Crew, Process
from langchain_groq import ChatGroq
import os

# --- SECURE API KEY HANDLING ---
# এখানে আমরা সরাসরি কী লিখছি না, বরং Streamlit-এর Secrets থেকে নিচ্ছি
if "GROQ_API_KEY" in st.secrets:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
else:
    st.error("⚠️ API Key পাওয়া যায়নি! দয়া করে Streamlit Cloud-এর Advanced Settings -> Secrets-এ GROQ_API_KEY যুক্ত করুন।")
    st.stop()

# AI মডেল সেটআপ (Llama 3 - সুপার ফাস্ট)
llm = ChatGroq(model_name="llama3-70b-8192")

# --- AI AGENTS DEFINITION ---
ceo = Agent(
    role='CEO',
    goal='Overall strategy, coordination, and final decision making.',
    backstory='You are a visionary leader. You coordinate between the CFO, CTO, CMO, Creative Director, and HR to ensure the company hits its goals.',
    llm=llm, allow_delegation=True
)

cfo = Agent(
    role='CFO',
    goal='Financial planning, budgeting, and profit maximization.',
    backstory='You are a numbers expert. You analyze costs, pricing strategies, and financial risks.',
    llm=llm
)

cto = Agent(
    role='CTO',
    goal='Technology stack, product development, and technical architecture.',
    backstory='You are a tech genius. You decide which software, language, and tools the company should use.',
    llm=llm
)

cmo = Agent(
    role='CMO',
    goal='Marketing, customer acquisition, and brand growth.',
    backstory='You are a marketing mastermind. You know how to make a product go viral and attract customers.',
    llm=llm
)

creative_director = Agent(
    role='Creative Director',
    goal='Visual identity, UI/UX, and design quality.',
    backstory='You are an art and design expert. You ensure everything the company produces looks stunning and professional.',
    llm=llm
)

hr = Agent(
    role='HR Manager',
    goal='Company culture, hiring, and employee management.',
    backstory='You are a people person. You manage the virtual and human team, setting policies and performance metrics.',
    llm=llm
)

# --- STREAMLIT UI ---
st.set_page_config(page_title="AI Executive Board", layout="wide", page_icon="🚀")

st.title("🚀 My AI Executive Board")
st.markdown("---")
st.subheader("আপনার ভার্চুয়াল বোর্ড অফ ডিরেক্টরস এখানে প্রস্তুত")
st.info("CEO, CFO, CTO, CMO, Creative Director এবং HR-এর সমন্বয়ে গঠিত এই টিম আপনার ব্যবসার যেকোনো সমস্যার সমাধান দিতে পারে।")

user_input = st.text_area("আপনার বিজনেস আইডিয়া বা সমস্যাটি বিস্তারিত লিখুন:", 
                          placeholder="উদাহরণ: আমি একটি ই-কমার্স কোম্পানি শুরু করতে চাই, আমার জন্য একটি পূর্ণাঙ্গ রোডম্যাপ এবং বাজেট প্ল্যান দাও।",
                          height=150)

if st.button("টিমকে কাজ দাও"):
    if user_input:
        with st.spinner('আপনার এক্সিকিউটিভ টিম আলোচনা করছে... দয়া করে অপেক্ষা করুন...'):
            try:
                main_task = Task(
                    description=f"Analyze this request and provide a comprehensive business solution: {user_input}. "
                                f"The CEO should coordinate and synthesize the final answer. "
                                f"CFO must provide financial insights, CTO provide tech stack, "
                                f"CMO provide marketing strategy, Creative Director provide branding ideas, "
                                f"and HR provide organizational structure.",
                    expected_output="A detailed, professionally formatted multi-departmental report with specific action points from each executive.",
                    agent=ceo
                )

                company_crew = Crew(
                    agents=[ceo, cfo, cto, cmo, creative_director, hr],
                    tasks=[main_task],
                    process=Process.sequential
                )

                result = company_crew.kickoff()
                st.success("✅ আপনার টিমের রিপোর্ট তৈরি হয়েছে!")
                st.markdown("---")
                st.markdown("### 📋 Final Executive Report")
                st.markdown(result)
                
            except Exception as e:
                st.error(f"একটি সমস্যা হয়েছে: {e}")
    else:
        st.warning("দয়া করে কিছু লিখুন!")

st.markdown("---")
st.caption("Powered by Groq Llama 3 & CrewAI")
