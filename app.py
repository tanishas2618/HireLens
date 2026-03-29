import streamlit as st
import pdfplumber
import re

# Title
st.set_page_config(page_title="HireLens", page_icon="🤖")

st.markdown("<h1 style='text-align: center;'>🤖 HireLens</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>AI Resume Analyzer</p>", unsafe_allow_html=True)
st.write("Upload your resume and analyze your skills!")

# Upload Resume
uploaded_file = st.file_uploader("📄 Upload your Resume (PDF only)", type=["pdf"])

if uploaded_file is not None:
    
    # 🔹 Extract Text
    text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            if page.extract_text():
                text += page.extract_text()

    # 🔹 Clean Text
    clean_text = re.sub(r'\s+', ' ', text)

    st.subheader("🧹 Cleaned Resume Text")
    st.write(clean_text)

    # 🔹 Skill Detection
    skills_list = [
        "python", "java", "c", "c++",
        "html", "css", "javascript", "react",
        "node", "mongodb", "sql",
        "machine learning", "ai",
        "data analysis", "communication",
        "leadership", "problem solving"
    ]

    found_skills = []

    for skill in skills_list:
        if skill.lower() in clean_text.lower():
            found_skills.append(skill)

    st.subheader("💡 Detected Skills")
    for skill in found_skills:
        st.write(f"✅ {skill}")

    # 🔹 Job Description Input
    job_description = st.text_area("📌 Paste Job Description Here")

    if job_description:
        jd_words = job_description.lower().split()
        resume_words = clean_text.lower().split()

        matched_words = set(jd_words).intersection(set(resume_words))

        score = (len(matched_words) / len(set(jd_words))) * 100

        if score > 70:
            st.success(f"📊 ATS Score: {score:.2f}% - Strong Match ✅")
        elif score > 40:
            st.warning(f"📊 ATS Score: {score:.2f}% - Medium Match ⚠️")
        else:
            st.error(f"📊 ATS Score: {score:.2f}% - Weak Match ❌")

    # 🔹 Missing Skills
    missing_skills = []

    for skill in skills_list:
        if skill not in found_skills:
            missing_skills.append(skill)

    st.subheader("❌ Missing Skills")
    for skill in missing_skills[:8]:
        st.write(f"❌ {skill}")

    # 🔹 Suggestions
    st.subheader("🧠 Suggestions")

    for skill in missing_skills[:5]:
        st.write(f"👉 Consider learning {skill}")
