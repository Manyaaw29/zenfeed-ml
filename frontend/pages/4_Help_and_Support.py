"""
🌿 ZenFeed — Mental Wellness Resources
You're not alone. Help is always available.
"""

import streamlit as st
import requests
import os

# ============================================================================
# PAGE CONFIG
# ============================================================================
st.set_page_config(
    page_title="ZenFeed · Resources",
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
  font-size: 1.1rem;
  font-weight: 700;
  letter-spacing: 0.3px;
  color: #93c5fd;
  margin-bottom: 12px;
  display: block;
}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SIDEBAR
# ============================================================================
PAGE_DESCRIPTION = "💚 You're not alone. Help is always available."

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
st.markdown("<h1>💚 Help & Support</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#8b949e;font-size:1rem;'>Everything you need to reclaim your mental wellness — fast.</p>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# ============================================================================
# SECTION 1 — BURNOUT SNAPSHOT (Stat tiles)
# ============================================================================
st.markdown("<div class='section-label'>📱 Social Media Burnout — At a Glance</div>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
stats = [
    ("68%", "report anxiety after scrolling"),
    ("2.4×", "higher depression risk (4+ hrs/day)"),
    ("1 in 3", "teens feel worse after social media"),
    ("40 min", "avg. daily time lost to mindless scroll"),
]
for col, (val, label) in zip([col1, col2, col3, col4], stats):
    with col:
        st.markdown(f"""
        <div class='zen-kpi'>
            <div class='zen-kpi-value'>{val}</div>
            <div class='zen-kpi-label'>{label}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================================
# SECTION 2 — INTERACTIVE WARNING SIGNS CHECKLIST
# ============================================================================
st.markdown("<div class='section-label'>🚨 Check Your Warning Signs</div>", unsafe_allow_html=True)
st.markdown("<p style='color:#8b949e;font-size:0.85rem;margin-bottom:14px;'>Tick any that apply to you right now.</p>", unsafe_allow_html=True)

warning_signs = [
    "😰  Anxious or irritable when I can't check my phone",
    "📉  I compare myself negatively to people online",
    "😔  Social media leaves me feeling worse than before",
    "🌀  I scroll mindlessly for long periods without noticing",
    "😴  Trouble sleeping due to screen use",
    "❤️  My self-worth depends on likes & comments",
    "🎯  Lost interest in hobbies I used to enjoy",
    "🔋  Exhausted but still can't stop scrolling",
]

col1, col2 = st.columns(2)
with col1:
    sign1 = st.checkbox(warning_signs[0], key='ws1')
    sign2 = st.checkbox(warning_signs[1], key='ws2')
    sign3 = st.checkbox(warning_signs[2], key='ws3')
    sign4 = st.checkbox(warning_signs[3], key='ws4')
with col2:
    sign5 = st.checkbox(warning_signs[4], key='ws5')
    sign6 = st.checkbox(warning_signs[5], key='ws6')
    sign7 = st.checkbox(warning_signs[6], key='ws7')
    sign8 = st.checkbox(warning_signs[7], key='ws8')

checked_count = sum([sign1, sign2, sign3, sign4, sign5, sign6, sign7, sign8])
total = 8

# Progress bar + dynamic message
st.markdown("<br>", unsafe_allow_html=True)
st.progress(checked_count / total, text=f"{checked_count} / {total} signs identified")

if checked_count == 0:
    st.success("✅ No warning signs. Great — keep your digital habits healthy!")
elif checked_count <= 2:
    st.info(f"🟡 Early signs. Stay mindful. A digital detox could help.")
elif checked_count <= 5:
    st.warning(f"🟠 Moderate burnout signs. Try the detox tips below.")
else:
    st.error(f"🔴 High burnout risk. Please reach out to someone — helplines below.")

st.markdown("<br><br>", unsafe_allow_html=True)

# ============================================================================
# SECTION 3 — DIGITAL DETOX TIPS (Expandable)
# ============================================================================
st.markdown("<div class='section-label'>🌿 Digital Detox Tips</div>", unsafe_allow_html=True)
st.markdown("<p style='color:#8b949e;font-size:0.85rem;margin-bottom:14px;'>Click any tip to expand.</p>", unsafe_allow_html=True)

tips = [
    ("🌙  Screen Curfew", "No screens 1 hr before bed.", "Blue light suppresses melatonin. Set a bedtime mode or use a physical alarm. Your brain needs darkness — not an endless feed."),
    ("📵  Notification Audit", "Turn off non-essential pings.", "Every alert is a dopamine hit rewiring your focus. Keep only calls & family texts. Check social media on your schedule, not the algorithm's."),
    ("🚶  One Offline Hour", "60 mins screen-free, every day.", "Walk, cook, sketch, call a friend. Real-world sensory input restores what scrolling drains. Even 30 mins makes a measurable difference."),
    ("🎨  Rediscover a Hobby", "Do something that doesn't need likes.", "Gardening, journaling, baking, puzzles — anything that gives you a sense of accomplishment without waiting for validation."),
    ("📋  Intentional Scrolling", "Ask 'why am I here?' before opening an app.", "Set a 10-minute timer. Find what you came for, then leave. You're the user, not the product."),
]

for title, subtitle, detail in tips:
    with st.expander(f"**{title}** — *{subtitle}*"):
        st.markdown(f"<p style='color:#c9d1d9;font-size:0.92rem;line-height:1.75;margin:0;'>{detail}</p>", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# ============================================================================
# SECTION 4 — WHEN TO SEEK HELP (Quick scan)
# ============================================================================
st.markdown("<div class='section-label'>🆘 When to Seek Professional Help</div>", unsafe_allow_html=True)
st.markdown("""
<div class='zen-card' style='border-left:4px solid #f59e0b; padding:20px 24px;'>
    <p style='color:#f59e0b; font-weight:600; font-size:0.95rem; margin:0 0 12px 0;'>Reach out immediately if you experience any of these:</p>
    <ul style='color:#c9d1d9; font-size:0.92rem; line-height:2; margin:0; padding-left:20px;'>
        <li>Persistent hopelessness or emptiness lasting >2 weeks</li>
        <li>Anxiety that stops you from working, studying, or sleeping</li>
        <li>Thoughts of self-harm or harming others</li>
        <li>Complete withdrawal from friends and real life</li>
        <li>Inability to stop compulsive phone use despite wanting to</li>
    </ul>
    <p style='color:#8b949e; font-size:0.82rem; margin:14px 0 0 0;'>There's no shame in asking for help. It's the smartest thing you can do. 💚</p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# ============================================================================
# SECTION 5 — 🇮🇳 INDIAN HELPLINES
# ============================================================================
st.markdown("<div class='section-label'>🇮🇳 Indian Mental Health Helplines</div>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

indian_lines = [
    ("iCall — TISS Mumbai", "9152987821", "Mon–Sat · 8 AM–10 PM", "#5eead4"),
    ("Vandrevala Foundation", "1860-2662-345", "24/7 · Multilingual", "#93c5fd"),
    ("Mann Talks", "8686139139", "Young Adults 18–35", "#c4b5fd"),
    ("NIMHANS", "080-46110007", "Mon–Fri · Office Hours", "#f59e0b"),
]

cols = st.columns(4)
for col, (name, number, hours, color) in zip(cols, indian_lines):
    with col:
        st.markdown(f"""
        <div class='zen-card' style='border-top:3px solid {color}; text-align:center; padding:18px 14px;'>
            <div style='font-size:0.8rem; color:#8b949e; margin-bottom:6px;'>{name}</div>
            <div style='font-size:1.15rem; font-weight:700; color:{color}; margin-bottom:6px;'>📞 {number}</div>
            <div style='font-size:0.75rem; color:#8b949e;'>{hours}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# ============================================================================
# SECTION 6 — 🌍 INTERNATIONAL
# ============================================================================
st.markdown("<div class='section-label'>🌍 International Helplines</div>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

intl_lines = [
    ("🇺🇸 USA", "Crisis Lifeline", "Call / Text 988", "#5eead4"),
    ("🇬🇧 UK", "Samaritans", "116 123 · 24/7 Free", "#93c5fd"),
    ("🇦🇺 AUS", "Beyond Blue", "1300 22 4636", "#c4b5fd"),
]
cols = st.columns(3)
for col, (flag, name, contact, color) in zip(cols, intl_lines):
    with col:
        st.markdown(f"""
        <div class='zen-card' style='border-top:3px solid {color}; text-align:center; padding:18px 14px;'>
            <div style='font-size:1.3rem; margin-bottom:4px;'>{flag}</div>
            <div style='font-size:0.85rem; font-weight:600; color:#e6edf3; margin-bottom:4px;'>{name}</div>
            <div style='font-size:0.85rem; color:{color}; font-weight:600;'>{contact}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# ============================================================================
# SECTION 7 — RECOMMENDED APPS
# ============================================================================
st.markdown("<div class='section-label'>📱 Recommended Wellness Apps</div>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

apps = [
    ("🟢 Headspace", "Guided meditation & sleep sounds.", "#5eead4", "Beginner-friendly mindfulness."),
    ("🔵 Calm", "Sleep stories & breathing programs.", "#93c5fd", "Best for anxiety & insomnia."),
    ("🤖 Wysa", "AI chatbot with CBT techniques.", "#c4b5fd", "Free, anonymous, 24/7."),
]
cols = st.columns(3)
for col, (name, desc, color, tag) in zip(cols, apps):
    with col:
        st.markdown(f"""
        <div class='zen-card' style='border-left:4px solid {color}; padding:16px 18px;'>
            <div style='font-size:1rem; font-weight:700; color:{color}; margin-bottom:6px;'>{name}</div>
            <div style='font-size:0.88rem; color:#c9d1d9; margin-bottom:8px;'>{desc}</div>
            <span style='font-size:0.75rem; background:rgba(255,255,255,0.06); color:#8b949e; padding:3px 10px; border-radius:20px;'>{tag}</span>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================================
# DISCLAIMER
# ============================================================================
st.markdown("""
<div class='disclaimer'>
    🌿 <b>Disclaimer:</b> ZenFeed is not a substitute for professional mental health care.
    All information is for general awareness only. If you are in immediate crisis, call emergency services or go to the nearest ER.
</div>
""", unsafe_allow_html=True)
