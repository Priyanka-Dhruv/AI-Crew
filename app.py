import streamlit as st
import base64
from analysis import analysis_page
from skill import skill_page
from ranking import ranking_page

# Set page configuration
st.set_page_config(page_title="RecruitSmart AI", layout="wide")

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "Home"
if "jd_input" not in st.session_state:
    st.session_state.jd_input = None
if "res_input" not in st.session_state:
    st.session_state.res_input = []
if "candidates_data" not in st.session_state:
    st.session_state.candidates_data = []
if "ranking_data" not in st.session_state:
    st.session_state.ranking_data = []

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
            color: #3b82f6 !important;
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
            padding: 12px 25px !important;
            border-radius: 50px !important; 
            font-size: 16px !important;
            font-weight: 500 !important;
            box-shadow: inset 0px 1px 2px rgba(255,255,255,0.1), 0px 10px 20px rgba(0,0,0,0.4) !important;
            transition: all 0.3s ease !important;
            display: block;
            margin: 30px auto 0 auto;
            width: 100%;
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
        
        .nav-link.active {{
            color: #3b82f6;
            font-weight: 600;
        }}
        
        /* Sidebar Polish */
        [data-testid="stSidebar"] {{
            background-color: #0f172a !important;
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
        
        .gap-card {{
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 25px;
            backdrop-filter: blur(15px);
            height: 100%;
        }}
        
        .skill-have {{ color: #10b981; font-weight: bold; }}
        .skill-missing {{ color: #ef4444; font-weight: bold; }}
        
        .ranking-card {{
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 25px;
            backdrop-filter: blur(10px);
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Execute style function
add_custom_style("back.jpg")

# ---------------------------------------------------------
# SIDEBAR NAVIGATION
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("<h2 style='color:#3b82f6;'>RecruitSmart AI</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Get current page and match it with radio
    page_options = ["Home", "Analysis", "Skill Gap", "Ranking"]
    current_index = page_options.index(st.session_state.page) if st.session_state.page in page_options else 0
    
    page = st.radio(
        "Navigation",
        page_options,
        index=current_index,
        label_visibility="collapsed"
    )
    # Only update if radio was actually changed
    if page != st.session_state.page:
        st.session_state.page = page
        st.rerun()
    
    st.markdown("---")
    st.markdown("<p style='color:#64748b; font-size:12px;'>Uploaded Files:</p>", unsafe_allow_html=True)
    if st.session_state.jd_input:
        st.success(f"✅ JD: {st.session_state.jd_input.name}")
    else:
        st.info("📄 No JD uploaded")
    
    if st.session_state.res_input:
        st.success(f"✅ Resumes: {len(st.session_state.res_input)} file(s)")
    else:
        st.info("👤 No resumes uploaded")

# ---------------------------------------------------------
# PAGE ROUTING
# ---------------------------------------------------------
if st.session_state.page == "Home":
    # ----- HOME PAGE -----
    c1, c2 = st.columns([2.5, 0.8])
    with c1: 
        st.markdown("<h2 style='margin:0; font-weight:700;'>RecruitSmart <span style='color:#3b82f6;'>AI</span></h2>", unsafe_allow_html=True)

    st.markdown("<hr style='opacity:0.1; margin:10px 0 40px 0;'>", unsafe_allow_html=True)

    left, right = st.columns([1.4, 1], gap="large")

    with left:
        st.markdown("<h1 style='font-size:48px; margin-bottom:10px;'>Smart AI</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='color:#64748b; margin-top:-20px; font-weight:400;'>Recruitment System</h3>", unsafe_allow_html=True)
        st.markdown("<p style='color:#94a3b8; font-size:16px; margin-bottom:30px;'>Streamline your hiring process with deep-learning candidate matching.</p>", unsafe_allow_html=True)
        
        # JD Upload Section
        st.markdown('<div class="upload-header">📄 Upload Job Description (PDF/TXT)</div>', unsafe_allow_html=True)
        jd_file = st.file_uploader("JD", type=["pdf", "txt"], label_visibility="collapsed", key="jd_upload")
        
        # Resume Upload Section (MULTIPLE FILES)
        st.markdown('<div class="upload-header">👤 Upload Candidate Resumes (Multiple PDFs)</div>', unsafe_allow_html=True)
        resume_files = st.file_uploader(
            "Resumes", 
            type=["pdf"], 
            label_visibility="collapsed", 
            accept_multiple_files=True,
            key="resume_upload"
        )
        
        # Store in session state
        if jd_file is not None:
            st.session_state.jd_input = jd_file
        
        if resume_files:
            st.session_state.res_input = resume_files

        # Primary Action Button
        st.markdown("")  # spacing
        
        # Check if files are ready
        has_jd = st.session_state.jd_input is not None
        has_resumes = len(st.session_state.res_input) > 0
        
        col1, col2 = st.columns([3, 1])
        with col1:
            button_clicked = st.button(
                "🚀 Start AI Analysis", 
                use_container_width=True,
                key="start_analysis_btn",
                disabled=not (has_jd and has_resumes)
            )
            
            if button_clicked:
                st.session_state.page = "Analysis"
                st.rerun()
        
        # Status indicator
        st.markdown("")
        if not has_jd:
            st.warning("📄 Upload Job Description first")
        if not has_resumes:
            st.warning("👤 Upload at least one Resume")
        if has_jd and has_resumes:
            st.success("✅ Ready to analyze!")

    with right:
        st.markdown(
            """
            <div class="info-card">
                <h3 style='color:#3b82f6; margin-top:0;'>✨ How It Works</h3>
                <ol style='color:#cbd5e1;'>
                    <li><strong>Upload</strong> your Job Description</li>
                    <li><strong>Upload</strong> candidate resumes</li>
                    <li><strong>Analyze</strong> skills & experience</li>
                    <li><strong>Compare</strong> skill gaps</li>
                    <li><strong>Rank</strong> best candidates</li>
                </ol>
            </div>
            """,
            unsafe_allow_html=True
        )

elif st.session_state.page == "Analysis":
    analysis_page()

elif st.session_state.page == "Skill Gap":
    skill_page()

elif st.session_state.page == "Ranking":
    ranking_page()