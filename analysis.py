import streamlit as st
import pdfplumber
import io
import re
from collections import Counter

# Initialize session state for file caching
if "cached_files" not in st.session_state:
    st.session_state.cached_files = {}

# --- EXTENDED SKILL MAPPINGS FOR BETTER DETECTION ---
TECHNICAL_SKILLS_MAP = {
    "python": ["python", "py", "django", "flask", "pandas", "numpy", "scipy"],
    "javascript": ["javascript", "js", "react", "angular", "vue", "node"],
    "java": ["java", "spring", "hibernate", "maven", "gradle"],
    "sql": ["sql", "mysql", "postgresql", "oracle", "t-sql", "plsql"],
    "react.js": ["react", "reactjs", "react.js"],
    "node.js": ["node", "nodejs", "node.js"],
    "machine learning": ["machine learning", "ml", "scikit-learn", "tensorflow", "keras", "sklearn"],
    "data analysis": ["data analysis", "analytics", "data science", "data analyst"],
    "deep learning": ["deep learning", "neural network", "cnn", "rnn", "lstm"],
    "artificial intelligence (ai)": ["artificial intelligence", "ai", "nlp", "computer vision"],
    "cloud computing": ["cloud", "aws", "azure", "gcp", "cloud services"],
    "aws": ["aws", "amazon web services", "ec2", "s3", "lambda", "dynamodb"],
    "azure": ["azure", "microsoft azure"],
    "docker": ["docker", "containerization", "container"],
    "kubernetes": ["kubernetes", "k8s", "orchestration"],
    "git/github": ["git", "github", "gitlab", "bitbucket", "version control"],
    "rest api": ["rest api", "restful", "api development", "api"],
    "database": ["database", "nosql", "relational", "mongodb", "cassandra"],
    "ui/ux design": ["ui/ux", "ux design", "ui design", "figma", "wireframe"],
    "video editing": ["video editing", "premiere", "final cut", "after effects"],
}

SOFT_SKILLS_MAP = {
    "communication": ["communication", "communicative", "interpersonal", "speaking"],
    "teamwork": ["teamwork", "team player", "collaboration", "collaborative", "cooperate"],
    "leadership": ["leadership", "leader", "management", "manager", "supervise"],
    "problem solving": ["problem solving", "problem-solving", "troubleshooting", "analytical"],
    "critical thinking": ["critical thinking", "critical-thinking", "analytical thinking"],
    "time management": ["time management", "deadline", "organization", "organized"],
    "adaptability": ["adaptability", "adaptable", "flexible", "flexibility"],
    "creativity": ["creativity", "creative", "innovation", "innovative"],
    "project management": ["project management", "agile", "scrum", "pmp"],
    "negotiation": ["negotiation", "negotiator", "persuasion"],
    "presentation skills": ["presentation", "public speaking", "presenter"],
}

REJECTED_COUNTRIES = ["usa", "canada", "uk", "pakistan", "china", "uae", "russia", "australia"]


def cache_file_content(file_obj):
    """Cache file content to avoid file pointer issues"""
    file_id = id(file_obj)
    
    # Check if already cached
    if file_id in st.session_state.cached_files:
        return st.session_state.cached_files[file_id]
    
    # Read and cache
    try:
        content = file_obj.read()
        st.session_state.cached_files[file_id] = content
        return content
    except Exception as e:
        st.error(f"Error caching file: {str(e)}")
        return None


def get_text_from_file(file):
    """Extract text from PDF or TXT file with caching"""
    if not file:
        return ""
    try:
        # Get cached content
        file_content = cache_file_content(file)
        
        if file_content is None:
            return ""
        
        if file.type == "application/pdf":
            # Use cached content
            with pdfplumber.open(io.BytesIO(file_content)) as pdf:
                text = " ".join([p.extract_text() or "" for p in pdf.pages])
                return clean_text(text)
        else:  # txt file
            text = file_content.decode("utf-8")
            return clean_text(text)
    except Exception as e:
        st.error(f"Error reading file {file.name}: {str(e)}")
        return ""


def clean_text(text):
    """Clean and normalize text for better matching"""
    text = text.lower()
    # Remove special characters but keep spaces
    text = re.sub(r'[^a-z0-9\s\.\-]', ' ', text)
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def extract_skills_advanced(text):
    """Advanced skill extraction using keyword mapping"""
    detected_tech = []
    detected_soft = []
    
    # Extract technical skills with keyword variants
    for skill, keywords in TECHNICAL_SKILLS_MAP.items():
        for keyword in keywords:
            if re.search(r'\b' + re.escape(keyword) + r'\b', text):
                if skill not in detected_tech:
                    detected_tech.append(skill)
                break
    
    # Extract soft skills with keyword variants
    for skill, keywords in SOFT_SKILLS_MAP.items():
        for keyword in keywords:
            if re.search(r'\b' + re.escape(keyword) + r'\b', text):
                if skill not in detected_soft:
                    detected_soft.append(skill)
                break
    
    return detected_tech, detected_soft


