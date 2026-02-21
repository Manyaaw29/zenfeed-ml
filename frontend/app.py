"""
🌿 ZenFeed — Landing Page
Your mind deserves a healthy feed.
"""

import streamlit as st
import requests
import os

# ============================================================================
# PAGE CONFIG
# ============================================================================
st.set_page_config(
    page_title="🌿 ZenFeed",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

try:
    API_URL = st.secrets.get("API_URL", os.environ.get("API_URL", "http://localhost:5000"))
except Exception:
    API_URL = os.environ.get("API_URL", "http://localhost:5000")

# ============================================================================
# GLOBAL CSS + GRADIENT BACKGROUND
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
  color: #a0a8b0;
  margin-top: 6px;
  font-weight: 500;
  position: relative;
  z-index: 1;
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
  background: linear-gradient(135deg, #0d9488 0%, #2563eb 55%, #7c3aed 100%);
  background-size: 220% 220%;
  animation: buttonShift 4s ease infinite;
  color: #fff;
  border: none;
  border-radius: 14px;
  font-family: 'Poppins', sans-serif;
  font-weight: 700;
  font-size: 1.05rem;
  padding: 15px 36px;
  transition: all 0.35s ease;
  width: 100%;
  box-shadow: 0 4px 24px rgba(13, 148, 136, 0.45), 0 0 48px rgba(124, 58, 237, 0.2);
  position: relative;
  overflow: hidden;
  letter-spacing: 0.3px;
  text-shadow: 0 1px 3px rgba(0,0,0,0.3);
}
@keyframes buttonShift {
  0%   { background-position: 0% 50%; }
  50%  { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}
.stButton > button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -120%;
  width: 80%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.22), transparent);
  transition: left 0.6s ease;
}
.stButton > button:hover::before {
  left: 140%;
}
.stButton > button:hover {
  transform: translateY(-3px) scale(1.01);
  box-shadow: 0 10px 40px rgba(13, 148, 136, 0.55), 0 0 60px rgba(124, 58, 237, 0.35);
}

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
  font-size: 0.8rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 2px;
  background: linear-gradient(90deg, #5eead4 0%, #93c5fd 50%, #c4b5fd 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 18px;
  position: relative;
  padding-bottom: 12px;
}

.section-label::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 60px;
  height: 3px;
  background: linear-gradient(90deg, #5eead4 0%, #93c5fd 100%);
  border-radius: 3px;
}

/* Animated gradient orbs */
.hero-bg {
  position: relative;
}
.hero-bg::before {
  content: '';
  position: absolute;
  width: 600px; 
  height: 600px;
  background: radial-gradient(circle, rgba(94,234,212,0.04) 0%, transparent 70%);
  top: -100px; 
  left: -100px;
  border-radius: 50%;
  pointer-events: none;
}
.hero-bg::after {
  content: '';
  position: absolute;
  width: 400px; 
  height: 400px;
  background: radial-gradient(circle, rgba(196,181,253,0.04) 0%, transparent 70%);
  top: 100px; 
  right: -50px;
  border-radius: 50%;
  pointer-events: none;
}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SIDEBAR
# ============================================================================
PAGE_DESCRIPTION = "🏠 Welcome to ZenFeed — your mental wellness companion."

@st.cache_data(ttl=60)
def fetch_total_screenings(api_url):
    try:
        response = requests.get(f"{api_url}/stats", timeout=10)
        if response.status_code == 200:
            return response.json().get('total_predictions', 0)
    except:
        pass
    return 0

