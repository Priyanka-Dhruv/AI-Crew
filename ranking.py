import streamlit as st
import base64
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Ranking - RecruitSmart AI", layout="wide")

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
        .ranking-card {{
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 25px;
            backdrop-filter: blur(10px);
        }}
        </style>
        """, unsafe_allow_html=True)

add_custom_style("back.jpg")

# --- NAVIGATION BAR (Consistent with Image c9e0d8) ---
nav_left, nav_right = st.columns([2, 1.5])
with nav_right:
    n1, n2, n3, n4 = st.columns(4)
    if n1.button("Home"): st.switch_page("app.py")
    if n2.button("Analysis"): st.switch_page("pages/analysis.py")
    if n3.button("Skill Gap"): st.switch_page("pages/skill_gap.py")
    if n4.button("Ranking"): st.rerun()

st.markdown("<h2 style='text-align:center;'>🏆 Candidate Leaderboard</h2>", unsafe_allow_html=True)

# 1. FETCH DYNAMIC DATA
ranking_list = st.session_state.get('ranking_data', [])

if not ranking_list:
    st.warning("⚠️ No data found. Please go to the Analysis page and click 'Proceed to Validation' first.")
else:
    # 2. CONVERT TO DATAFRAME & SORT
    df = pd.DataFrame(ranking_list)
    df = df.sort_values(by="Match Score", ascending=False).reset_index(drop=True)

    # 3. DISPLAY VISUALS
    col_chart, col_table = st.columns([1.2, 1], gap="large")

    with col_chart:
        st.markdown("### 📊 Score Distribution")
        fig = px.bar(
            df, 
            x="Candidate Name", 
            y="Match Score", 
            color="Match Score",
            color_continuous_scale="Blues",
            text="Match Score",
            template="plotly_dark"
        )
        fig.update_traces(texttemplate='%{text}%', textposition='outside')
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color="white")
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_table:
        st.markdown("### 📋 Ranked Details")
        st.markdown('<div class="ranking-card">', unsafe_allow_html=True)
        # Displaying the dynamic table
        st.dataframe(
            df, 
            use_container_width=True, 
            hide_index=False,
            column_config={
                "Match Score": st.column_config.ProgressColumn(
                    "Match Percentage",
                    help="Score based on JD requirements",
                    format="%d%%",
                    min_value=0,
                    max_value=100,
                ),
            }
        )
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
if st.button("🗑️ Clear All Rankings"):
    st.session_state.ranking_data = []
    st.rerun()