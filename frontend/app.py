"""
🌿 ZenFeed — Landing Page
Your mind deserves a healthy feed.
"""

import streamlit as st

# ============================================================================
# PAGE CONFIG
# ============================================================================
st.set_page_config(
    page_title="ZenFeed",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)


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

.block-container {
  background: transparent !important;
  background-color: transparent !important;
  border: none !important;
  box-shadow: none !important;
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
# NAVIGATION
# ============================================================================
pg = st.navigation([
    st.Page("pages/0_Home.py",            title="Home",            icon="🏠", default=True),
    st.Page("pages/1_Take_Assessment.py", title="Take Assessment", icon="📋"),
    st.Page("pages/2_Community.py",        title="Community",       icon="👥"),
    st.Page("pages/3_Data_Insights.py",    title="Data Insights",   icon="📊"),
    st.Page("pages/4_Help_and_Support.py", title="Help & Support",  icon="💚"),
])
pg.run()
