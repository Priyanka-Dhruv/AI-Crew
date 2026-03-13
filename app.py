import streamlit as st
import base64

# Set page configuration
st.set_page_config(page_title="RecruitSmart AI", layout="wide")

# ---------------------------------------------------------
# Background & CSS Styling
# ---------------------------------------------------------
def add_custom_style(image_file):
    try:
        with open(image_file, "rb") as image:
            encoded = base64.b64encode(image.read()).decode()
    except FileNotFoundError:
        encoded = ""

    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

        /* Main App Background */
        .stApp {{
            background: linear-gradient(rgba(10, 15, 30, 0.88), rgba(10, 15, 30, 0.88)), 
                        url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            font-family: 'Inter', sans-serif;
            color: white;
        }}

        /* --- UPLOAD SECTION REFINEMENT --- */
        .upload-header {{
            font-size: 14px !important;
            font-weight: 600;
            color: #8fb3ff !important;
            margin-bottom: 8px;
            margin-top: 15px;
        }}

        /* Shrinking the 'Limit 200MB' and dropzone text */
        [data-testid="stFileUploadDropzone"] p {{
            font-size: 13px !important;
            color: #cbd5e1 !important;
        }}
        [data-testid="stFileUploadDropzone"] small {{
            font-size: 10px !important;
            color: #64748b !important;
            text-transform: uppercase;
        }}

        /* --- THE PILL BUTTON PATTERN --- */
        .stButton > button {{
            background: linear-gradient(180deg, #1e3a5f 0%, #0a1420 100%) !important;
            color: #ffffff !important;
            border: 1px solid #2d4f7c !important;
            padding: 12px 60px !important;
            border-radius: 50px !important; /* Pill shape */
            font-size: 16px !important;
            font-weight: 500 !important;
            box-shadow: inset 0px 1px 2px rgba(255,255,255,0.1), 0px 10px 20px rgba(0,0,0,0.4) !important;
            transition: all 0.3s ease !important;
            display: block;
            margin: 30px auto 0 auto;
            min-width: 220px;
        }}

        .stButton > button:hover {{
            border-color: #3b82f6 !important;
            box-shadow: 0px 0px 20px rgba(59, 130, 246, 0.4) !important;
            transform: translateY(-1px);
        }}

        /* INFO CARD */
        .info-card {{
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 24px;
            padding: 30px;
            backdrop-filter: blur(15px);
        }}

        .nav-link {{
            color: #94a3b8;
            font-size: 15px;
            text-decoration: none;
            font-weight: 500;
            margin-top: 15px;
        }}
        
        /* Sidebar Polish */
        [data-testid="stSidebar"] {{
            background-color: #0f172a !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Execute style function
add_custom_style("re.jpeg")

# ---------------------------------------------------------
# NAVIGATION
# ---------------------------------------------------------
c1, c2, c3, c4 = st.columns([2.5, 0.8, 1, 1])
with c1: 
    st.markdown("<h2 style='margin:0; font-weight:700;'>RecruitSmart <span style='color:#3b82f6;'>AI</span></h2>", unsafe_allow_html=True)
with c2: st.markdown("<p class='nav-link'>Home</p>", unsafe_allow_html=True)
with c3: st.markdown("<p class='nav-link'>Analysis</p>", unsafe_allow_html=True)
with c4: st.markdown("<p class='nav-link'>Ranking</p>", unsafe_allow_html=True)

st.markdown("<hr style='opacity:0.1; margin:10px 0 40px 0;'>", unsafe_allow_html=True)

# ---------------------------------------------------------
# MAIN LAYOUT
# ---------------------------------------------------------
left, right = st.columns([1.4, 1], gap="large")

with left:
    st.markdown("<h1 style='font-size:48px; margin-bottom:10px;'>Smart AI</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='color:#64748b; margin-top:-20px; font-weight:400;'>Recruitment System</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color:#94a3b8; font-size:16px; margin-bottom:30px;'>Streamline your hiring process with deep-learning candidate matching.</p>", unsafe_allow_html=True)
    
    # JD Upload Section
    st.markdown('<div class="upload-header">📄 Upload Job Description</div>', unsafe_allow_html=True)
    st.file_uploader("JD", type=["pdf", "txt"], key="jd_input", label_visibility="collapsed")
    
    # Resume Upload Section
    st.markdown('<div class="upload-header">👤 Upload Candidate Resume</div>', unsafe_allow_html=True)
    st.file_uploader("Resume", type=["pdf"], key="res_input", label_visibility="collapsed")

    # Primary Pill Action Button
    if st.button("🚀 Start AI Analysis"):
        st.toast("Beginning Analysis...", icon="🤖")

with right:
    st.markdown(
        """
        <div class="info-card">
            <h3 style="margin-top:0; color:#3b82f6;">🔍 What Happens Next?</h3>
            <ul style="color:#cbd5e1; font-size:15px; line-height:2.2; list-style-type: none; padding-left:0;">
                <li>🔹 Resume text extraction</li>
                <li>🔹 Skill detection & mapping</li>
                <li>🔹 Experience relevance analysis</li>
                <li>🔹 Match score calculation</li>
                <li>🔹 Candidate ranking</li>
                <li>🔹 Strengths & weaknesses summary</li>
            </ul>
        </div>
        """, 
        unsafe_allow_html=True
    )

# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------
st.sidebar.title("Dashboard")
st.sidebar.radio("Navigate", ["Home", "Resume Analysis", "Candidate Ranking"])