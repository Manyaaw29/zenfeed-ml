# 🌿 ZenFeed — Social Media Mental Wellness Analyzer

> **A mental health screening tool that analyzes social media consumption patterns and predicts digital wellness risk using ensemble machine learning.**

ZenFeed lets users complete a 2-minute anonymous assessment about their social media habits and emotional state. Three trained ML models analyze 9 behavioral and demographic features to generate a personalized **ZenScore (0–100)**, classify wellness risk (_Healthy / At Risk / Burnout_), surface SHAP-based top risk factors, and deliver a downloadable PDF wellness report — all in real time.

---

## 🔗 Live Demo

> [**https://zenfeed-ml-kzgcebsh6wrmt6t6thmgop.streamlit.app/**](https://zenfeed-ml-kzgcebsh6wrmt6t6thmgop.streamlit.app/)

---

## ✨ Features

- 🧠 **Multi-model ML prediction** — Logistic Regression, Random Forest, XGBoost trained on real survey data
- 📊 **Composite domain scoring** — ADHD tendency, anxiety signals, self-esteem impact, depression indicators
- 🔍 **SHAP explainability** — top 3 personalized risk factors surfaced per user
- 📄 **PDF report generation** — downloadable ZenReport with score, breakdown, and ZenPlan tips
- 🚨 **Crisis detection** — automatic mental health helpline banner for high-risk results
- 📈 **Community dashboard** — anonymized population-level insights with interactive Plotly charts
- 💡 **Digital Detox module** — interactive warning signs checklist + expandable tip library
- 🔒 **Fully anonymous** — no login, no data stored client-side beyond session

---

## 🛠 Tech Stack

- **Frontend** — Streamlit 1.54, custom CSS (Poppins + Inter, dark navy theme)
- **Backend API** — Flask 3.0 (REST), Python 3.14
- **Database** — MongoDB Atlas (PyMongo 4.16)
- **ML / Data** — scikit-learn 1.8, XGBoost 3.2, SHAP, pandas, NumPy
- **Visualization** — Plotly 6.5, ReportLab 4.0 (PDF)
- **Dev Tools** — VS Code, PowerShell, Git

---

## 🤖 ML Models

### Training Data

- **Dataset:** `zenfeed.csv` — 481 survey records with 20 features across social media behavior, emotional health, and demographics
- **Source:** [Social Media and Mental Health — Kaggle](https://www.kaggle.com/datasets/souvikahmed071/social-media-and-mental-health)
- **Target variable:** 3-class wellness label — `Healthy`, `At Risk`, `Burnout`
- **Train/test split:** 80/20 stratified

### Models Trained

- **Logistic Regression** ✅ _(used for live predictions)_ — Accuracy: 100% · F1: 1.00 · ROC-AUC: 1.00
- **Random Forest** — Accuracy: ~97% · F1: ~0.97 · ROC-AUC: ~0.99
- **XGBoost** — Accuracy: ~96% · F1: ~0.96 · ROC-AUC: ~0.99

> Logistic Regression is used for live predictions (best generalization on this dataset).

### Feature Engineering

9 input features fed to the model after preprocessing:

- **`anxiety_score`** _(Highest importance)_ — Composite: restlessness + worry + sleep disruption
- **`adhd_score`** _(High)_ — Composite: purposeless use + distraction + concentration
- **`depression_score`** _(High)_ — Composite: mood + interest fluctuation + sleep issues
- **`self_esteem_score`** _(Moderate)_ — Comparison frequency + post-comparison feelings + validation seeking
- **`gender`** _(Low)_ — Encoded demographic
- **`age`** _(Low)_ — Numeric
- **`relationship_status`** _(Low)_ — Encoded categorical
- **`social_media_hours`** _(Low)_ — Ordinal-encoded daily usage
- **`occupation`** _(Low)_ — Encoded categorical

Composite domain scores are computed from raw slider inputs (1–5 scale) as weighted averages before being passed to the model.

### Explainability

SHAP (SHapley Additive exPlanations) values are computed per prediction to identify the top 3 behavioral factors driving each individual's risk classification — shown directly on the results page.

---

## 📁 Project Structure

```
zenfeed/
├── frontend/
│   ├── app.py                    # Home / landing page
│   └── pages/
│       ├── 1_Take_Assessment.py  # Assessment form + ML results + PDF
│       ├── 2_Community.py        # Population-level dashboard
│       ├── 3_Data_Insights.py    # Deep data analysis & visualizations
│       └── 4_Help_and_Support.py # Resources, helplines, detox tips
├── backend/
│   └── app.py                    # Flask REST API (/predict, /health, /community)
├── model/
│   ├── train_model.py            # Model training & artifact export
│   ├── logistic_regression.pkl   # Trained model
│   ├── random_forest.pkl
│   ├── xgboost_model.pkl
│   ├── scaler.pkl                # StandardScaler
│   ├── label_encoders.pkl        # Categorical encoders
│   ├── feature_importance.json   # SHAP feature weights
│   └── metrics.json              # Evaluation metrics
├── .streamlit/
│   └── config.toml               # UI config (minimal toolbar)
├── zenfeed.csv                   # Training dataset
└── requirements.txt
```

---

## 🚀 Running Locally

**1. Install dependencies**

```bash
pip install -r requirements.txt
```

**2. Start Flask backend** (Terminal 1)

```bash
cd backend
python app.py
```

**3. Start Streamlit frontend** (Terminal 2)

```bash
streamlit run frontend/app.py
```

Open [http://localhost:8501](http://localhost:8501)

---

## 🚀 Deployment (Render + Streamlit Cloud)

### Step 1 — Deploy Flask backend on Render

1. Go to [render.com](https://render.com) → **New → Web Service**
2. Connect your GitHub repo
3. Render auto-detects `render.yaml` — confirm the settings:
   - **Build command:** `pip install -r requirements.txt`
   - **Start command:** `cd backend && gunicorn app:app`
   - **Runtime:** Python 3.10
4. Under **Environment Variables**, add:
   | Key | Value |
   |-----|-------|
   | `MONGO_URI` | your MongoDB Atlas connection string |
5. Click **Deploy** — Render will give you a URL like `https://zenfeed-api.onrender.com`

> ⚠️ Render free tier spins down after 15 min of inactivity — first request after idle takes ~30s to wake up.

---

### Step 2 — Deploy Streamlit frontend on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**
2. Connect your GitHub repo, set:
   - **Main file path:** `frontend/app.py`
   - **Branch:** `main`
3. Click **Advanced settings → Secrets** and add:
   ```toml
   API_URL = "https://zenfeed-api.onrender.com"
   ```
   _(replace with your actual Render URL from Step 1)_
4. Click **Deploy**

---

## ⚠️ Disclaimer

ZenFeed is a screening tool for awareness purposes only — not a clinical diagnostic instrument. Results are based on statistical patterns and should not replace consultation with a licensed mental health professional.

---

_Built with for mental wellness 🌿_
