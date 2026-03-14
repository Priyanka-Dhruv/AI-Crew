import streamlit as st
import base64
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Skill Gap - RecruitSmart AI", layout="wide")

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
        </style>
        """, unsafe_allow_html=True)

add_custom_style("back.jpg")

# Navigation Bar
nav_left, nav_right = st.columns([2, 1.5])
with nav_right:
    n1, n2, n3, n4 = st.columns(4)
    if n1.button("Home"): st.switch_page("app.py")
    if n2.button("Analysis"): st.switch_page("pages/analysis.py")
    if n3.button("Skill Gap"): st.rerun()
    if n4.button("Ranking"): st.switch_page("pages/ranking.py")

st.markdown("<h2 style='text-align:center;'>🔍 Skill Gap Analysis</h2>", unsafe_allow_html=True)

# Data from Session State (Calculated on Page 2)
# We assume Page 2 saved these lists: 'detected_skills' and 'required_skills'
have = st.session_state.get('detected_skills', [])
needed = st.session_state.get('required_skills', [])
missing = [s for s in needed if s not in have]

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="gap-card">', unsafe_allow_html=True)
    st.subheader("✅ Skills You Have")
    if have:
        for s in have:
            st.markdown(f"- <span class='skill-have'>{s}</span>", unsafe_allow_html=True)
    else:
        st.write("No matching skills found.")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="gap-card">', unsafe_allow_html=True)
    st.subheader("❌ Missing Skills")
    if missing:
        for s in missing:
            st.markdown(f"- <span class='skill-missing'>{s}</span>", unsafe_allow_html=True)
    else:
        st.success("Perfect Match! No skills missing.")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
if st.button("Proceed to Final Ranking"):
    st.switch_page("pages/ranking.py")