"""
🌿 ZenFeed — Model Comparison
Side-by-side comparison of all three ML models.
"""

import streamlit as st
import requests
import os
import plotly.graph_objects as go

# ============================================================================
# PAGE CONFIG
# ============================================================================
st.set_page_config(
    page_title="ZenFeed · Model Comparison",
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

.compare-table td, .compare-table th {
  padding: 10px 14px;
  border-bottom: 1px solid rgba(255,255,255,0.05);
  font-size: 0.87rem;
}
.compare-table th {
  color: #5eead4;
  font-weight: 600;
  font-family: 'Poppins', sans-serif;
  background: rgba(94,234,212,0.05);
}
.compare-table tr:hover { background: rgba(255,255,255,0.02); }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SIDEBAR
# ============================================================================
PAGE_DESCRIPTION = "⚖️ Side-by-side model comparison"

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
# FETCH MODEL DATA
# ============================================================================
models_data = None
try:
    r = requests.get(f"{API_URL}/models", timeout=8)
    if r.status_code == 200:
        models_data = r.json()
except Exception as e:
    st.warning(f"Could not reach the backend: {e}")

if models_data is None:
    st.error("Backend unavailable — please try again later.")
    st.stop()

model_dict = models_data.get("models", {})
active_model = models_data.get("active_model", "Logistic Regression")
selection_logic = models_data.get("selection_logic", "")

MODEL_COLORS = {
    "Logistic Regression": "#c4b5fd",
    "Random Forest":       "#5eead4",
    "XGBoost":             "#f59e0b",
}
MODEL_ICONS = {
    "Logistic Regression": "📐",
    "Random Forest":       "🌲",
    "XGBoost":             "⚡",
}

names  = list(model_dict.keys())
colors = [MODEL_COLORS.get(n, "#93c5fd") for n in names]

# ============================================================================
# PAGE HEADER
# ============================================================================
st.markdown("<h1>⚖️ Model Comparison</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='color:#8b949e;font-size:0.95rem;margin-top:-10px;margin-bottom:32px;'>"
    "All three models trained identically — same data, same split, same features. "
    "Differences reflect the algorithm's inductive bias, not data quality."
    "</p>",
    unsafe_allow_html=True
)

# ============================================================================
# SECTION 1 — GROUPED BAR CHART
# ============================================================================
st.markdown("### 📊 Performance Metrics — All Models, All Metrics")

metrics_keys  = ["accuracy", "precision", "recall", "f1", "roc_auc"]
metric_labels = ["Accuracy", "Precision", "Recall", "F1", "ROC-AUC"]

fig_grouped = go.Figure()
for name in names:
    meta = model_dict[name]
    y_vals = [meta.get(k, 0) for k in metrics_keys]
    fig_grouped.add_trace(go.Bar(
        name=f"{MODEL_ICONS.get(name,'')} {name}",
        x=metric_labels,
        y=y_vals,
        marker=dict(
            color=MODEL_COLORS.get(name, "#93c5fd"),
            opacity=0.85,
            line=dict(color='rgba(255,255,255,0.06)', width=1),
        ),
        text=[f"{v*100:.1f}%" if k != 'roc_auc' else f"{v:.3f}" for v, k in zip(y_vals, metrics_keys)],
        textposition='outside',
        textfont=dict(size=10, color='#8b949e'),
    ))

fig_grouped.update_layout(
    barmode='group',
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Inter', color='#e6edf3', size=12),
    margin=dict(l=10, r=10, t=20, b=10),
    height=340,
    yaxis=dict(
        range=[0.88, 1.06],
        gridcolor='rgba(255,255,255,0.05)',
        showgrid=True,
        zeroline=False,
        tickformat='.0%',
        tickfont=dict(color='#8b949e'),
    ),
    xaxis=dict(showgrid=False, tickfont=dict(color='#e6edf3', size=13)),
    legend=dict(
        font=dict(size=12, color='#e6edf3'),
        bgcolor='rgba(0,0,0,0)',
        orientation='h',
        yanchor='bottom', y=-0.28,
        xanchor='center', x=0.5,
    ),
    bargap=0.15,
    bargroupgap=0.05,
)
st.plotly_chart(fig_grouped, use_container_width=True)

# ============================================================================
# SECTION 2 — RADAR CHART
# ============================================================================
st.markdown("<hr style='border:none;border-top:1px solid #21262d;margin:32px 0;'>", unsafe_allow_html=True)
st.markdown("### 🕸️ Radar — All Metrics at Once")

radar_metrics = ["Accuracy", "Precision", "Recall", "F1", "ROC-AUC"]
fig_radar = go.Figure()

for name in names:
    meta = model_dict[name]
    vals_r = [
        meta.get("accuracy", 0),
        meta.get("precision", 0),
        meta.get("recall", 0),
        meta.get("f1", 0),
        meta.get("roc_auc", 0),
    ]
    fig_radar.add_trace(go.Scatterpolar(
        r=vals_r + [vals_r[0]],
        theta=radar_metrics + [radar_metrics[0]],
        fill='toself',
        name=f"{MODEL_ICONS.get(name,'')} {name}",
        line=dict(color=MODEL_COLORS.get(name, "#93c5fd"), width=2),
        fillcolor=MODEL_COLORS.get(name, "#93c5fd").replace(")", ", 0.08)").replace("rgb", "rgba") if "rgb" in MODEL_COLORS.get(name, "") else MODEL_COLORS.get(name, "#93c5fd") + "14",
        opacity=0.85,
    ))

fig_radar.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0.9, 1.01],
            gridcolor='rgba(255,255,255,0.08)',
            tickfont=dict(color='#8b949e', size=10),
            tickformat='.0%',
        ),
        angularaxis=dict(
            gridcolor='rgba(255,255,255,0.08)',
            tickfont=dict(color='#e6edf3', size=12),
        ),
        bgcolor='rgba(0,0,0,0)',
    ),
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Inter', color='#e6edf3'),
    legend=dict(
        font=dict(size=12, color='#e6edf3'),
        bgcolor='rgba(0,0,0,0)',
        orientation='h',
        yanchor='bottom',
        y=-0.15,
        x=0.5,
        xanchor='center',
    ),
    margin=dict(l=40, r=40, t=30, b=40),
    height=420,
)
st.plotly_chart(fig_radar, use_container_width=True)