total_predictions = fetch_total_screenings(API_URL)

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
# SECTION 1 — HERO
# ============================================================================
st.markdown("""
<div class="hero-bg" style="
  text-align:center; 
  padding: 60px 20px 20px 20px;
  position: relative;
  overflow: hidden;
">
  <!-- Animated background glow -->
  <div style="
    position: absolute;
    top: -50%;
    left: 50%;
    transform: translateX(-50%);
    width: 500px;
    height: 500px;
    background: radial-gradient(circle, rgba(94, 234, 212, 0.08) 0%, rgba(147, 197, 253, 0.07) 50%, transparent 70%);
    animation: float 6s ease-in-out infinite;
    z-index: 0;
  "></div>
  
  <style>
    @keyframes float {
      0%, 100% { transform: translateX(-50%) translateY(0px); }
      50% { transform: translateX(-50%) translateY(-30px); }
    }
  </style>

  <!-- Illustration -->
  <div style="margin-bottom: 32px; position: relative; z-index: 1;">
    <img
      src="https://cdni.iconscout.com/illustration/premium/thumb/mental-health-illustration-svg-download-png-3016778.png"
      width="340"
      style="
        border-radius: 20px; 
        opacity: 0.95;
        box-shadow: 0 8px 32px rgba(94, 234, 212, 0.12), 0 0 60px rgba(59, 130, 246, 0.15);
      "
    />
  </div>

  <!-- App name -->
  <div style="
    font-family: 'Poppins', sans-serif;
    font-size: 3.8rem;
    font-weight: 900;
    background: linear-gradient(135deg, #5eead4 0%, #93c5fd 50%, #c4b5fd 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -2px;
    line-height: 1.1;
    margin-bottom: 16px;
    position: relative;
    z-index: 1;
  ">
    🌿 ZenFeed
  </div>

  <!-- Primary tagline -->
  <div style="
    font-family: 'Inter', sans-serif;
    font-size: 1.3rem;
    color: #e3e8ef;
    font-weight: 500;
    margin-bottom: 12px;
    max-width: 540px;
    margin-left: auto;
    margin-right: auto;
    line-height: 1.6;
    position: relative;
    z-index: 1;
  ">
    Understand how your feed is affecting your mind.
  </div>

  <!-- Secondary tagline -->
  <div style="
    font-size: 0.95rem;
    background: linear-gradient(90deg, #5eead4, #93c5fd, #c4b5fd);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 42px;
    font-weight: 600;
    position: relative;
    z-index: 1;
  ">
    Free · Anonymous · AI-powered · Takes 2 minutes
  </div>

</div>
""", unsafe_allow_html=True)

# CTA Button
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("Calculate your ZenScore 🌿", use_container_width=True):
        st.switch_page("pages/1_Take_Assessment.py")

# ============================================================================
# SECTION 2 — ANIMATED STATS ROW
# ============================================================================
st.markdown("<hr style='border:none;border-top:1px solid #21262d;margin:10px 0 32px 0;'>", unsafe_allow_html=True)

# Fetch real statistics from API (reuse cached value)
ml_models = 3
features_analyzed = 9

st.markdown(f"""
<div style="display:grid; grid-template-columns: repeat(4,1fr); gap:16px; padding: 0 20px;">

  <div class="zen-kpi">
    <div class="zen-kpi-value">{total_predictions}</div>
    <div class="zen-kpi-label">Live Screenings</div>
  </div>

  <div class="zen-kpi">
    <div class="zen-kpi-value">{ml_models}</div>
    <div class="zen-kpi-label">ML Models</div>
  </div>

  <div class="zen-kpi">
    <div class="zen-kpi-value">{features_analyzed}</div>
    <div class="zen-kpi-label">Features Analyzed</div>
  </div>

  <div class="zen-kpi">
    <div class="zen-kpi-value">100%</div>
    <div class="zen-kpi-label">Anonymous</div>
  </div>

</div>
""", unsafe_allow_html=True)

