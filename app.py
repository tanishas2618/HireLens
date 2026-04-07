import streamlit as st
import pdfplumber
import re
import matplotlib.pyplot as plt
from fpdf import FPDF

# ─── Page Config ─────────────────────────────
st.set_page_config(page_title="HireLens", page_icon="🔍")

st.title("🔍 HireLens - AI Resume Analyzer")

# ─── Upload ─────────────────────────────
uploaded_file = st.file_uploader("Upload your Resume (PDF only)", type=["pdf"])

if uploaded_file:

    # ─── Extract Text ─────────────────────
    text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            if page.extract_text():
                text += page.extract_text()

    clean_text = re.sub(r'\s+', ' ', text)

    st.subheader("📄 Extracted Resume Text")
    st.write(clean_text[:1000])

    # ─── AI Summary ─────────────────────
    st.subheader("🤖 Resume Summary")
    summary = " ".join(clean_text.split()[:50]) + "..."
    st.write(summary)

    # ─── Skills ─────────────────────
    skills_list = [
        "python", "java", "c", "c++",
        "html", "css", "javascript", "react",
        "node", "mongodb", "sql",
        "machine learning", "ai",
        "data analysis", "communication",
        "leadership", "problem solving"
    ]

    found_skills = [s for s in skills_list if s in clean_text.lower()]
    missing_skills = [s for s in skills_list if s not in found_skills]

    st.subheader("💡 Detected Skills")
    for skill in found_skills:
        st.write(f"✅ {skill}")

    # ─── Job Description ─────────────────────
    job_description = st.text_area("📌 Paste Job Description Here")

    if job_description:
        jd_words = job_description.lower().split()
        resume_words = clean_text.lower().split()

        matched_words = set(jd_words).intersection(set(resume_words))
        score = (len(matched_words) / len(set(jd_words))) * 100

        # ─── Score Display ─────────────────
        if score > 70:
            st.success(f"📊 ATS Score: {score:.2f}% - Strong Match")
        elif score > 40:
            st.warning(f"📊 ATS Score: {score:.2f}% - Medium Match")
        else:
            st.error(f"📊 ATS Score: {score:.2f}% - Weak Match")

        # ─── Chart ─────────────────
        st.subheader("📊 Skill Match Chart")
        matched_count = len(found_skills)
        missing_count = len(missing_skills)

        fig, ax = plt.subplots()
        ax.pie([matched_count, missing_count],
               labels=["Matched", "Missing"],
               autopct='%1.1f%%')
        st.pyplot(fig)

    # ─── Missing Skills ─────────────────────
    st.subheader("❌ Missing Skills")
    for skill in missing_skills[:8]:
        st.write(f"❌ {skill}")

    # ─── Suggestions ─────────────────────
    st.subheader("🧠 Suggestions")
    for skill in missing_skills[:5]:
        st.write(f"👉 Add {skill} by including projects or certifications")

    # ─── Download Report ─────────────────────
    if job_description:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, txt="HireLens Resume Report", ln=True)
        pdf.cell(200, 10, txt=f"ATS Score: {score:.2f}%", ln=True)

        pdf.cell(200, 10, txt="Skills Found:", ln=True)
        for s in found_skills:
            pdf.cell(200, 10, txt=s, ln=True)

        pdf.cell(200, 10, txt="Missing Skills:", ln=True)
        for s in missing_skills[:5]:
            pdf.cell(200, 10, txt=s, ln=True)

        pdf.output("report.pdf")

        with open("report.pdf", "rb") as f:
            st.download_button("📄 Download Report", f, file_name="report.pdf")

else:
    st.write("📄 Upload a resume to begin analysis")