def extract_jd_requirements(jd_text):
    """Extract specific requirements from JD"""
    requirements = {
        "skills": [],
        "experience_years": 0,
        "education": [],
        "keywords": []
    }
    
    # Extract all detected skills
    tech, soft = extract_skills_advanced(jd_text)
    requirements["skills"] = tech + soft
    
    # Extract years of experience
    exp_match = re.search(r'(\d+)\+?\s*(?:year|yr)s?\s*(?:of\s*)?(?:experience|exp)?', jd_text)
    if exp_match:
        requirements["experience_years"] = int(exp_match.group(1))
    
    # Extract education keywords
    edu_keywords = ["bachelor", "master", "degree", "phd", "certification", "diploma"]
    for edu in edu_keywords:
        if edu in jd_text:
            requirements["education"].append(edu)
    
    return requirements


def calculate_advanced_match_score(jd_requirements, candidate_text, candidate_skills):
    """
    Calculate match score based purely on JD skill matching.
    
    Logic:
    1. Extract required skills from JD
    2. Extract candidate skills from resume
    3. Find intersection (skills candidate HAS that JD requires)
    4. Calculate percentage: (matched_skills / required_skills) * 100
    
    Example:
    - JD requires: [Python, SQL, React, Leadership, Communication] = 5 skills
    - Candidate has: [Python, React, Communication, Teamwork] = 4 detected
    - Matched: [Python, React, Communication] = 3 skills
    - Score: (3/5) * 100 = 60%
    """
    
    jd_skills = set(jd_requirements["skills"])
    candidate_skills_set = set(candidate_skills)
    
    # Find exact matches between JD requirements and candidate skills
    skill_matches = jd_skills.intersection(candidate_skills_set)
    
    # Calculate percentage based only on skill matching
    if len(jd_skills) > 0:
        match_score = int((len(skill_matches) / len(jd_skills)) * 100)
    else:
        # If no skills found in JD, score based on if candidate has any skills
        match_score = 50 if len(candidate_skills_set) > 0 else 0
    
    # Ensure score is between 0 and 100
    match_score = min(max(match_score, 0), 100)
    
    return match_score, skill_matches


def get_skill_gap_analysis(jd_skills, candidate_skills):
    """Analyze skill gaps"""
    jd_set = set(jd_skills)
    cand_set = set(candidate_skills)
    
    have = jd_set.intersection(cand_set)
    missing = jd_set - cand_set
    extra = cand_set - jd_set
    
    return {
        "have": list(have),
        "missing": list(missing),
        "extra": list(extra)
    }


