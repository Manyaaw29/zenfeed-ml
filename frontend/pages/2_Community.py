"""
🌿 ZenFeed — Community Dashboard
Anonymized insights from all ZenScreen assessments.
"""

import streamlit as st
import requests
import os
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# ============================================================================
# PAGE CONFIG
# ============================================================================
st.set_page_config(
    page_title="ZenFeed · Dashboard",
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
.zen-kpi-label {
  font-size: 0.88rem;
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
PAGE_DESCRIPTION = "📊 Community wellness data — anonymized"

total_predictions = 0
try:
    response = requests.get(f"{API_URL}/stats", timeout=5)
    if response.status_code == 200:
        total_predictions = response.json().get('total_predictions', 0)
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
    st.markdown("<p style='color:#8b949e;font-size:0.75rem;'>For informational purposes only — not a substitute for professional mental health advice. 🌿</p>", unsafe_allow_html=True)

# ============================================================================
# PAGE HEADER
# ============================================================================
st.markdown("<h1>📊 Community Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#8b949e;'>Anonymized insights from all ZenScreen assessments.</p>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# ============================================================================
# FETCH DATA
# ============================================================================
try:
    stats_response = requests.get(f"{API_URL}/stats", timeout=5)
    history_response = requests.get(f"{API_URL}/history", timeout=5)
    
    if stats_response.status_code != 200 or history_response.status_code != 200:
        st.warning("⚠️ Unable to fetch data from the API. Please ensure the backend is running.")
        st.stop()
    
    stats = stats_response.json()
    history = history_response.json()['predictions']
    
    if len(history) == 0:
        st.info("📭 No data available yet. Complete your first ZenScreen assessment to see community insights!")
        st.stop()
    
    df = pd.DataFrame(history)
    
except requests.exceptions.RequestException as e:
    st.error(f"❌ Cannot connect to API at {API_URL}. Error: {str(e)}")
    st.stop()
except Exception as e:
    st.error(f"❌ Error loading dashboard data: {str(e)}")
    st.stop()

# ============================================================================
# ROW 1 — KPI CARDS
# ============================================================================
col1, col2, col3, col4 = st.columns(4)

total_screenings = stats['total_predictions']
avg_wellness = stats['avg_wellness_score']
risk_dist = stats['risk_distribution']
burnout_pct = round((risk_dist.get('Burnout', 0) / total_screenings * 100) if total_screenings > 0 else 0, 1)
avg_sm_hours = stats['avg_social_media_hours']

with col1:
    st.markdown(f"""
    <div class='zen-kpi'>
        <div class='zen-kpi-value'>{total_screenings}</div>
        <div class='zen-kpi-label'>Total Screenings</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    score_color = '#5eead4' if avg_wellness > 67 else '#f59e0b' if avg_wellness > 34 else '#ef4444'
    st.markdown(f"""
    <div class='zen-kpi'>
        <div class='zen-kpi-value' style='color:{score_color};'>{avg_wellness:.1f}</div>
        <div class='zen-kpi-label'>Avg Wellness Score</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    burnout_color = '#ef4444' if burnout_pct > 20 else '#f59e0b' if burnout_pct > 10 else '#5eead4'
    st.markdown(f"""
    <div class='zen-kpi' style='border-top-color:{burnout_color};'>
        <div class='zen-kpi-value' style='color:{burnout_color};'>{burnout_pct}%</div>
        <div class='zen-kpi-label'>Burnout Rate</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class='zen-kpi'>
        <div class='zen-kpi-value'>{avg_sm_hours:.1f}h</div>
        <div class='zen-kpi-label'>Avg Daily SM Hours</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================================
# ROW 2 — DONUT CHART & SCATTER PLOT
# ============================================================================
col1, col2 = st.columns(2)

with col1:
    st.markdown("<h3>Risk Distribution</h3>", unsafe_allow_html=True)
    
    risk_labels = list(risk_dist.keys())
    risk_values = list(risk_dist.values())
    risk_colors = ['#5eead4', '#f59e0b', '#ef4444']
    
    fig_donut = go.Figure(data=[go.Pie(
        labels=risk_labels,
        values=risk_values,
        hole=0.5,
        marker=dict(colors=risk_colors),
        textposition='outside',
        textinfo='label+percent'
    )])
    
    fig_donut.update_layout(
        height=400,
        showlegend=False,
        margin=dict(l=20, r=20, t=20, b=20),
        **PLOTLY_THEME
    )
    
    st.plotly_chart(fig_donut, use_container_width=True)

with col2:
    st.markdown("<h3>Social Media Hours vs Wellness</h3>", unsafe_allow_html=True)
    
    if 'social_media_hours' in df.columns and 'wellness_score' in df.columns:
        color_map = {'Healthy': '#5eead4', 'At Risk': '#f59e0b', 'Burnout': '#ef4444'}
        
        fig_scatter = px.scatter(
            df,
            x='social_media_hours',
            y='wellness_score',
            color='risk_level',
            color_discrete_map=color_map,
            opacity=0.7,
            size_max=15,
            hover_data=['age', 'gender']
        )
        
        fig_scatter.update_traces(marker=dict(size=10))
        
        fig_scatter.update_layout(
            xaxis_title="Daily Social Media Hours",
            yaxis_title="Wellness Score",
            height=400,
            legend=dict(title="Risk Level"),
            margin=dict(l=20, r=20, t=20, b=60),
            **PLOTLY_THEME
        )
        
        st.plotly_chart(fig_scatter, use_container_width=True)
    else:
        st.info("Insufficient data for scatter plot")

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================================
# ROW 3 — RISK BY AGE GROUP & SCREENINGS OVER TIME
# ============================================================================
col1, col2 = st.columns(2)

with col1:
    st.markdown("<h3>Risk Level by Age Group</h3>", unsafe_allow_html=True)
    
    if 'age' in df.columns:
        def age_group(age):
            if age < 19:
                return '13-18'
            elif age < 26:
                return '19-25'
            elif age < 36:
                return '26-35'
            else:
                return '36+'
        
        df['age_group'] = df['age'].apply(age_group)
        
        age_risk = df.groupby(['age_group', 'risk_level']).size().reset_index(name='count')
        
        fig_age = px.bar(
            age_risk,
            x='age_group',
            y='count',
            color='risk_level',
            color_discrete_map={'Healthy': '#5eead4', 'At Risk': '#f59e0b', 'Burnout': '#ef4444'},
            barmode='group'
        )
        
        fig_age.update_layout(
            xaxis_title="Age Group",
            yaxis_title="Count",
            legend=dict(title="Risk Level"),
            height=400,
            margin=dict(l=20, r=20, t=20, b=60),
            **PLOTLY_THEME
        )
        
        st.plotly_chart(fig_age, use_container_width=True)
    else:
        st.info("Age data not available")

with col2:
    st.markdown("<h3>Screenings Over Time</h3>", unsafe_allow_html=True)
    
    if 'timestamp' in df.columns:
        df['date'] = pd.to_datetime(df['timestamp']).dt.date
        time_series = df.groupby('date').size().reset_index(name='count')
        time_series['cumulative'] = time_series['count'].cumsum()
        
        if len(time_series) < 7:
            st.info(f"📊 {len(time_series)} data point(s) available. Time trends become clearer with more data over multiple days.")
        
        fig_time = go.Figure()
        
        fig_time.add_trace(go.Scatter(
            x=time_series['date'],
            y=time_series['cumulative'],
            mode='lines+markers',
            line=dict(color='#5eead4', width=3),
            fill='tozeroy',
            fillcolor='rgba(0, 212, 170, 0.1)',
            marker=dict(size=8),
            name='Cumulative Screenings'
        ))
        
        fig_time.update_layout(
            xaxis_title="Date",
            yaxis_title="Total Screenings",
            height=400,
            showlegend=False,
            margin=dict(l=20, r=20, t=20, b=60),
            **PLOTLY_THEME
        )
        
        st.plotly_chart(fig_time, use_container_width=True)
    else:
        st.info("Timestamp data not available")

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================================
# ROW 4 — RADAR CHART & WELLNESS BY OCCUPATION
# ============================================================================
col1, col2 = st.columns(2)

with col1:
    st.markdown("<h3>Composite Scores by Risk Level</h3>", unsafe_allow_html=True)
    
    if all(col in df.columns for col in ['adhd_score', 'anxiety_score', 'self_esteem_score', 'depression_score']):
        radar_data = df.groupby('risk_level')[['adhd_score', 'anxiety_score', 'self_esteem_score', 'depression_score']].mean()
        
        fig_radar = go.Figure()
        
        categories = ['ADHD', 'Anxiety', 'Self-Esteem', 'Depression']
        colors_radar = {'Healthy': '#5eead4', 'At Risk': '#f59e0b', 'Burnout': '#ef4444'}
        
        for risk, color in colors_radar.items():
            if risk in radar_data.index:
                values = radar_data.loc[risk].values.tolist()
                values.append(values[0])  # Close the polygon
                
                fig_radar.add_trace(go.Scatterpolar(
                    r=values,
                    theta=categories + [categories[0]],
                    fill='toself',
                    name=risk,
                    line=dict(color=color),
                    fillcolor=color,
                    opacity=0.4
                ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 5], gridcolor='#21262d'),
                angularaxis=dict(gridcolor='#21262d')
            ),
            height=400,
            showlegend=True,
            legend=dict(title="Risk Level"),
            margin=dict(l=60, r=60, t=40, b=40),
            **PLOTLY_THEME
        )
        
        st.plotly_chart(fig_radar, use_container_width=True)
    else:
        st.info("Composite score data not available")

with col2:
    st.markdown("<h3>Avg Wellness by Occupation</h3>", unsafe_allow_html=True)
    
    if 'occupation' in df.columns and 'wellness_score' in df.columns:
        occ_wellness = df.groupby('occupation')['wellness_score'].mean().sort_values(ascending=True)
        
        colors_occ = ['#5eead4' if x > 67 else '#f59e0b' if x > 34 else '#ef4444' for x in occ_wellness.values]
        
        fig_occ = go.Figure(go.Bar(
            x=occ_wellness.values,
            y=occ_wellness.index,
            orientation='h',
            marker=dict(color=colors_occ),
            text=[f"{x:.1f}" for x in occ_wellness.values],
            textposition='outside'
        ))
        
        fig_occ.update_layout(
            xaxis_title="Average Wellness Score",
            yaxis_title="",
            height=400,
            showlegend=False,
            margin=dict(l=20, r=40, t=20, b=60),
            **PLOTLY_THEME
        )
        
        st.plotly_chart(fig_occ, use_container_width=True)
    else:
        st.info("Occupation data not available")

st.markdown("<br><br>", unsafe_allow_html=True)

# ============================================================================
# ROW 5 — DATA TABLE WITH FILTERS
# ============================================================================
st.markdown("<h3>📋 Full Screening Data</h3>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# Filters
col1, col2, col3 = st.columns([2, 2, 1])

with col1:
    risk_filter = st.multiselect(
        "Filter by Risk Level:",
        options=['Healthy', 'At Risk', 'Burnout'],
        default=['Healthy', 'At Risk', 'Burnout']
    )

with col2:
    wellness_range = st.slider(
        "Wellness Score Range:",
        min_value=0,
        max_value=100,
        value=(0, 100)
    )

with col3:
    st.markdown("<br>", unsafe_allow_html=True)
    show_all = st.checkbox("Show all columns", value=False)

# Filter dataframe
df_filtered = df[
    (df['risk_level'].isin(risk_filter)) &
    (df['wellness_score'] >= wellness_range[0]) &
    (df['wellness_score'] <= wellness_range[1])
].copy()

# Select columns to display
if show_all:
    display_cols = df_filtered.columns.tolist()
else:
    display_cols = ['timestamp', 'wellness_score', 'risk_level', 'adhd_score', 
                    'anxiety_score', 'self_esteem_score', 'depression_score', 
                    'age', 'gender', 'occupation', 'model_used']
    display_cols = [col for col in display_cols if col in df_filtered.columns]

df_display = df_filtered[display_cols].copy()

# Format timestamp
if 'timestamp' in df_display.columns:
    df_display['timestamp'] = pd.to_datetime(df_display['timestamp']).dt.strftime('%Y-%m-%d %H:%M')

# Style dataframe
def style_risk(val):
    if val == 'Healthy':
        return 'background-color: #0d2f22; color: #5eead4;'
    elif val == 'At Risk':
        return 'background-color: #2d1f00; color: #f59e0b;'
    elif val == 'Burnout':
        return 'background-color: #2d0d0d; color: #ef4444;'
    return ''

if 'risk_level' in df_display.columns:
    styled_df = df_display.style.applymap(style_risk, subset=['risk_level'])
else:
    styled_df = df_display

st.dataframe(styled_df, use_container_width=True, height=400)

st.caption(f"Showing {len(df_filtered)} of {len(df)} total records")

# Download button
col1, col2, col3 = st.columns([1, 1, 2])
with col1:
    csv = df_filtered.to_csv(index=False)
    st.download_button(
        label="⬇️ Download CSV",
        data=csv,
        file_name=f"zenfeed_data_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

# ============================================================================
# DISCLAIMER
# ============================================================================
st.markdown("""
<div class='disclaimer'>
    ⚠️ All data is anonymized and aggregated. Individual responses cannot be traced back to specific users.
    This dashboard is for informational and research purposes only.
</div>
""", unsafe_allow_html=True)