# ============================================================================
# SECTION 3 — HOW IT WORKS
# ============================================================================
st.markdown("<div style='margin-top:60px;'></div>", unsafe_allow_html=True)
st.markdown("<div class='section-label'>HOW IT WORKS</div>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="zen-card" style="border-top: 3px solid #5eead4;">
      <div style="
        width:40px; height:40px; border-radius:50%;
        background: linear-gradient(135deg,#0d9488,#0f766e);
        display:flex; align-items:center; justify-content:center;
        font-weight:800; font-size:1.1rem; color:#fff;
        margin-bottom:16px;
        box-shadow: 0 4px 15px rgba(94, 234, 212, 0.18);
      ">1</div>
      <div style="font-family:'Poppins',sans-serif; font-size:1.15rem; font-weight:700; margin:0 0 10px 0; color:#5eead4;">📋 Fill the Form</div>
      <p style="color:#a0a8b0; font-size:0.92rem; line-height:1.7; margin:0;">
        Answer 15 quick questions about your social media habits and how you feel.
        Takes under 2 minutes. No account needed.
      </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="zen-card" style="border-top: 3px solid #93c5fd;">
      <div style="
        width:40px; height:40px; border-radius:50%;
        background: linear-gradient(135deg,#2563eb,#1d4ed8);
        display:flex; align-items:center; justify-content:center;
        font-weight:800; font-size:1.1rem; color:#fff;
        margin-bottom:16px;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
      ">2</div>
      <div style="font-family:'Poppins',sans-serif; font-size:1.15rem; font-weight:700; margin:0 0 10px 0; color:#93c5fd;">🤖 AI Analyzes</div>
      <p style="color:#a0a8b0; font-size:0.92rem; line-height:1.7; margin:0;">
        Three ML models examine your digital behavior patterns in real time
        using advanced ensemble techniques.
      </p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="zen-card" style="border-top: 3px solid #c4b5fd;">
      <div style="
        width:40px; height:40px; border-radius:50%;
        background: linear-gradient(135deg,#6d28d9,#5b21b6);
        display:flex; align-items:center; justify-content:center;
        font-weight:800; font-size:1.1rem; color:#fff;
        margin-bottom:16px;
        box-shadow: 0 4px 15px rgba(196, 181, 253, 0.18);
      ">3</div>
      <div style="font-family:'Poppins',sans-serif; font-size:1.15rem; font-weight:700; margin:0 0 10px 0; color:#c4b5fd;">📊 Get Your ZenScore</div>
      <p style="color:#a0a8b0; font-size:0.92rem; line-height:1.7; margin:0;">
        See your 0–100 Wellness Score, top SHAP-powered risk factors, and 3
        personalized tips. Download a PDF report.
      </p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# SECTION 4 — WHAT WE MEASURE
# ============================================================================
st.markdown("<div style='margin-top:50px;'></div>", unsafe_allow_html=True)
st.markdown("<div class='section-label'>WHAT WE ANALYZE</div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="zen-card" style="border-left:5px solid #5eead4; background: linear-gradient(135deg, rgba(94, 234, 212, 0.04) 0%, rgba(8, 16, 30, 0.97) 100%);">
      <div style="font-family:'Poppins',sans-serif; font-size:1.3rem; font-weight:700; margin:0 0 10px 0; color:#5eead4;">🎯 ADHD Tendency</div>
      <p style="color:#a0a8b0; font-size:0.95rem; line-height:1.7; margin:0;">
        How often social media hijacks your focus and intent. Measures purposeless
        scrolling, distraction frequency, and loss of task awareness.
      </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="zen-card" style="border-left:5px solid #93c5fd; background: linear-gradient(135deg, rgba(147, 197, 253, 0.04) 0%, rgba(8, 16, 30, 0.97) 100%);">
      <div style="font-family:'Poppins',sans-serif; font-size:1.3rem; font-weight:700; margin:0 0 10px 0; color:#93c5fd;">🪞 Self-Esteem Impact</div>
      <p style="color:#a0a8b0; font-size:0.95rem; line-height:1.7; margin:0;">
        Comparison behavior and validation-seeking patterns. Tracks how your
        self-worth fluctuates based on social media feedback loops.
      </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="zen-card" style="border-left:5px solid #f59e0b; background: linear-gradient(135deg, rgba(245, 158, 11, 0.05) 0%, rgba(8, 16, 30, 0.97) 100%);">
      <div style="font-family:'Poppins',sans-serif; font-size:1.3rem; font-weight:700; margin:0 0 10px 0; color:#f59e0b;">😰 Anxiety Signals</div>
      <p style="color:#a0a8b0; font-size:0.95rem; line-height:1.7; margin:0;">
        Restlessness, worry levels, and need for constant connectivity. Identifies
        when social media becomes a source of stress rather than relaxation.
      </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="zen-card" style="border-left:5px solid #c4b5fd; background: linear-gradient(135deg, rgba(124, 58, 237, 0.05) 0%, rgba(8, 16, 30, 0.97) 100%);">
      <div style="font-family:'Poppins',sans-serif; font-size:1.3rem; font-weight:700; margin:0 0 10px 0; color:#c4b5fd;">😔 Depression Indicators</div>
      <p style="color:#a0a8b0; font-size:0.95rem; line-height:1.7; margin:0;">
        Mood dips, interest loss, and sleep disruption from screens. Measures
        how your emotional baseline shifts with digital consumption.
      </p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# SECTION 5 — DISCLAIMER
# ============================================================================
st.markdown("""
<div class="disclaimer" style="max-width:680px; margin: 32px auto 0 auto;">
  ⚠️ <strong>ZenFeed is a screening tool, not a clinical diagnosis.</strong>
  Results are based on statistical patterns from survey data and do not replace
  professional mental health advice. If you are struggling, please see our
  <strong>Resources</strong> page for helplines.
</div>
""", unsafe_allow_html=True)

# ============================================================================
# SECTION 6 — FOOTER
# ============================================================================
st.markdown("""
<div style="
  text-align:center;
  color:#484f58;
  font-size:0.78rem;
  margin-top:60px;
  padding: 24px 0;
  border-top: 1px solid #21262d;
">
  🌿 ZenFeed &nbsp;·&nbsp; AI-Powered Digital Wellness Assessment &nbsp;·&nbsp; For awareness purposes only — not a clinical diagnostic tool<br/>
  <span style="font-size:0.72rem; color:#363c45;">Powered by Logistic Regression &nbsp;·&nbsp; Random Forest &nbsp;·&nbsp; XGBoost</span><br/>
  © 2026 ZenFeed &nbsp;·&nbsp; Open Source &nbsp;·&nbsp; Privacy First &nbsp;·&nbsp; Designed &amp; Developed in India 🇮🇳
</div>
""", unsafe_allow_html=True)