# ============================================================================
# SECTION 3 — SUMMARY TABLE
# ============================================================================
st.markdown("<hr style='border:none;border-top:1px solid #21262d;margin:32px 0;'>", unsafe_allow_html=True)
st.markdown("### 📋 Quick Reference Table")

rows = []
for name, meta in model_dict.items():
    icon  = MODEL_ICONS.get(name, "•")
    rec   = "✅ Default" if meta.get("recommended") else ""
    rows.append({
        "Model": f"{icon} {name}",
        "Type": meta.get("type", ""),
        "Accuracy": f"{meta.get('accuracy',0)*100:.1f}%",
        "Precision": f"{meta.get('precision',0)*100:.1f}%",
        "Recall": f"{meta.get('recall',0)*100:.1f}%",
        "F1": f"{meta.get('f1',0)*100:.1f}%",
        "ROC-AUC": f"{meta.get('roc_auc',0):.3f}",
        "Status": rec,
    })

import pandas as pd
df = pd.DataFrame(rows)
st.dataframe(
    df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Model":    st.column_config.TextColumn("Model", width="medium"),
        "Type":     st.column_config.TextColumn("Type", width="medium"),
        "Accuracy": st.column_config.TextColumn("Accuracy", width="small"),
        "F1":       st.column_config.TextColumn("F1", width="small"),
        "ROC-AUC":  st.column_config.TextColumn("ROC-AUC", width="small"),
        "Status":   st.column_config.TextColumn("Status", width="small"),
    }
)

