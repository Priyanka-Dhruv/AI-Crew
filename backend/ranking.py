import streamlit as st
import pandas as pd
import plotly.express as px


def ranking_page():
    """Candidate Ranking and Leaderboard page"""
    
    st.markdown("<h2 style='text-align:center;'>🏆 Candidate Leaderboard</h2>", unsafe_allow_html=True)
    
    # Check if analysis has been completed
    if not st.session_state.candidates_data:
        st.warning("⚠️ Please complete the Analysis step first.")
        if st.button("← Back to Analysis"):
            st.session_state.page = "Analysis"
            st.rerun()
        return
    
    # Prepare data for ranking
    ranking_list = []
    for candidate in st.session_state.candidates_data:
        ranking_list.append({
            "Rank": "",  # Will be filled after sorting
            "Candidate": candidate["name"],
            "Match Score": candidate["match_score"],
            "Skills Found": len(candidate["detected_skills"]),
            "Skills Missing": len([s for s in candidate["required_skills"] if s not in candidate["detected_skills"]]),
            "Location": candidate["country"],
            "Technical Skills": len(candidate["technical_skills"]),
            "Soft Skills": len(candidate["soft_skills"])
        })
    
    # Convert to DataFrame and sort by Match Score
    df = pd.DataFrame(ranking_list)
    df = df.sort_values(by="Match Score", ascending=False).reset_index(drop=True)
    df["Rank"] = df.index + 1
    
    # Reorder columns
    df = df[["Rank", "Candidate", "Match Score", "Skills Found", "Skills Missing", 
             "Technical Skills", "Soft Skills", "Location"]]
    
    st.info(f"📊 Ranked {len(df)} candidate(s) - Top performer: {df.iloc[0]['Candidate']} ({df.iloc[0]['Match Score']}%)")
    
    st.markdown("---")
    
    # Display rankings with top 3 highlighted
    col_chart, col_table = st.columns([1.2, 1.5], gap="large")
    
    with col_chart:
        st.markdown("### 📊 Score Distribution")
        fig = px.bar(
            df, 
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
            xaxis_title="",
            yaxis_title="Match Score (%)"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col_table:
        st.markdown("### 🏅 Top Candidates")
        for idx, row in df.head(3).iterrows():
            medal = ["🥇", "🥈", "🥉"][idx]
            color = ["#fbbf24", "#c0c0c0", "#cd7f32"][idx]
            st.markdown(f"""
                <div style="background: {color}15; border: 1px solid {color}; border-radius:10px; 
                padding:12px; margin:8px 0; background-clip:padding-box;">
                    <strong>{medal} {row['Candidate']}</strong><br>
                    <small>Match: {row['Match Score']}% | Skills: {row['Skills Found']}</small>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Full Leaderboard Table
    st.markdown("### 📋 Full Leaderboard")
    st.markdown('<div class="ranking-card">', unsafe_allow_html=True)
    
    # Display table with formatting
    st.dataframe(
        df, 
        use_container_width=True, 
        hide_index=True,
        column_config={
            "Rank": st.column_config.NumberColumn("Rank", width="small"),
            "Candidate": st.column_config.TextColumn("Candidate Name"),
            "Match Score": st.column_config.ProgressColumn(
                "Match %",
                help="Percentage match to job requirements",
                format="%d%%",
                min_value=0,
                max_value=100,
            ),
            "Skills Found": st.column_config.NumberColumn("Found", width="small"),
            "Skills Missing": st.column_config.NumberColumn("Missing", width="small"),
            "Technical Skills": st.column_config.NumberColumn("Tech", width="small"),
            "Soft Skills": st.column_config.NumberColumn("Soft", width="small"),
            "Location": st.column_config.TextColumn("Location"),
        }
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Detailed candidate profiles
    st.markdown("### 👥 Detailed Candidate Profiles")
    
    for idx, candidate in enumerate(st.session_state.candidates_data):
        df_candidate = df[df["Candidate"] == candidate["name"]].iloc[0]
        rank = int(df_candidate["Rank"])
        
        with st.expander(f"{'🥇' if rank == 1 else '🥈' if rank == 2 else '🥉' if rank == 3 else '🔷'} #{rank} - {candidate['name']} ({candidate['match_score']}%)"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Match Score", f"{candidate['match_score']}%")
            with col2:
                st.metric("Skills Found", len(candidate['detected_skills']))
            with col3:
                st.metric("Skills Missing", len([s for s in candidate['required_skills'] if s not in candidate['detected_skills']]))
            
            st.write(f"**Location:** {candidate['country']}")
            
            if candidate['technical_skills']:
                st.write("**Technical Skills:**")
                for skill in candidate['technical_skills']:
                    st.markdown(f'<span class="skill-tag">{skill}</span>', unsafe_allow_html=True)
            
            if candidate['soft_skills']:
                st.write("**Soft Skills:**")
                for skill in candidate['soft_skills']:
                    st.markdown(f'<span class="skill-tag">{skill}</span>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Export options
    st.markdown("### 💾 Export Options")
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name="candidate_rankings.csv",
            mime="text/csv"
        )
    
    with col2:
        # JSON export
        import json
        json_data = json.dumps(ranking_list, indent=2)
        st.download_button(
            label="📥 Download JSON",
            data=json_data,
            file_name="candidate_rankings.json",
            mime="application/json"
        )
    
    with col3:
        st.write("")  # spacer
    
    st.markdown("---")
    
    # Navigation buttons
    col_a, col_b, col_c, col_d = st.columns([1, 1, 1, 1])
    
    with col_a:
        if st.button("↩️ Back to Skill Gap"):
            st.session_state.page = "Skill Gap"
            st.rerun()
    
    with col_b:
        if st.button("↪️ Back to Analysis"):
            st.session_state.page = "Analysis"
            st.rerun()
    
    with col_c:
        if st.button("🗑️ Clear All Data"):
            st.session_state.jd_input = None
            st.session_state.res_input = []
            st.session_state.candidates_data = []
            st.session_state.page = "Home"
            st.rerun()
    
    with col_d:
        if st.button("← Home"):
            st.session_state.page = "Home"
            st.rerun()