def analysis_page():
    """Main analysis page function with advanced backend"""
    
    # Reset cache if files have changed
    if "last_jd_id" not in st.session_state:
        st.session_state.last_jd_id = None
    if "last_res_ids" not in st.session_state:
        st.session_state.last_res_ids = []
    
    current_jd_id = id(st.session_state.jd_input) if st.session_state.jd_input else None
    current_res_ids = [id(f) for f in st.session_state.res_input] if st.session_state.res_input else []
    
    # Clear cache if files changed
    if current_jd_id != st.session_state.last_jd_id or current_res_ids != st.session_state.last_res_ids:
        st.session_state.cached_files = {}
        st.session_state.last_jd_id = current_jd_id
        st.session_state.last_res_ids = current_res_ids
    
    st.markdown("<h2 style='text-align:center;'>📋 Resume Analysis & Filtering</h2>", unsafe_allow_html=True)
    
    # Check if files are uploaded
    if not st.session_state.jd_input or not st.session_state.res_input:
        st.warning("⚠️ Please upload Job Description and Resumes on the Home page first.")
        if st.button("← Go Back to Home"):
            st.session_state.page = "Home"
            st.rerun()
        return
    
    # Extract and analyze JD
    jd_text = get_text_from_file(st.session_state.jd_input)
    jd_requirements = extract_jd_requirements(jd_text)
    jd_required_skills = jd_requirements["skills"]
    
    # Display JD Analysis
    with st.expander("📄 Job Description Analysis", expanded=False):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Required Skills", len(jd_required_skills))
        with col2:
            st.metric("Experience Required", f"{jd_requirements['experience_years']}+ Years")
        with col3:
            st.metric("Education Keywords", len(jd_requirements["education"]))
        
        st.write("**Required Skills:**")
        for skill in jd_required_skills:
            st.markdown(f'<span class="skill-tag">{skill}</span>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Process each resume
    candidates_data = []
    
    for idx, resume_file in enumerate(st.session_state.res_input):
        with st.container():
            st.markdown(f"<h4>👤 Candidate {idx + 1}: {resume_file.name}</h4>", unsafe_allow_html=True)
            
            res_text = get_text_from_file(resume_file)
            
            if not res_text:
                st.error(f"Could not extract text from {resume_file.name}")
                continue
            
            # Extract skills from resume
            det_tech, det_soft = extract_skills_advanced(res_text)
            all_detected_skills = det_tech + det_soft
            
            # Calculate match score based purely on JD skill matching
            match_score, skill_matches = calculate_advanced_match_score(
                jd_requirements, 
                res_text, 
                all_detected_skills
            )
            
            # Analyze skill gaps
            gap_analysis = get_skill_gap_analysis(jd_required_skills, all_detected_skills)
            
            # Display matching breakdown
            with st.expander(f"📊 Matching Breakdown", expanded=True):
                col_breakdown1, col_breakdown2, col_breakdown3 = st.columns(3)
                
                with col_breakdown1:
                    st.metric("JD Required Skills", len(jd_required_skills))
                
                with col_breakdown2:
                    st.metric("Skills Matched", len(skill_matches))
                
                with col_breakdown3:
                    st.metric("Skills Missing", len(gap_analysis["missing"]))
                
                # Show matching calculation
                st.markdown(f"""
                    **Calculation:**
                    - JD requires: **{len(jd_required_skills)} skills**
                    - Candidate has: **{len(skill_matches)} matching skills**
                    - Score: ({len(skill_matches)} ÷ {len(jd_required_skills)}) × 100 = **{match_score}%**
                """)
                
                if skill_matches:
                    st.write("**✅ Matched Skills:**")
                    for skill in sorted(skill_matches):
                        st.markdown(f'<span class="skill-tag">{skill}</span>', unsafe_allow_html=True)
            
            # Display results in columns
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.markdown('<div class="skills-card">', unsafe_allow_html=True)
                st.subheader("🎯 Detected Skills")
                
                if det_tech:
                    st.write("**Technical Skills:**")
                    for skill in det_tech:
                        st.markdown(f'<span class="skill-tag">{skill}</span>', unsafe_allow_html=True)
                
                if det_soft:
                    st.write("**Soft Skills:**")
                    for skill in det_soft:
                        st.markdown(f'<span class="skill-tag">{skill}</span>', unsafe_allow_html=True)
                
                if not all_detected_skills:
                    st.info("⚠️ No matching skills detected")
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                # Match score display with color
                if match_score >= 80:
                    color = "#10b981"  # Green
                elif match_score >= 60:
                    color = "#f59e0b"  # Orange
                else:
                    color = "#ef4444"  # Red
                
                st.markdown(f"""
                    <div style="text-align:center; padding:20px; background:{color}20; border-radius:10px; border:2px solid {color};">
                        <p style="margin:0; color:#94a3b8; font-size:12px;">Match Score</p>
                        <h2 style="color:{color}; margin:10px 0;">{match_score}%</h2>
                        <p style="margin:0; color:#94a3b8; font-size:11px;">
                            {'🟢 Excellent' if match_score >= 80 else '🟠 Good' if match_score >= 60 else '🔴 Needs Work'}
                        </p>
                    </div>
                """, unsafe_allow_html=True)
            
            with col3:
                country = st.selectbox(
                    f"Location", 
                    ["India", "USA", "Canada", "UK", "Pakistan", "China", "UAE", "Russia", "Australia", "Other"],
                    key=f"country_{idx}"
                )
            
            # Additional metrics
            col_m1, col_m2, col_m3 = st.columns(3)
            with col_m1:
                st.metric("Skills Found", len(all_detected_skills))
            with col_m2:
                st.metric("Matched", len(gap_analysis["have"]))
            with col_m3:
                st.metric("Missing", len(gap_analysis["missing"]))
            
            # Store candidate data
            candidate_info = {
                "name": resume_file.name.replace(".pdf", ""),
                "detected_skills": all_detected_skills,
                "required_skills": jd_required_skills,
                "match_score": match_score,
                "country": country,
                "technical_skills": det_tech,
                "soft_skills": det_soft,
                "gap_analysis": gap_analysis,
                "skill_matches": list(skill_matches)
            }
            candidates_data.append(candidate_info)
            
            st.markdown("---")
    
    # Store processed data in session state
    st.session_state.candidates_data = candidates_data
    
    # Action buttons
    col_a, col_b, col_c = st.columns([1, 1, 1])
    
    with col_a:
        if st.button("✅ Proceed to Skill Gap Analysis", key="to_skillgap"):
            st.session_state.page = "Skill Gap"
            st.rerun()
    
    with col_b:
        if st.button("🏆 Go to Ranking", key="to_ranking"):
            st.session_state.page = "Ranking"
            st.rerun()
    
    with col_c:
        if st.button("← Back to Home", key="back_home"):
            st.session_state.page = "Home"
            st.rerun()
            st.rerun()
    
    with col_b:
        if st.button("🏆 Go to Ranking"):
            st.session_state.page = "Ranking"
            st.rerun()
    
    with col_c:
        if st.button("← Back to Home"):
            st.session_state.page = "Home"
            st.rerun()