# ============================================================================
# SECTION 4 — VERDICT CARD
# ============================================================================
st.markdown("<hr style='border:none;border-top:1px solid #21262d;margin:32px 0;'>", unsafe_allow_html=True)
st.markdown("### 🏆 Verdict")

# Determine overall winner by F1
best_name = max(model_dict, key=lambda n: model_dict[n].get("f1", 0))
best_meta = model_dict[best_name]
best_icon = MODEL_ICONS.get(best_name, "🤖")
best_color = MODEL_COLORS.get(best_name, "#5eead4")

runner_ups = [n for n in names if n != best_name]
runner_str = " and ".join(runner_ups)

st.markdown(f"""
<div style="
  background: linear-gradient(135deg, rgba(94,234,212,0.06) 0%, rgba(99,102,241,0.06) 100%);
  border: 1px solid rgba(94,234,212,0.2);
  border-left: 5px solid {best_color};
  border-radius: 14px;
  padding: 22px 26px;
">
  <div style="display:flex;align-items:center;gap:12px;margin-bottom:12px;">
    <span style="font-size:2rem;">{best_icon}</span>
    <div>
      <p style="color:{best_color};font-size:1.1rem;font-weight:700;font-family:'Poppins',sans-serif;margin:0;">
        {best_name} wins
        <span style="background:linear-gradient(90deg,#14b8a6,#6366f1);color:#fff;font-size:0.7rem;
          padding:2px 10px;border-radius:999px;font-weight:700;margin-left:8px;vertical-align:middle;">DEFAULT</span>
      </p>
      <p style="color:#8b949e;font-size:0.8rem;margin:2px 0 0 0;">
        F1 = {best_meta.get('f1',0)*100:.1f}% &nbsp;·&nbsp;
        Accuracy = {best_meta.get('accuracy',0)*100:.1f}% &nbsp;·&nbsp;
        ROC-AUC = {best_meta.get('roc_auc',0):.3f}
      </p>
    </div>
  </div>
  <p style="color:#e6edf3;font-size:0.9rem;margin:0 0 6px 0;font-weight:500;">
    {best_name} achieves the highest weighted F1 across all three classes on this dataset, outperforming {runner_str}.
  </p>
  <p style="color:#8b949e;font-size:0.86rem;margin:0;line-height:1.6;">
    The composite features (anxiety/ADHD/depression/self-esteem scores) form linearly separable clusters,
    favouring a linear boundary. {runner_str.split(' and ')[0]} and tree-based models are more powerful in
    general but add unnecessary complexity here — their slightly lower scores reflect mild overfitting on
    the 481-record training set.
  </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown(f"""
<div style="
  background: rgba(8,16,30,0.6);
  border: 1px solid rgba(99,102,241,0.15);
  border-left: 4px solid #6366f1;
  border-radius: 12px;
  padding: 16px 20px;
">
  <p style="color:#c4b5fd;font-size:0.82rem;font-weight:600;margin:0 0 6px 0;">🧠 How the default is chosen automatically</p>
  <p style="color:#8b949e;font-size:0.82rem;margin:0;line-height:1.6;">{selection_logic}</p>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("""
<div style="
  text-align:center;
  color:#484f58;
  font-size:0.78rem;
  margin-top:60px;
  padding:24px 0;
  border-top:1px solid #21262d;
">
  🌿 ZenFeed &nbsp;·&nbsp; Model Comparison &nbsp;·&nbsp; For awareness purposes only — not a clinical diagnostic tool<br/>
  © 2026 ZenFeed &nbsp;·&nbsp; Open Source &nbsp;·&nbsp; Privacy First &nbsp;·&nbsp; Designed &amp; Developed in India 🇮🇳
</div>
""", unsafe_allow_html=True)
