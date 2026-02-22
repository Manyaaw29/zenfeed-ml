"""
🌿 ZenFeed — ZenScreen Assessment
Complete the form to get your personalized wellness report.
"""

import streamlit as st
import requests
import os
import plotly.graph_objects as go
import pandas as pd
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime

# ============================================================================
# PAGE CONFIG
# ============================================================================
st.set_page_config(
    page_title="ZenFeed · ZenScreen",
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
  margin-bottom: 16px;
  transition: box-shadow 0.25s ease, transform 0.2s ease;
}
.zen-card:hover {
  box-shadow: 0 0 24px rgba(94, 234, 212, 0.08);
  transform: translateY(-2px);
}

.zen-kpi {
  background: #0b1422;
  border: 1px solid #30363d;
  border-top: 3px solid #5eead4;
  border-radius: 12px;
  padding: 20px;
  text-align: center;
}
.zen-kpi-value {
  font-family: 'Poppins', sans-serif;
  font-size: 2rem;
  font-weight: 700;
  color: #5eead4;
}
.zen-kpi-label {
  font-size: 0.85rem;
  color: #8b949e;
  margin-top: 4px;
}

.badge-healthy { background:#052d16; color:#22c55e; border:1px solid #22c55e; border-radius:20px; padding:4px 14px; font-weight:600; font-size:0.9rem; }
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

.gradient-section-1 {
  background: linear-gradient(135deg, rgba(13, 148, 136, 0.12) 0%, rgba(8, 145, 178, 0.06) 100%);
  border: 1px solid rgba(94, 234, 212, 0.22);
  border-left: 4px solid #0d9488;
  border-radius: 16px;
  padding: 24px 28px 12px 28px;
  margin-bottom: 8px;
  box-shadow: 0 4px 24px rgba(13, 148, 136, 0.1);
}

.gradient-section-2 {
  background: linear-gradient(135deg, rgba(109, 40, 217, 0.12) 0%, rgba(99, 102, 241, 0.06) 100%);
  border: 1px solid rgba(196, 181, 253, 0.22);
  border-left: 4px solid #7c3aed;
  border-radius: 16px;
  padding: 24px 28px 12px 28px;
  margin-bottom: 8px;
  box-shadow: 0 4px 24px rgba(109, 40, 217, 0.1);
}

.gradient-section-3 {
  background: linear-gradient(135deg, rgba(217, 119, 6, 0.12) 0%, rgba(251, 191, 36, 0.06) 100%);
  border: 1px solid rgba(245, 158, 11, 0.25);
  border-left: 4px solid #d97706;
  border-radius: 16px;
  padding: 24px 28px 12px 28px;
  margin-bottom: 8px;
  box-shadow: 0 4px 24px rgba(217, 119, 6, 0.1);
}

.section-heading {
  font-family: 'Poppins', sans-serif;
  font-size: 1.25rem;
  font-weight: 700;
  color: #5eead4;
  margin: 0 0 4px 0;
  letter-spacing: -0.3px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.section-subtext {
  font-size: 0.82rem;
  color: #64748b;
  margin: 0 0 16px 0;
  padding-left: 2px;
}

.section-heading-2 {
  color: #c4b5fd;
}

.section-heading-3 {
  color: #fbbf24;
}



.progress-steps {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 12px;
  margin: 30px 0;
  padding: 20px;
  background: #0b1422;
  border-radius: 12px;
  border: 1px solid #30363d;
}

.progress-step {
  display: flex;
  align-items: center;
  gap: 8px;
}

.step-circle {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.9rem;
  border: 2px solid #30363d;
  background: #0d1117;
  color: #8b949e;
}

.step-circle.active {
  background: linear-gradient(135deg, #14b8a6 0%, #818cf8 100%);
  border: none;
  color: #fff;
}

.step-label {
  font-size: 0.85rem;
  color: #8b949e;
  font-weight: 500;
}

.step-label.active {
  color: #5eead4;
}

.step-connector {
  width: 40px;
  height: 2px;
  background: #30363d;
}

.crisis-banner {
  background: linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, rgba(220, 38, 38, 0.1) 100%);
  border: 2px solid #ef4444;
  border-radius: 16px;
  padding: 24px;
  margin: 24px 0;
  text-align: center;
}

.crisis-title {
  font-family: 'Poppins', sans-serif;
  font-size: 1.5rem;
  font-weight: 700;
  color: #ef4444;
  margin-bottom: 12px;
}

.crisis-text {
  color: #e6edf3;
  font-size: 1rem;
  line-height: 1.6;
  margin-bottom: 16px;
}

.crisis-phone {
  font-family: 'Poppins', sans-serif;
  font-size: 2rem;
  font-weight: 800;
  color: #ef4444;
  margin: 16px 0;
  letter-spacing: 2px;
}

.hotline-card {
  background: #0b1422;
  border: 1px solid #ef4444;
  border-radius: 12px;
  padding: 16px;
  margin: 12px 0;
  text-align: left;
}

.hotline-name {
  font-weight: 700;
  color: #5eead4;
  font-size: 1.1rem;
  margin-bottom: 6px;
}

.hotline-number {
  font-family: 'Poppins', sans-serif;
  font-size: 1.3rem;
  font-weight: 700;
  color: #ef4444;
  margin: 4px 0;
}

.hotline-desc {
  color: #8b949e;
  font-size: 0.85rem;
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
PAGE_DESCRIPTION = "📋 Complete the form to get your ZenScore"

if 'total_predictions' not in st.session_state:
    st.session_state.total_predictions = 0
try:
    response = requests.get(f"{API_URL}/stats", timeout=5)
    if response.status_code == 200:
        fetched = response.json().get('total_predictions', 0)
        if fetched > 0:
            st.session_state.total_predictions = fetched
except:
    pass
total_predictions = st.session_state.total_predictions

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
st.markdown("<h1>🌿 ZenScreen</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#8b949e;'>Your personalized mental wellness assessment — anonymous, free, takes 2 minutes.</p>", unsafe_allow_html=True)

# Progress Steps Indicator
st.markdown("""
<div class='progress-steps'>
    <div class='progress-step'>
        <div class='step-circle active'>1</div>
        <span class='step-label active'>Social Media</span>
    </div>
    <div class='step-connector'></div>
    <div class='progress-step'>
        <div class='step-circle active'>2</div>
        <span class='step-label active'>How You Feel</span>
    </div>
    <div class='step-connector'></div>
    <div class='progress-step'>
        <div class='step-circle active'>3</div>
        <span class='step-label active'>About You</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================================
# FORM
# ============================================================================
with st.form("zenscreen_form"):
    
    # ========== SECTION 1: SOCIAL MEDIA HABITS ==========
    st.markdown("""
    <div class='gradient-section-1'>
        <div class='section-heading'>📱 Social Media Habits</div>
        <p class='section-subtext'>How you use social media day-to-day</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        social_media_hours = st.selectbox(
            "Daily time on social media?",
            ["Less than 1 hr", "1–2 hrs", "2–3 hrs", "3–4 hrs", "4–5 hrs", "More than 5 hrs"],
            index=2
        )
        
        purposeless_use = st.slider(
            "Scrolling without a purpose?",
            1, 5, 3,
            help="1 = Never, 5 = Very frequently"
        )
        
        distracted_by_sm = st.slider(
            "How easily does social media distract you?",
            1, 5, 3,
            help="1 = Never, 5 = Always"
        )
        
        restless_without_sm = st.slider(
            "Restless when you can't check your phone?",
            1, 5, 2,
            help="1 = Never feel this, 5 = Extremely restless"
        )
        
        easily_distracted = st.slider(
            "How easily distracted are you in general?",
            1, 5, 3,
            help="1 = Very focused, 5 = Very easily distracted"
        )
    
    with col2:
        compare_to_others = st.slider(
            "How often do you compare yourself online?",
            1, 5, 3,
            help="1 = Never compare, 5 = Constantly"
        )
        
        feelings_about_comparisons = st.slider(
            "How do you feel after comparing yourself?",
            1, 5, 3,
            help="1 = Feel better, 5 = Feel much worse"
        )
        
        seek_validation = st.slider(
            "Do likes & comments affect your mood?",
            1, 5, 2,
            help="1 = Not at all, 5 = Extremely dependent on likes"
        )
        
        bothered_by_worries = st.slider(
            "How often are you bothered by worries?",
            1, 5, 3,
            help="1 = Rarely, 5 = Almost always"
        )
        
        difficulty_concentrating = st.slider(
            "How hard is it to concentrate on tasks?",
            1, 5, 3,
            help="1 = No difficulty, 5 = Very difficult"
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ========== SECTION 2: HOW YOU FEEL ==========
    st.markdown("""
    <div class='gradient-section-2'>
        <div class='section-heading section-heading-2'>💭 How You Feel</div>
        <p class='section-subtext'>Your emotional state over the past 2 weeks</p>
    </div>
    """, unsafe_allow_html=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        feel_depressed = st.slider(
            "How often do you feel depressed or down?",
            1, 5, 2,
            help="1 = Rarely, 5 = Most days"
        )
        
        interest_fluctuation = st.slider(
            "How much does your interest in activities fluctuate?",
            1, 5, 3,
            help="1 = Very stable, 5 = Very unstable"
        )
    
    with col4:
        sleep_issues = st.slider(
            "How often do you have trouble sleeping?",
            1, 5, 2,
            help="1 = No issues, 5 = Every night"
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ========== SECTION 3: ABOUT YOU ==========
    st.markdown("""
    <div class='gradient-section-3'>
        <div class='section-heading section-heading-3'>👤 About You</div>
        <p class='section-subtext'>A little context helps the model personalise your result</p>
    </div>
    """, unsafe_allow_html=True)
    
    col5, col6 = st.columns(2)
    
    with col5:
        age = st.number_input("Age", min_value=13, max_value=65, value=21, step=1)
        gender = st.selectbox("Gender", ["Male", "Female", "Non-binary", "Prefer not to say"])
    
    with col6:
        relationship_status = st.selectbox(
            "Relationship Status",
            ["Single", "In a relationship", "Married", "Divorced", "Other"]
        )
        occupation = st.selectbox(
            "Occupation",
            ["Student", "Working Professional", "Both", "Neither"]
        )
    
    # FULL WIDTH — Platforms and Model
    st.markdown("<br>", unsafe_allow_html=True)
    
    platforms = st.multiselect(
        "Which social media platforms do you use? (logging only, not used in prediction)",
        ["Instagram", "TikTok", "Twitter/X", "YouTube", "Facebook", "Snapchat", "LinkedIn", "Reddit", "Pinterest", "Other"],
        default=["Instagram", "YouTube"]
    )

    # SUBMIT BUTTON
    st.markdown("<br><br>", unsafe_allow_html=True)
    submitted = st.form_submit_button("🌿 Check My ZenScore")

# ============================================================================
# PROCESS SUBMISSION
# ============================================================================
if submitted:

    model_name = "Logistic Regression"
    
    # Prepare payload
    payload = {
        "age": age,
        "gender": gender,
        "relationship_status": relationship_status,
        "occupation": occupation,
        "social_media_hours": social_media_hours,
        "purposeless_use": purposeless_use,
        "distracted_by_sm": distracted_by_sm,
        "restless_without_sm": restless_without_sm,
        "easily_distracted": easily_distracted,
        "bothered_by_worries": bothered_by_worries,
        "difficulty_concentrating": difficulty_concentrating,
        "compare_to_others": compare_to_others,
        "feelings_about_comparisons": feelings_about_comparisons,
        "seek_validation": seek_validation,
        "feel_depressed": feel_depressed,
        "interest_fluctuation": interest_fluctuation,
        "sleep_issues": sleep_issues,
        "model": model_name
    }
    
    # Call API
    with st.spinner("🤖 Analyzing your digital wellness patterns..."):
        try:
            response = requests.post(f"{API_URL}/predict", json=payload, timeout=10)
            
            if response.status_code == 200:
                result = response.json()

                st.markdown("<hr style='border:none;border-top:2px solid #21262d;margin:40px 0;'>", unsafe_allow_html=True)
                st.markdown("<h2 style='text-align:center;'>📊 Your ZenScore Results</h2>", unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                
                # ============================================================
                # CRISIS DETECTION
                # ============================================================
                risk_level = result['risk_level']
                wellness_score = result['wellness_score']
                
                if risk_level in ['At Risk', 'Burnout'] or wellness_score < 40:
                    st.markdown("""
                    <div class='crisis-banner'>
                        <div class='crisis-title'>🚨 You're Not Alone — Help is Available 24/7</div>
                        <p class='crisis-text'>Your responses indicate you may be experiencing significant distress. Support is available right now — reaching out is a sign of strength.</p>
                    </div>
                    """, unsafe_allow_html=True)
                    c1, c2 = st.columns(2)
                    with c1:
                        st.markdown("""
                        <div class='hotline-card'>
                            <div class='hotline-name'>🇮🇳 iCall — TISS</div>
                            <div class='hotline-number'>9152987821</div>
                            <div class='hotline-desc'>Mon–Sat · 8 AM–10 PM · Free</div>
                        </div>""", unsafe_allow_html=True)
                    with c2:
                        st.markdown("""
                        <div class='hotline-card'>
                            <div class='hotline-name'>🌍 Vandrevala Foundation</div>
                            <div class='hotline-number'>1860-2662-345</div>
                            <div class='hotline-desc'>24/7 · Multilingual · Free</div>
                        </div>""", unsafe_allow_html=True)
                    st.markdown("<p style='color:#8b949e;font-size:0.85rem;margin:12px 0 0 0;'>💚 <strong style='color:#e6edf3;'>You deserve support.</strong> These services are free, confidential, and staffed by trained professionals.</p>", unsafe_allow_html=True)
                
                # ============================================================
                # BLOCK 1 — WELLNESS GAUGE
                # ============================================================
                wellness_score = result['wellness_score']
                risk_level = result['risk_level']
                
                # Gauge color
                if risk_level == 'Healthy':
                    gauge_color = '#5eead4'
                    badge_class = 'badge-healthy'
                elif risk_level == 'At Risk':
                    gauge_color = '#f59e0b'
                    badge_class = 'badge-atrisk'
                else:
                    gauge_color = '#ef4444'
                    badge_class = 'badge-burnout'
                
                fig_gauge = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=wellness_score,
                    title={'text': "Wellness Score", 'font': {'size': 20, 'color': '#e6edf3', 'family': 'Poppins'}},
                    number={'font': {'size': 48, 'color': gauge_color, 'family': 'Poppins'}},
                    gauge={
                        'axis': {'range': [0, 100], 'tickcolor': '#8b949e'},
                        'bar': {'color': gauge_color, 'thickness': 0.75},
                        'bgcolor': '#161b22',
                        'borderwidth': 2,
                        'bordercolor': '#30363d',
                        'steps': [
                            {'range': [0, 33], 'color': 'rgba(239, 68, 68, 0.15)'},
                            {'range': [33, 67], 'color': 'rgba(245, 158, 11, 0.15)'},
                            {'range': [67, 100], 'color': 'rgba(94, 234, 212, 0.08)'}
                        ],
                        'threshold': {
                            'line': {'color': gauge_color, 'width': 4},
                            'thickness': 0.75,
                            'value': wellness_score
                        }
                    }
                ))
                
                fig_gauge.update_layout(
                    height=350,
                    margin=dict(l=20, r=20, t=60, b=20),
                    **PLOTLY_THEME
                )
                
                st.plotly_chart(fig_gauge, use_container_width=True)
                
                # Risk badge and interpretation
                interpretations = {
                    'Healthy': 'Your digital habits appear balanced. Keep maintaining healthy boundaries!',
                    'At Risk': 'Some patterns suggest your social media use may be impacting your wellbeing. Review your personalized tips below.',
                    'Burnout': 'Multiple indicators suggest significant digital wellness concerns. Please consider the resources and professional support options.'
                }
                
                st.markdown(f"""
                <div style='text-align:center; margin:20px 0;'>
                    <span class='{badge_class}'>{risk_level}</span>
                    <p style='color:#8b949e; margin-top:14px; font-size:0.95rem;'>{interpretations[risk_level]}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # ============================================================
                # PERSONAL HISTORY TRACKING (localStorage)
                # ============================================================
                # Save current score to browser's localStorage
                from datetime import datetime
                import json
                
                current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
                
                st.markdown(f"""
                <script>
                    (function() {{
                        try {{
                            // Get existing history
                            let history = JSON.parse(localStorage.getItem('zenfeed_history') || '[]');
                            
                            // Add new entry
                            history.push({{
                                date: '{current_timestamp}',
                                score: {wellness_score},
                                risk: '{risk_level}'
                            }});
                            
                            // Keep only last 10 entries
                            if (history.length > 10) {{
                                history = history.slice(-10);
                            }}
                            
                            // Save back to localStorage
                            localStorage.setItem('zenfeed_history', JSON.stringify(history));
                        }} catch(e) {{
                            console.log('LocalStorage not available');
                        }}
                    }})();
                </script>
                """, unsafe_allow_html=True)
                
                # Display "Your Progress Over Time" if there's history
                st.markdown("<br><br>", unsafe_allow_html=True)
                st.markdown("""
                <div style='background:#0b1422; border:1px solid #30363d; border-radius:12px; padding:20px; text-align:center;'>
                    <p style='color:#5eead4; font-size:1.1rem; font-weight:600; margin-bottom:8px;'>📈 Your Progress is Being Tracked</p>
                    <p style='color:#8b949e; font-size:0.9rem;'>
                        Your ZenScore history is saved locally in your browser. 
                        Come back regularly to see how you're doing over time! 
                        <br><span style='font-size:0.8rem;'>(Data stays private on your device only)</span>
                    </p>
                </div>
                """, unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                
                # ============================================================
                # BLOCK 2 — COMPOSITE SCORE CARDS
                # ============================================================
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("<div class='section-label'>COMPOSITE SCORES</div>", unsafe_allow_html=True)
                
                col1, col2, col3, col4 = st.columns(4)
                
                composite_scores = [
                    ('🎯 ADHD', result['adhd_score'], 'adhd'),
                    ('😰 Anxiety', result['anxiety_score'], 'anxiety'),
                    ('🪞 Self-Esteem', result['self_esteem_score'], 'self_esteem'),
                    ('😔 Depression', result['depression_score'], 'depression')
                ]
                
                for col, (label, score, key) in zip([col1, col2, col3, col4], composite_scores):
                    if score < 2.0:
                        border_color = '#5eead4'
                        score_color = '#5eead4'
                    elif score < 3.5:
                        border_color = '#f59e0b'
                        score_color = '#f59e0b'
                    else:
                        border_color = '#ef4444'
                        score_color = '#ef4444'
                    
                    with col:
                        st.markdown(f"""
                        <div class='zen-kpi' style='border-top-color:{border_color};'>
                            <div class='zen-kpi-value' style='color:{score_color};'>{score:.1f}</div>
                            <div class='zen-kpi-label'>{label}</div>
                        </div>
                        """, unsafe_allow_html=True)
                
                # ============================================================
                # BLOCK 3 — SHAP CHART
                # ============================================================
                st.markdown("<br><br>", unsafe_allow_html=True)
                st.markdown("<h3>🔍 What's Driving Your ZenScore</h3>", unsafe_allow_html=True)
                st.caption("Powered by SHAP explainability")
                
                shap_values = result['shap_values']
                shap_df = pd.DataFrame({
                    'feature': list(shap_values.keys()),
                    'impact': list(shap_values.values())
                }).sort_values('impact', key=abs, ascending=True)
                
                colors_shap = ['#ef4444' if x > 0 else '#5eead4' for x in shap_df['impact']]
                
                fig_shap = go.Figure(go.Bar(
                    x=shap_df['impact'],
                    y=shap_df['feature'],
                    orientation='h',
                    marker=dict(color=colors_shap),
                    text=[f"{x:+.3f}" for x in shap_df['impact']],
                    textposition='outside'
                ))
                
                fig_shap.update_layout(
                    title="Feature Impact on Risk Prediction",
                    xaxis_title="SHAP Value (Red = Risk, Teal = Protective)",
                    yaxis_title="",
                    height=400,
                    showlegend=False,
                    margin=dict(l=20, r=20, t=60, b=60),
                    **PLOTLY_THEME
                )
                
                st.plotly_chart(fig_shap, use_container_width=True)
                
                # ============================================================
                # BLOCK 4 — PERSONALIZED TIPS
                # ============================================================
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("<h3>💡 Your Personalized ZenPlan</h3>", unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                
                for tip in result['personalized_tips']:
                    st.markdown(f"""
                    <div class='tip-card'>
                        <div style='font-size:1.5rem; margin-bottom:8px;'>{tip['emoji']}</div>
                        <h4 style='color:#5eead4; margin:0 0 8px 0; font-size:1.1rem;'>{tip['title']}</h4>
                        <p style='color:#8b949e; margin:0; line-height:1.6;'>{tip['description']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # ============================================================
                # BLOCK 5 — PDF DOWNLOAD
                # ============================================================
                st.markdown("<br><br>", unsafe_allow_html=True)
                
                try:
                    # Generate PDF
                    buffer = BytesIO()
                    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
                    story = []
                    styles = getSampleStyleSheet()
                    
                    # Custom styles
                    title_style = ParagraphStyle(
                        'CustomTitle',
                        parent=styles['Heading1'],
                        fontSize=18,
                        textColor=colors.HexColor('#5eead4'),
                        spaceAfter=6,
                        alignment=TA_CENTER,
                        fontName='Helvetica-Bold'
                    )
                    
                    normal_style = ParagraphStyle(
                        'CustomNormal',
                        parent=styles['Normal'],
                        fontSize=10,
                        textColor=colors.black,
                        spaceAfter=12
                    )
                    
                    # Header
                    story.append(Paragraph("🌿 ZenFeed — Mental Wellness Report", title_style))
                    story.append(Spacer(1, 0.1*inch))
                    story.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", 
                                          ParagraphStyle('date', parent=normal_style, alignment=TA_CENTER, fontSize=9, textColor=colors.grey)))
                    story.append(Spacer(1, 0.3*inch))
                    
                    # Wellness Score — use a table so nothing overlaps
                    score_color = colors.HexColor(gauge_color)
                    risk_color_map = {'Healthy': '#0d9488', 'At Risk': '#d97706', 'Burnout': '#dc2626'}
                    risk_hex = risk_color_map.get(risk_level, '#dc2626')

                    score_block = Table(
                        [[Paragraph(f"<b>{wellness_score:.0f}</b>",
                                    ParagraphStyle('score', parent=styles['Normal'],
                                                   fontSize=52, textColor=score_color,
                                                   alignment=TA_CENTER, fontName='Helvetica-Bold',
                                                   leading=58))],
                         [Paragraph(f"<b>{risk_level}</b>",
                                    ParagraphStyle('risk', parent=styles['Normal'],
                                                   fontSize=16, textColor=colors.HexColor(risk_hex),
                                                   alignment=TA_CENTER, fontName='Helvetica-Bold',
                                                   spaceAfter=6))],
                         [Paragraph(interpretations[risk_level],
                                    ParagraphStyle('interp', parent=styles['Normal'],
                                                   fontSize=10, textColor=colors.HexColor('#555555'),
                                                   alignment=TA_CENTER, leading=14))]],
                        colWidths=[6*inch]
                    )
                    score_block.setStyle(TableStyle([
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('TOPPADDING', (0, 0), (-1, -1), 4),
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                        ('LINEBELOW', (0, 2), (-1, 2), 0.5, colors.HexColor('#dddddd')),
                    ]))
                    story.append(score_block)
                    story.append(Spacer(1, 0.3*inch))
                    
                    # Composite Scores Table
                    story.append(Paragraph("<b>Composite Scores</b>", ParagraphStyle('subtitle', parent=styles['Heading2'], fontSize=14, textColor=colors.HexColor('#5eead4'))))
                    story.append(Spacer(1, 0.1*inch))
                    
                    score_meanings = {
                        'adhd': 'Focus & Attention',
                        'anxiety': 'Stress & Worry',
                        'self_esteem': 'Self-Worth & Comparison',
                        'depression': 'Mood & Interest'
                    }
                    
                    table_data = [['Domain', 'Score', 'Level', 'Meaning']]
                    for label, score, key in composite_scores:
                        level = 'Low' if score < 2.0 else 'Moderate' if score < 3.5 else 'High'
                        table_data.append([label, f"{score:.1f}/5.0", level, score_meanings.get(key, '')])
                    
                    table = Table(table_data, colWidths=[1.5*inch, 1*inch, 1*inch, 2.5*inch])
                    table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#5eead4')),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, 0), 10),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                        ('FONTSIZE', (0, 1), (-1, -1), 9),
                        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
                    ]))
                    story.append(table)
                    story.append(Spacer(1, 0.3*inch))
                    
                    # Top Risk Factors
                    story.append(Paragraph("<b>Top Risk Factors</b>", ParagraphStyle('subtitle2', parent=styles['Heading2'], fontSize=14, textColor=colors.HexColor('#5eead4'))))
                    story.append(Spacer(1, 0.1*inch))
                    top_factors = sorted(shap_values.items(), key=lambda x: abs(x[1]), reverse=True)[:3]
                    for i, (feat, val) in enumerate(top_factors, 1):
                        story.append(Paragraph(f"{i}. <b>{feat.replace('_', ' ').title()}</b> (Impact: {val:+.3f})", normal_style))
                    story.append(Spacer(1, 0.3*inch))
                    
                    # ZenPlan Tips
                    story.append(Paragraph("<b>Your ZenPlan</b>", ParagraphStyle('subtitle3', parent=styles['Heading2'], fontSize=14, textColor=colors.HexColor('#5eead4'))))
                    story.append(Spacer(1, 0.1*inch))
                    for i, tip in enumerate(result['personalized_tips'], 1):
                        story.append(Paragraph(f"<b>{i}. {tip['title']}</b>", normal_style))
                        story.append(Paragraph(tip['description'], ParagraphStyle('tipdesc', parent=normal_style, fontSize=9, leftIndent=15)))
                        story.append(Spacer(1, 0.15*inch))
                    
                    # Support Resources
                    story.append(Spacer(1, 0.2*inch))
                    story.append(Paragraph("<b>Need Support?</b>", ParagraphStyle('support', parent=styles['Heading2'], fontSize=12, textColor=colors.HexColor('#5eead4'))))
                    story.append(Paragraph("🇮🇳 <b>iCall (TISS Mumbai):</b> 9152987821 (Mon-Sat, 8am-10pm)", normal_style))
                    story.append(Paragraph("🇮🇳 <b>Vandrevala Foundation:</b> 1860-2662-345 (24/7, Multilingual)", normal_style))
                    
                    # Footer
                    story.append(Spacer(1, 0.4*inch))
                    footer_style = ParagraphStyle('footer', parent=normal_style, fontSize=8, textColor=colors.grey, alignment=TA_CENTER)
                    story.append(Paragraph("⚠️ This report is an AI-generated screening tool, not a clinical diagnosis.", footer_style))
                    story.append(Paragraph("ZenFeed does not replace professional mental health care. Consult a licensed professional for personalized advice.", footer_style))
                    
                    # Build PDF
                    doc.build(story)
                    buffer.seek(0)
                    pdf_bytes = buffer.getvalue()
                    
                    st.markdown("""
                    <style>
                    div[data-testid="stDownloadButton"] > button {
                        background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 60%, #3b82f6 100%) !important;
                        color: #ffffff !important;
                        border: none !important;
                        border-radius: 12px !important;
                        font-family: 'Poppins', sans-serif !important;
                        font-weight: 700 !important;
                        font-size: 1rem !important;
                        padding: 14px 32px !important;
                        letter-spacing: 0.3px !important;
                        box-shadow: 0 4px 28px rgba(37, 99, 235, 0.55), 0 0 50px rgba(59, 130, 246, 0.25) !important;
                        transition: all 0.3s ease !important;
                        text-shadow: 0 1px 3px rgba(0,0,0,0.2) !important;
                    }
                    div[data-testid="stDownloadButton"] > button:hover {
                        transform: translateY(-2px) !important;
                        box-shadow: 0 8px 40px rgba(37, 99, 235, 0.7), 0 0 70px rgba(59, 130, 246, 0.4) !important;
                    }
                    </style>
                    """, unsafe_allow_html=True)
                    st.download_button(
                        label="📥 Download Your Report",
                        data=pdf_bytes,
                        file_name=f"ZenReport_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
                    
                except Exception as pdf_error:
                    st.error(f"PDF generation failed. Please try again. ({str(pdf_error)})")
                
                # ============================================================
                # DISCLAIMER
                # ============================================================
                st.markdown("""
                <div class='disclaimer'>
                    ⚠️ This result is an AI estimate — not a clinical diagnosis. See our Resources page if you need support.
                </div>
                """, unsafe_allow_html=True)
                
            else:
                error_data = response.json()
                st.error(f"❌ Prediction failed: {error_data.get('error', 'Unknown error')}")
        
        except requests.exceptions.Timeout:
            st.error("❌ Request timed out. Please check if the API server is running and try again.")
        except requests.exceptions.ConnectionError:
            st.error("❌ Cannot connect to API. Please ensure the Flask backend is running at " + API_URL)
        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")

# Bottom disclaimer (always shown)
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div class='disclaimer'>
    ⚠️ <b>Important:</b> ZenFeed is a screening tool for awareness, not a diagnostic instrument.
    Results are based on machine learning patterns and should not replace consultation with a licensed mental health professional.
    If you're experiencing distress, please visit our <b>Resources</b> page for helplines and support options.
</div>
""", unsafe_allow_html=True)
