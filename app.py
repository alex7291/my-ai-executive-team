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

# --- STREAMLIT UI ---
st.set_page_config(page_title="AI Executive Board", layout="wide", page_icon="🚀")
st.title("🚀 My AI Executive Board")
st.markdown("---")
st.subheader("আপনার ভার্চুয়াল বোর্ড অফ ডিরেক্টরস এখানে প্রস্তুত")

user_input = st.text_area("আপনার বিজনেস আইডিয়া বা সমস্যাটি লিখুন:", height=150)

if st.button("টিমকে কাজ দাও"):
    if user_input:
        with st.spinner('আপনার এক্সিকিউটিভ টিম আলোচনা করছে...'):
            try:
                # আমরা এখানে একটি প্রফেশনাল প্রম্পট ব্যবহার করছি যা AI-কে ৬টি ভিন্ন চরিত্রে কথা বলতে বাধ্য করবে
                system_prompt = (
                    "You are a Virtual Board of Directors consisting of a CEO, CFO, CTO, CMO, Creative Director, and HR Manager. "
                    "For the given user request, provide a comprehensive and detailed response. "
                    "You MUST structure your answer as follows:\n\n"
                    "1. 👔 **CEO's Strategic Vision**: (Overall direction and final decision)\n"
                    "2. 💰 **CFO's Financial Plan**: (Budget, costs, and revenue streams)\n"
                    "3. 💻 **CTO's Technical Roadmap**: (Tech stack, development, and infrastructure)\n"
                    "4. 📢 **CMO's Growth Strategy**: (Marketing, branding, and customer acquisition)\n"
                    "5. 🎨 **Creative Director's Visual Identity**: (UI/UX, design, and branding)\n"
                    "6. 👥 **HR's Organizational Structure**: (Hiring, team culture, and roles)\n\n"
                    "Be professional, detailed, and actionable. User request: "
                )
                
                full_prompt = system_prompt + user_input
                response = llm.invoke(full_prompt)
                
                st.success("✅ আপনার টিমের রিপোর্ট তৈরি হয়েছে!")
                st.markdown("---")
                st.markdown("### 📋 Final Executive Report")
                st.markdown(response.content)
                
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("দয়া করে কিছু লিখুন!")

st.markdown("---")
st.caption("Powered by Groq Llama 3 - Stable Version")
