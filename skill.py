import streamlit as st
import pandas as pd
import plotly.express as px


def skill_page():
    """Skill Gap Analysis page"""
    
    st.markdown("<h2 style='text-align:center;'>🔍 Skill Gap Analysis</h2>", unsafe_allow_html=True)
    
    # Check if analysis has been completed
    if not st.session_state.candidates_data:
        st.warning("⚠️ Please complete the Analysis step first.")
        if st.button("← Back to Analysis"):
            st.session_state.page = "Analysis"
            st.rerun()
        return
    
    st.info(f"📊 Analyzing {len(st.session_state.candidates_data)} candidate(s)")
    
    # Display skill gaps for each candidate
    for idx, candidate in enumerate(st.session_state.candidates_data):
        with st.container():
            st.markdown(f"<h4>Candidate: {candidate['name']}</h4>", unsafe_allow_html=True)
            
            have = candidate['detected_skills']
            needed = candidate['required_skills']
            missing = [s for s in needed if s not in have]
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown('<div class="gap-card">', unsafe_allow_html=True)
                st.subheader("✅ Skills You Have")
                
                if have:
                    for s in have:
                        st.markdown(f"- <span class='skill-have'>{s}</span>", unsafe_allow_html=True)
                else:
                    st.info("No matching skills found.")
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="gap-card">', unsafe_allow_html=True)
                st.subheader("❌ Missing Skills")
                
                if missing:
                    for s in missing:
                        st.markdown(f"- <span class='skill-missing'>{s}</span>", unsafe_allow_html=True)
                else:
                    st.success("✨ Perfect Match! No skills missing.")
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Show match percentage
            match_pct = candidate['match_score']
            st.markdown(f"""
                <div style="text-align:center; padding:10px; background:{'#10b981' if match_pct >= 70 else '#f59e0b'}20; 
                border-radius:10px; margin-top:15px; border:1px solid {'#10b981' if match_pct >= 70 else '#f59e0b'};">
                    <p style="color:#94a3b8; margin:0; font-size:12px;">Match Score</p>
                    <h3 style="color:{'#10b981' if match_pct >= 70 else '#f59e0b'}; margin:5px 0;">
                        {match_pct}%
                    </h3>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
    
    # Summary statistics
    st.markdown("<h3>📈 Summary Statistics</h3>", unsafe_allow_html=True)
    
    summary_data = {
        "Candidate": [c["name"] for c in st.session_state.candidates_data],
        "Match Score": [c["match_score"] for c in st.session_state.candidates_data],
        "Skills Found": [len(c["detected_skills"]) for c in st.session_state.candidates_data],
        "Skills Missing": [len([s for s in c["required_skills"] if s not in c["detected_skills"]]) 
                          for c in st.session_state.candidates_data]
    }
    
    df_summary = pd.DataFrame(summary_data)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Match Scores")
        fig = px.bar(
            df_summary,
            x="Candidate",
            y="Match Score",
            color="Match Score",
            color_continuous_scale="Blues",
            text="Match Score",
            template="plotly_dark",
            title="All Candidates Match Scores"
        )
        fig.update_traces(texttemplate='%{text}%', textposition='outside')
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color="white"),
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Skills Comparison")
        fig2 = px.bar(
            df_summary,
            x="Candidate",
            y=["Skills Found", "Skills Missing"],
            title="Skills Found vs Missing",
            template="plotly_dark",
            barmode="stack"
        )
        fig2.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color="white")
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    # Display summary table
    st.subheader("Detailed Summary Table")
    st.dataframe(df_summary, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Navigation buttons
    col_a, col_b, col_c = st.columns([1, 1, 1])
    
    with col_a:
        if st.button("🏆 Go to Ranking"):
            st.session_state.page = "Ranking"
            st.rerun()
    
    with col_b:
        if st.button("↩️ Back to Analysis"):
            st.session_state.page = "Analysis"
            st.rerun()
    
    with col_c:
        if st.button("← Home"):
            st.session_state.page = "Home"
            st.rerun()