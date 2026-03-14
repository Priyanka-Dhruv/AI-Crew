import streamlit as st
import base64
import pdfplumber
import io

st.set_page_config(page_title="Analysis - RecruitSmart AI", layout="wide")

def add_custom_style(image_file):
    try:
        with open(image_file, "rb") as image:
            encoded = base64.b64encode(image.read()).decode()
    except FileNotFoundError:
        encoded = ""
    st.markdown(f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(10, 15, 30, 0.92), rgba(10, 15, 30, 0.92)), 
                        url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            color: white;
        }}
        .skills-card {{
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 25px;
            backdrop-filter: blur(15px);
        }}
        .skill-tag {{
            display: inline-block;
            background: rgba(59, 130, 246, 0.2);
            color: #8fb3ff;
            padding: 5px 12px;
            border-radius: 50px;
            margin: 4px;
            border: 1px solid rgba(59, 130, 246, 0.3);
            font-size: 12px;
        }}
        </style>
        """, unsafe_allow_html=True)

add_custom_style("back.jpg")

# --- TOP NAVIGATION BAR ---
nav_left, nav_right = st.columns([3, 1])
with nav_right:
    n1, n2, n3 = st.columns(3)
    if n1.button("Home"): st.switch_page("app.py")
    if n2.button("Analysis"): st.rerun()
    n3.button("Ranking")

# --- FULL SKILL LISTS ---
TECHNICAL_SKILLS = ["UI/UX Design", "Video Editing", "Machine Learning", "Data Analysis", "Python", "SQL", "React.js", "Artificial Intelligence (AI)", "Cloud Computing", "Git/GitHub", "Deep Learning", "Data Mining"]
SOFT_SKILLS = ["Communication", "Teamwork", "Leadership", "Problem Solving", "Critical Thinking", "Time Management", "Adaptability"]
REJECTED_COUNTRIES = ["usa", "canada", "uk", "pakistan", "china", "uae", "russia", "australia"]

def get_text(file):
    if not file: return ""
    try:
        with pdfplumber.open(io.BytesIO(file.read())) as pdf:
            return " ".join([p.extract_text() for p in pdf.pages if p.extract_text()]).lower()
    except:
        return ""

st.markdown("<h2 style='text-align:center;'>Resume Analysis & Filtering</h2>", unsafe_allow_html=True)

# Fetching files from Page 1
jd_file = st.session_state.get('jd_input')
res_file = st.session_state.get('res_input')

left, right = st.columns([1.5, 1])

with left:
    st.subheader("Candidate Details")
    country = st.selectbox("Current Location", ["India"] + [c.title() for c in REJECTED_COUNTRIES])
    
    res_text = get_text(res_file)
    jd_text = get_text(jd_file)
    
    # Detection
    det_tech = [s for s in TECHNICAL_SKILLS if s.lower() in res_text]
    det_soft = [s for s in SOFT_SKILLS if s.lower() in res_text]
    
    st.write("#### Verified Technical Skills")
    tech_verified = st.multiselect("Check detected technical skills", TECHNICAL_SKILLS, default=det_tech)
    
    st.write("#### Verified Soft Skills")
    soft_verified = st.multiselect("Check detected soft skills", SOFT_SKILLS, default=det_soft)
    
    if st.button("Proceed to Validation"):
        if country.lower() in REJECTED_COUNTRIES:
            st.error(f"❌ Rejected: Automated rejection for {country}.")
        elif not res_file:
            st.warning("⚠️ No resume found. Please upload on Home page.")
        else:
            st.success("✅ Candidate criteria met!")

with right:
    st.markdown('<div class="skills-card">', unsafe_allow_html=True)
    st.markdown("<h3 style='color:#3b82f6;'>📊 Match Score</h3>", unsafe_allow_html=True)
    
    # Match Score Calculation
    jd_reqs = [s for s in (TECHNICAL_SKILLS + SOFT_SKILLS) if s.lower() in jd_text]
    score = 0
    if jd_reqs:
        matches = set(tech_verified + soft_verified).intersection(set(jd_reqs))
        score = int((len(matches) / len(jd_reqs)) * 100)
    elif res_text:
        score = 40 
    
    st.markdown(f"""
        <div style="text-align:center; padding:20px; background:rgba(59,130,246,0.1); border-radius:15px; border:1px solid #1e3a5f; margin-bottom:20px;">
            <h1 style="color:#3b82f6; font-size:60px; margin:0;">{score}%</h1>
            <p style="color:#94a3b8; margin:0;">JD Match Score</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("**Detected Skills:**")
    all_det = tech_verified + soft_verified
    if all_det:
        for s in all_det:
            st.markdown(f'<span class="skill-tag">{s}</span>', unsafe_allow_html=True)
    else:
        st.info("Upload a resume on the Home page to see skills.")
    st.markdown('</div>', unsafe_allow_html=True)