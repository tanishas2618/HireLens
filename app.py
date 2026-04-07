import streamlit as st
import pdfplumber
import re

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(page_title="HireLens", page_icon="🔍", layout="centered")

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

* { font-family: 'DM Sans', sans-serif; }

/* ── Background ── */
.stApp {
    background: #0a0a0f;
    background-image:
        radial-gradient(ellipse 60% 40% at 70% 10%, rgba(99,60,255,0.18) 0%, transparent 60%),
        radial-gradient(ellipse 50% 30% at 20% 80%, rgba(0,200,150,0.10) 0%, transparent 60%);
}

/* ── Hero ── */
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 3.4rem;
    font-weight: 800;
    letter-spacing: -2px;
    background: linear-gradient(120deg, #fff 30%, #a78bfa 70%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    margin-bottom: 0;
    line-height: 1.1;
}
.hero-sub {
    font-family: 'DM Sans', sans-serif;
    font-weight: 300;
    font-size: 1.05rem;
    color: #888;
    text-align: center;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-top: 6px;
    margin-bottom: 2rem;
}
.hero-divider {
    width: 60px;
    height: 2px;
    background: linear-gradient(90deg, #7c3aed, #10b981);
    margin: 0 auto 2.5rem;
    border-radius: 2px;
}

/* ── Cards ── */
.card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1.2rem;
    backdrop-filter: blur(10px);
}
.card-title {
    font-family: 'Syne', sans-serif;
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    color: #a78bfa;
    margin-bottom: 0.8rem;
}

/* ── Skill pills ── */
.skills-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 4px;
}
.skill-pill {
    background: rgba(16, 185, 129, 0.12);
    border: 1px solid rgba(16,185,129,0.35);
    color: #34d399;
    padding: 5px 14px;
    border-radius: 999px;
    font-size: 0.82rem;
    font-weight: 500;
    letter-spacing: 0.02em;
}
.skill-missing {
    background: rgba(239,68,68,0.10);
    border: 1px solid rgba(239,68,68,0.30);
    color: #f87171;
    padding: 5px 14px;
    border-radius: 999px;
    font-size: 0.82rem;
    font-weight: 500;
}

