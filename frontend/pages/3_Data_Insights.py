"""
🌿 ZenFeed — Data Insights
Patterns across all ZenFeed screenings.
"""

import streamlit as st
import requests
import os
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# ============================================================================
# PAGE CONFIG
# ============================================================================
st.set_page_config(
    page_title="ZenFeed · Insights",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

try:
    API_URL = st.secrets.get("API_URL", os.environ.get("API_URL", "http://localhost:5000"))
except Exception:
    API_URL = os.environ.get("API_URL", "http://localhost:5000")

# ============================================================================
# GLOBAL CSS
# ============================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;800&family=Inter:wght@400;500;600&display=swap');

html, body, .stApp {
  background: linear-gradient(160deg, #050b14 0%, #08122a 40%, #0b1a36 100%) !important;
  background-attachment: fixed !important;
  color: #e6edf3;
  font-family: 'Inter', sans-serif;
}

h1, h2, h3, h4 {
  font-family: 'Poppins', sans-serif;
  background: linear-gradient(135deg, #5eead4 0%, #93c5fd 50%, #c4b5fd 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: -0.5px;
}

section[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #06101e 0%, #0a192e 100%);
  border-right: 2px solid;
  border-image: linear-gradient(180deg, #14b8a6 0%, #818cf8 100%) 1;
}

.zen-card {
  background: linear-gradient(135deg, rgba(8, 16, 30, 0.97) 0%, rgba(12, 24, 44, 0.97) 100%);
  border: 1px solid transparent;
  background-clip: padding-box;
  position: relative;
  border-radius: 16px;
  padding: 24px 28px;
  margin-bottom: 18px;
  transition: all 0.3s ease;
  overflow: hidden;
}
.zen-card::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: 16px;
  padding: 1px;
  background: linear-gradient(135deg, #5eead4 0%, #93c5fd 50%, #c4b5fd 100%);
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  opacity: 0.4;
}
.zen-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 32px rgba(94, 234, 212, 0.12), 0 0 60px rgba(196, 181, 253, 0.08);
}
.zen-card:hover::before {
  opacity: 1;
}

.zen-kpi {
  background: linear-gradient(135deg, rgba(94, 234, 212, 0.06) 0%, rgba(147, 197, 253, 0.06) 100%);
  border: 1px solid rgba(94, 234, 212, 0.18);
  border-top: 3px solid;
  border-image: linear-gradient(90deg, #5eead4 0%, #93c5fd 100%) 1;
  border-radius: 14px;
  padding: 24px;
  text-align: center;
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
}
.zen-kpi::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(94, 234, 212, 0.08) 0%, transparent 70%);
  animation: pulse 3s ease-in-out infinite;
}
@keyframes pulse {
  0%, 100% { transform: scale(0.8); opacity: 0.5; }
  50% { transform: scale(1.2); opacity: 0.8; }
}
.zen-kpi:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 20px rgba(94, 234, 212, 0.12);
}
.zen-kpi-value {
  font-family: 'Poppins', sans-serif;
  font-size: 2.2rem;
  font-weight: 800;
  background: linear-gradient(135deg, #5eead4 0%, #93c5fd 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  position: relative;
  z-index: 1;
}
}
.zen-kpi-label {
  font-size: 0.85rem;
  color: #8b949e;
  margin-top: 4px;
}

.badge-healthy { background:#0a1e1a; color:#5eead4; border:1px solid #5eead4; border-radius:20px; padding:4px 14px; font-weight:600; font-size:0.9rem; }
.badge-atrisk  { background:#2d1f00; color:#f59e0b; border:1px solid #f59e0b; border-radius:20px; padding:4px 14px; font-weight:600; font-size:0.9rem; }
.badge-burnout { background:#2d0d0d; color:#ef4444; border:1px solid #ef4444; border-radius:20px; padding:4px 14px; font-weight:600; font-size:0.9rem; }

.tip-card {
  background: #0b1422;
  border: 1px solid #30363d;
  border-left: 4px solid #5eead4;
  border-radius: 10px;
  padding: 18px 20px;
  margin-bottom: 12px;
}

.stButton > button {
  background: linear-gradient(135deg, #14b8a6 0%, #818cf8 100%);
  color: #fff;
  border: none;
  border-radius: 10px;
  font-family: 'Poppins', sans-serif;
  font-weight: 600;
  font-size: 1rem;
  padding: 12px 28px;
  transition: opacity 0.2s ease;
  width: 100%;
}
.stButton > button:hover { opacity: 0.88; }

.disclaimer {
  background: #0b1422;
  border-left: 4px solid #5eead4;
  border-radius: 8px;
  padding: 14px 18px;
  color: #8b949e;
  font-size: 0.82rem;
  margin-top: 24px;
}

.section-label {
  font-family: 'Poppins', sans-serif;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1.5px;
  color: #8b949e;
  margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# PLOTLY THEME
# ============================================================================
PLOTLY_THEME = dict(
    paper_bgcolor='#0d1117',
    plot_bgcolor='#161b22',
    font=dict(color='#e6edf3', family='Inter, sans-serif', size=13),
    xaxis=dict(gridcolor='#21262d', zerolinecolor='#21262d'),
    yaxis=dict(gridcolor='#21262d', zerolinecolor='#21262d'),
    colorway=['#5eead4', '#c4b5fd', '#f59e0b', '#ef4444', '#93c5fd']
)

# ============================================================================
# SIDEBAR
# ============================================================================
PAGE_DESCRIPTION = "🔎 Patterns across all ZenFeed screenings"

total_predictions = 0
try:
    response = requests.get(f"{API_URL}/health", timeout=3)
    if response.status_code == 200:
        health_data = response.json()
        total_predictions = health_data.get('total_predictions', 0)
except:
    pass

with st.sidebar:
    st.markdown("## 🌿 ZenFeed")
    st.markdown("<p style='color:#8b949e;font-size:0.85rem;margin-top:-10px;'>Your mind deserves a healthy feed.</p>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown(f"**{PAGE_DESCRIPTION}**")
    st.markdown("---")
    st.markdown(f"🔢 **Total Screenings:** `{total_predictions}`")
    st.markdown("---")
    st.markdown("<p style='color:#8b949e;font-size:0.75rem;'>🌿 Not a clinical diagnosis.</p>", unsafe_allow_html=True)

# ============================================================================
# PAGE HEADER
# ============================================================================
st.markdown("<h1>🔎 Data Insights</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#8b949e;'>Patterns and trends across all ZenFeed screenings.</p>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# ============================================================================
# FETCH DATA
# ============================================================================
try:
    history_response = requests.get(f"{API_URL}/history", timeout=5)
    feature_response = requests.get(f"{API_URL}/feature-importance", timeout=5)
    
    if history_response.status_code != 200 or feature_response.status_code != 200:
        st.warning("⚠️ Unable to fetch data from the API. Please ensure the backend is running.")
        st.stop()
    
    history = history_response.json()['predictions']
    feature_importance = feature_response.json()['feature_importance']
    
    if len(history) == 0:
        st.info("📭 No data available yet. Complete your first ZenScreen assessment!")
        st.stop()
    
    df = pd.DataFrame(history)
    
except requests.exceptions.RequestException as e:
    st.error(f"❌ Cannot connect to API at {API_URL}. Error: {str(e)}")
    st.stop()
except Exception as e:
    st.error(f"❌ Error loading insights data: {str(e)}")
    st.stop()

# ============================================================================
# ROW 1 — FEATURE IMPORTANCE
# ============================================================================
st.markdown("<h3>🎯 Top Risk Factors</h3>", unsafe_allow_html=True)
st.caption("Features that most strongly influence wellness predictions")

# Sort by importance
feat_df = pd.DataFrame({
    'feature': list(feature_importance.keys()),
    'importance': list(feature_importance.values())
}).sort_values('importance', ascending=True)

fig_feat = go.Figure(go.Bar(
    x=feat_df['importance'],
    y=feat_df['feature'],
    orientation='h',
    marker=dict(color='#5eead4'),
    text=[f"{x:.4f}" for x in feat_df['importance']],
    textposition='outside'
))

fig_feat.update_layout(
    xaxis_title="Feature Importance Score",
    yaxis_title="",
    height=400,
    showlegend=False,
    margin=dict(l=20, r=60, t=20, b=60),
    **PLOTLY_THEME
)

# Clean feature names
fig_feat.update_yaxes(
    ticktext=[f.replace('_', ' ').title() for f in feat_df['feature']],
    tickvals=feat_df['feature']
)

st.plotly_chart(fig_feat, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================================
# ROW 2 — BOX PLOTS (4 COMPOSITE SCORES)
# ============================================================================
st.markdown("<h3>📦 Composite Score Distributions by Risk Level</h3>", unsafe_allow_html=True)

if all(col in df.columns for col in ['adhd_score', 'anxiety_score', 'self_esteem_score', 'depression_score', 'risk_level']):
    
    col1, col2, col3, col4 = st.columns(4)
    
    composite_info = [
        ('adhd_score', '🎯 ADHD', col1),
        ('anxiety_score', '😰 Anxiety', col2),
        ('self_esteem_score', '🪞 Self-Esteem', col3),
        ('depression_score', '😔 Depression', col4)
    ]
    
    color_map = {'Healthy': '#5eead4', 'At Risk': '#f59e0b', 'Burnout': '#ef4444'}
    
    for score_col, title, col in composite_info:
        with col:
            fig_box = go.Figure()
            
            for risk_level, color in color_map.items():
                data = df[df['risk_level'] == risk_level][score_col]
                
                if len(data) > 0:
                    # Box plot
                    fig_box.add_trace(go.Box(
                        y=data,
                        x=[risk_level] * len(data),
                        name=risk_level,
                        marker=dict(color=color),
                        boxmean=True,
                        showlegend=False
                    ))
            
            # Merge xaxis settings
            layout_settings = PLOTLY_THEME.copy()
            layout_settings['xaxis'] = {**PLOTLY_THEME['xaxis'], 'showgrid': False}
            
            fig_box.update_layout(
                title=title,
                yaxis_title="Score (1-5)",
                height=350,
                margin=dict(l=20, r=20, t=40, b=60),
                **layout_settings
            )
            
            st.plotly_chart(fig_box, use_container_width=True)
else:
    st.info("Composite score data not available")

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================================
# ROW 3 — VIOLIN CHART & RISK BY OCCUPATION
# ============================================================================
col1, col2 = st.columns(2)

with col1:
    st.markdown("<h3>🎻 SM Hours by Risk Level</h3>", unsafe_allow_html=True)
    
    if 'social_media_hours' in df.columns and 'risk_level' in df.columns:
        fig_violin = go.Figure()
        
        color_map = {'Healthy': '#5eead4', 'At Risk': '#f59e0b', 'Burnout': '#ef4444'}
        
        for risk_level, color in color_map.items():
            data = df[df['risk_level'] == risk_level]['social_media_hours']
            
            if len(data) > 0:
                fig_violin.add_trace(go.Violin(
                    y=data,
                    name=risk_level,
                    box_visible=True,
                    meanline_visible=True,
                    fillcolor=color,
                    line=dict(color=color),
                    opacity=0.6
                ))
        
        fig_violin.update_layout(
            yaxis_title="Daily Social Media Hours",
            height=400,
            showlegend=True,
            legend=dict(title="Risk Level"),
            margin=dict(l=20, r=20, t=20, b=60),
            **PLOTLY_THEME
        )
        
        st.plotly_chart(fig_violin, use_container_width=True)
    else:
        st.info("Social media hours data not available")

with col2:
    st.markdown("<h3>💼 Risk Distribution by Occupation</h3>", unsafe_allow_html=True)
    
    if 'occupation' in df.columns and 'risk_level' in df.columns:
        occ_risk = df.groupby(['occupation', 'risk_level']).size().reset_index(name='count')
        
        fig_occ = px.bar(
            occ_risk,
            x='occupation',
            y='count',
            color='risk_level',
            color_discrete_map={'Healthy': '#5eead4', 'At Risk': '#f59e0b', 'Burnout': '#ef4444'},
            barmode='stack'
        )
        
        fig_occ.update_layout(
            xaxis_title="Occupation",
            yaxis_title="Count",
            legend=dict(title="Risk Level"),
            height=400,
            margin=dict(l=20, r=20, t=20, b=60),
            **PLOTLY_THEME
        )
        
        st.plotly_chart(fig_occ, use_container_width=True)
    else:
        st.info("Occupation data not available")

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================================
# ROW 4 — RISK BY GENDER & CORRELATION HEATMAP
# ============================================================================
col1, col2 = st.columns(2)

with col1:
    st.markdown("<h3>👥 Risk Distribution by Gender</h3>", unsafe_allow_html=True)
    
    if 'gender' in df.columns and 'risk_level' in df.columns:
        gender_risk = df.groupby(['gender', 'risk_level']).size().reset_index(name='count')
        
        fig_gender = px.bar(
            gender_risk,
            x='gender',
            y='count',
            color='risk_level',
            color_discrete_map={'Healthy': '#5eead4', 'At Risk': '#f59e0b', 'Burnout': '#ef4444'},
            barmode='group'
        )
        
        fig_gender.update_layout(
            xaxis_title="Gender",
            yaxis_title="Count",
            legend=dict(title="Risk Level"),
            height=400,
            margin=dict(l=20, r=20, t=20, b=60),
            **PLOTLY_THEME
        )
        
        st.plotly_chart(fig_gender, use_container_width=True)
    else:
        st.info("Gender data not available")

with col2:
    st.markdown("<h3>🔗 Feature Correlation Matrix</h3>", unsafe_allow_html=True)
    
    corr_cols = ['wellness_score', 'adhd_score', 'anxiety_score', 'self_esteem_score', 
                 'depression_score', 'social_media_hours', 'age']
    corr_cols = [col for col in corr_cols if col in df.columns]
    
    if len(corr_cols) > 2:
        corr_df = df[corr_cols].corr()
        
        fig_corr = px.imshow(
            corr_df,
            text_auto='.2f',
            color_continuous_scale='RdBu_r',
            zmin=-1,
            zmax=1,
            aspect="auto"
        )
        
        fig_corr.update_layout(
            height=400,
            margin=dict(l=20, r=20, t=20, b=20),
            coloraxis_colorbar=dict(title="Correlation"),
            **PLOTLY_THEME
        )
        
        # Clean axis labels
        clean_labels = [c.replace('_', ' ').title() for c in corr_df.columns]
        fig_corr.update_xaxes(ticktext=clean_labels, tickvals=list(range(len(clean_labels))))
        fig_corr.update_yaxes(ticktext=clean_labels, tickvals=list(range(len(clean_labels))))
        
        st.plotly_chart(fig_corr, use_container_width=True)
    else:
        st.info("Insufficient numeric data for correlation analysis")

st.markdown("<br><br>", unsafe_allow_html=True)

# ============================================================================
# ROW 5 — BURNOUT PROFILE CARD
# ============================================================================
st.markdown("<h3>🔥 Burnout Profile</h3>", unsafe_allow_html=True)

if 'risk_level' in df.columns:
    burnout_df = df[df['risk_level'] == 'Burnout']
    
    if len(burnout_df) > 0:
        # Calculate statistics
        avg_adhd = burnout_df['adhd_score'].mean() if 'adhd_score' in burnout_df.columns else 0
        avg_anxiety = burnout_df['anxiety_score'].mean() if 'anxiety_score' in burnout_df.columns else 0
        avg_self_esteem = burnout_df['self_esteem_score'].mean() if 'self_esteem_score' in burnout_df.columns else 0
        avg_depression = burnout_df['depression_score'].mean() if 'depression_score' in burnout_df.columns else 0
        avg_wellness = burnout_df['wellness_score'].mean() if 'wellness_score' in burnout_df.columns else 0
        avg_sm_hours = burnout_df['social_media_hours'].mean() if 'social_media_hours' in burnout_df.columns else 0
        
        most_common_occ = burnout_df['occupation'].mode()[0] if 'occupation' in burnout_df.columns and not burnout_df['occupation'].mode().empty else 'N/A'
        most_common_gender = burnout_df['gender'].mode()[0] if 'gender' in burnout_df.columns and not burnout_df['gender'].mode().empty else 'N/A'
        
        if 'age' in burnout_df.columns:
            def age_group(age):
                if age < 19:
                    return '13-18'
                elif age < 26:
                    return '19-25'
                elif age < 36:
                    return '26-35'
                else:
                    return '36+'
            
            burnout_df['age_group'] = burnout_df['age'].apply(age_group)
            most_common_age = burnout_df['age_group'].mode()[0] if not burnout_df['age_group'].mode().empty else 'N/A'
        else:
            most_common_age = 'N/A'
        
        # Display profile
        st.markdown(f"""
        <div class='zen-card' style='border-left:4px solid #ef4444;'>
            <p style='color:#c9d1d9; font-size:0.95rem; line-height:1.8; margin:0 0 20px 0;'>
                Based on <b>{len(burnout_df)}</b> Burnout cases in the dataset, the typical profile shows 
                an average wellness score of <b>{avg_wellness:.1f}/100</b> with elevated depression 
                (<b>{avg_depression:.2f}/5.0</b>) and anxiety (<b>{avg_anxiety:.2f}/5.0</b>) indicators. 
                Most frequently observed in <b>{most_common_occ}</b> individuals within the 
                <b>{most_common_age}</b> age range. Average daily social media consumption is 
                <b>{avg_sm_hours:.1f} hours</b>.
            </p>
        """, unsafe_allow_html=True)
        
        # Summary table
        profile_data = {
            'Metric': ['Avg Wellness Score', 'ADHD Score', 'Anxiety Score', 'Self-Esteem Score', 
                      'Depression Score', 'SM Hours/Day', 'Most Common Occupation', 
                      'Most Common Gender', 'Most Common Age Group'],
            'Value': [f'{avg_wellness:.1f}/100', f'{avg_adhd:.2f}/5.0', f'{avg_anxiety:.2f}/5.0',
                     f'{avg_self_esteem:.2f}/5.0', f'{avg_depression:.2f}/5.0', f'{avg_sm_hours:.1f}h',
                     most_common_occ, most_common_gender, most_common_age]
        }
        
        profile_table = pd.DataFrame(profile_data)
        
        st.dataframe(profile_table, use_container_width=True, hide_index=True)
        
        st.markdown("""
        </div>
        """, unsafe_allow_html=True)
        
        st.caption("⚠️ Anonymized statistical pattern — not a clinical profile.")
        
    else:
        st.info("No Burnout cases recorded yet.")
else:
    st.info("Risk level data not available")

# ============================================================================
# DISCLAIMER
# ============================================================================
st.markdown("""
<div class='disclaimer'>
    ⚠️ All insights are derived from anonymized, aggregated data. Patterns shown are statistical 
    correlations, not causal relationships. Individual experiences vary significantly. This page 
    is for research and awareness purposes only.
</div>
""", unsafe_allow_html=True)