/* ── ATS Score ── */
.score-wrap {
    text-align: center;
    padding: 1rem 0 0.5rem;
}
.score-number {
    font-family: 'Syne', sans-serif;
    font-size: 4rem;
    font-weight: 800;
    letter-spacing: -3px;
    line-height: 1;
}
.score-strong { color: #34d399; }
.score-medium { color: #fbbf24; }
.score-weak   { color: #f87171; }

.score-label {
    font-size: 0.85rem;
    font-weight: 500;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-top: 6px;
    margin-bottom: 1rem;
}
.bar-bg {
    background: rgba(255,255,255,0.08);
    border-radius: 999px;
    height: 8px;
    width: 100%;
    overflow: hidden;
    margin: 0 auto;
}
.bar-fill-strong { background: linear-gradient(90deg, #059669, #34d399); border-radius: 999px; height: 100%; }
.bar-fill-medium { background: linear-gradient(90deg, #d97706, #fbbf24); border-radius: 999px; height: 100%; }
.bar-fill-weak   { background: linear-gradient(90deg, #dc2626, #f87171); border-radius: 999px; height: 100%; }

/* ── Suggestions ── */
.suggestion-item {
    background: rgba(124,58,237,0.10);
    border-left: 3px solid #7c3aed;
    border-radius: 0 10px 10px 0;
    padding: 10px 16px;
    margin-bottom: 8px;
    font-size: 0.9rem;
    color: #c4b5fd;
    font-weight: 400;
}

/* ── Streamlit overrides ── */
.stFileUploader > div {
    background: rgba(255,255,255,0.03) !important;
    border: 1px dashed rgba(167,139,250,0.4) !important;
    border-radius: 14px !important;
}
.stTextArea textarea {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.10) !important;
    border-radius: 12px !important;
    color: #e2e8f0 !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stTextArea textarea:focus {
    border-color: rgba(167,139,250,0.6) !important;
    box-shadow: 0 0 0 3px rgba(124,58,237,0.15) !important;
}
div[data-testid="stExpander"] {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
}
label, .stTextArea label { color: #aaa !important; font-size: 0.85rem !important; }
p { color: #cbd5e1; }

/* ── Section label ── */
.section-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.16em;
    color: #6b7280;
    margin-bottom: 0.5rem;
    margin-top: 2rem;
}
</style>
""", unsafe_allow_html=True)


# ─── Hero ────────────────────────────────────────────────────────────────────
st.markdown("<div class='hero-title'>HireLens</div>", unsafe_allow_html=True)
st.markdown("<div class='hero-sub'>AI Resume Analyzer</div>", unsafe_allow_html=True)
st.markdown("<div class='hero-divider'></div>", unsafe_allow_html=True)


# ─── Upload ──────────────────────────────────────────────────────────────────
st.markdown("<div class='section-label'>Step 1 — Upload Resume</div>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("Upload your Resume (PDF only)", type=["pdf"], label_visibility="collapsed")

if uploaded_file is not None:

    # ── Extract Text ──────────────────────────────────────────────────────────
    text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            if page.extract_text():
                text += page.extract_text()

    clean_text = re.sub(r'\s+', ' ', text)

    # ── Extracted Text ────────────────────────────────────────────────────────
    with st.expander("📄 View Extracted Resume Text"):
        st.markdown(f"<p style='font-size:0.85rem; color:#94a3b8; line-height:1.7'>{clean_text[:2000]}{'...' if len(clean_text)>2000 else ''}</p>", unsafe_allow_html=True)

    # ── Skill Detection ───────────────────────────────────────────────────────
    skills_list = [
        "python", "java", "c", "c++",
        "html", "css", "javascript", "react",
        "node", "mongodb", "sql",
        "machine learning", "ai",
        "data analysis", "communication",
        "leadership", "problem solving"
    ]

    found_skills = [s for s in skills_list if s.lower() in clean_text.lower()]
    missing_skills = [s for s in skills_list if s not in found_skills]

    # ── Skills Card ───────────────────────────────────────────────────────────
    st.markdown("<div class='section-label'>Step 2 — Skills Detected</div>", unsafe_allow_html=True)
    found_html = "".join([f"<span class='skill-pill'>{s}</span>" for s in found_skills]) if found_skills else "<span style='color:#6b7280;font-size:0.9rem'>No matching skills found.</span>"
    st.markdown(f"""
    <div class='card'>
        <div class='card-title'>✦ Matched Skills — {len(found_skills)} found</div>
        <div class='skills-grid'>{found_html}</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Job Description ───────────────────────────────────────────────────────
    st.markdown("<div class='section-label'>Step 3 — Job Description</div>", unsafe_allow_html=True)
    job_description = st.text_area("Paste the job description here", placeholder="Copy and paste the full job description...", label_visibility="collapsed", height=160)

    if job_description:
        jd_words = job_description.lower().split()
        resume_words = clean_text.lower().split()
        matched_words = set(jd_words).intersection(set(resume_words))
        score = (len(matched_words) / len(set(jd_words))) * 100

        if score > 70:
            score_class = "score-strong"
            bar_class = "bar-fill-strong"
            verdict = "Strong Match 🟢"
        elif score > 40:
            score_class = "score-medium"
            bar_class = "bar-fill-medium"
            verdict = "Medium Match 🟡"
        else:
            score_class = "score-weak"
            bar_class = "bar-fill-weak"
            verdict = "Weak Match 🔴"

        # ── ATS Score Card ─────────────────────────────────────────────────
        st.markdown("<div class='section-label'>ATS Compatibility Score</div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class='card'>
            <div class='card-title'>✦ ATS Score Analysis</div>
            <div class='score-wrap'>
                <div class='score-number {score_class}'>{score:.0f}%</div>
                <div class='score-label {score_class}'>{verdict}</div>
                <div class='bar-bg'>
                    <div class='{bar_class}' style='width:{min(score,100):.0f}%'></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Missing Skills ────────────────────────────────────────────────────────
    if missing_skills:
        st.markdown("<div class='section-label'>Skill Gaps</div>", unsafe_allow_html=True)
        missing_html = "".join([f"<span class='skill-missing'>{s}</span>" for s in missing_skills[:8]])
        st.markdown(f"""
        <div class='card'>
            <div class='card-title'>✦ Missing Skills — {len(missing_skills)} gaps found</div>
            <div class='skills-grid'>{missing_html}</div>
        </div>
        """, unsafe_allow_html=True)

    # ── Suggestions ───────────────────────────────────────────────────────────
    if missing_skills:
        st.markdown("<div class='section-label'>Recommendations</div>", unsafe_allow_html=True)
        suggestions_html = "".join([
            f"<div class='suggestion-item'>→ Add <strong>{s}</strong> to your skills section or highlight related experience</div>"
            for s in missing_skills[:5]
        ])
        st.markdown(f"""
        <div class='card'>
            <div class='card-title'>✦ How to Improve Your Score</div>
            {suggestions_html}
        </div>
        """, unsafe_allow_html=True)

else:
    # ── Empty State ────────────────────────────────────────────────────────
    st.markdown("""
    <div style='text-align:center; padding: 3rem 1rem; color: #4b5563;'>
        <div style='font-size:3rem; margin-bottom:1rem;'>📄</div>
        <div style='font-family: Syne, sans-serif; font-size:1rem; font-weight:600; color:#6b7280; letter-spacing:0.05em;'>Upload a PDF to get started</div>
        <div style='font-size:0.85rem; margin-top:6px; color:#4b5563;'>Your resume will be analyzed for skills, ATS score & improvement tips</div>
    </div>
    """, unsafe_allow_html=True)

