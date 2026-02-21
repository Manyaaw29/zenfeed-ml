"""
🌿 ZenFeed — ML Training Pipeline
Trains Random Forest, Logistic Regression, and XGBoost models for mental wellness risk screening.
"""

import pandas as pd
import numpy as np
import json
import joblib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, roc_curve, auc
)
from imblearn.over_sampling import SMOTE
import xgboost as xgb
import shap
import warnings
warnings.filterwarnings('ignore')

print("🌿 ZenFeed ML Training Pipeline")
print("=" * 60)

# ============================================================================
# STEP 1: LOAD AND RENAME COLUMNS
# ============================================================================
print("\n[1/15] Loading dataset...")
df = pd.read_csv('../zenfeed.csv')
print(f"✓ Loaded {len(df)} rows × {len(df.columns)} columns")

# Get current column names for mapping
current_cols = df.columns.tolist()
print(f"\nOriginal columns: {current_cols[:5]}... ({len(current_cols)} total)")

# Create column mapping based on expected structure
# The dataset should have these columns in some order
column_mapping = {}
for col in current_cols:
    col_lower = col.lower().strip().replace(' ', '_')
    
    if 'what_is_your_age' in col_lower or col_lower.endswith('age?'):
        column_mapping[col] = 'age'
    elif 'gender' in col_lower:
        column_mapping[col] = 'gender'
    elif 'relationship' in col_lower:
        column_mapping[col] = 'relationship_status'
    elif 'occupation' in col_lower:
        column_mapping[col] = 'occupation'
    elif 'platform' in col_lower:
        column_mapping[col] = 'social_media_platforms'
    elif 'average_time' in col_lower or ('time' in col_lower and 'spend' in col_lower):
        column_mapping[col] = 'social_media_hours'
    elif 'purposeless' in col_lower or 'without_purpose' in col_lower or 'without_a_specific_purpose' in col_lower:
        column_mapping[col] = 'purposeless_use'
    elif 'distract' in col_lower and ('by' in col_lower or 'social' in col_lower or 'busy' in col_lower):
        column_mapping[col] = 'distracted_by_sm'
    elif 'restless' in col_lower:
        column_mapping[col] = 'restless_without_sm'
    elif 'easily' in col_lower and 'distract' in col_lower:
        column_mapping[col] = 'easily_distracted'
    elif 'bother' in col_lower and 'worr' in col_lower:
        column_mapping[col] = 'bothered_by_worries'
    elif 'difficult' in col_lower and 'concentrat' in col_lower:
        column_mapping[col] = 'difficulty_concentrating'
    elif 'compar' in col_lower and 'other' in col_lower:
        column_mapping[col] = 'compare_to_others'
    elif ('feel' in col_lower and 'comparison' in col_lower) or ('following' in col_lower and 'previous' in col_lower):
        column_mapping[col] = 'feelings_about_comparisons'
    elif 'validation' in col_lower or ('seek' in col_lower and 'features' in col_lower):
        column_mapping[col] = 'seek_validation'
    elif 'depress' in col_lower:
        column_mapping[col] = 'feel_depressed'
    elif 'interest' in col_lower and 'fluctuat' in col_lower:
        column_mapping[col] = 'interest_fluctuation'
    elif 'sleep' in col_lower:
        column_mapping[col] = 'sleep_issues'
    elif 'counselstatement' in col_lower or 'need' in col_lower:
        column_mapping[col] = 'needs_counselling'

df = df.rename(columns=column_mapping)
print(f"✓ Renamed columns to standardized format")

# ============================================================================
# STEP 2: HANDLE MISSING VALUES
# ============================================================================
print("\n[2/15] Handling missing values...")
print(f"Columns: {list(df.columns)}")
print(f"Column count: {len(df.columns)}, Unique: {len(set(df.columns))}")
initial_nulls = df.isnull().sum().sum()

# Fill all numeric columns with median
numeric_df = df.select_dtypes(include=[np.number])
for col in numeric_df.columns:
    df[col] = df[col].fillna(df[col].median())

# Fill all categorical columns with mode
object_df = df.select_dtypes(include=['object'])
for col in object_df.columns:
    mode_series = df[col].mode()
    fill_val = mode_series.iloc[0] if len(mode_series) > 0 else 'Unknown'
    df[col] = df[col].fillna(fill_val)

final_nulls = df.isnull().sum().sum()
print(f"✓ Filled {initial_nulls} null values → {final_nulls} remaining")

# ============================================================================
# STEP 3: ENGINEER COMPOSITE SCORES
# ============================================================================
print("\n[3/15] Engineering composite scores...")

df['adhd_score'] = df[['purposeless_use', 'distracted_by_sm', 'easily_distracted']].mean(axis=1)
df['anxiety_score'] = df[['restless_without_sm', 'bothered_by_worries']].mean(axis=1)
df['self_esteem_score'] = df[['compare_to_others', 'feelings_about_comparisons', 'seek_validation']].mean(axis=1)
df['depression_score'] = df[['feel_depressed', 'interest_fluctuation', 'sleep_issues']].mean(axis=1)

print("✓ Created 4 composite scores:")
print(f"  • ADHD Score:       {df['adhd_score'].mean():.2f} ± {df['adhd_score'].std():.2f}")
print(f"  • Anxiety Score:    {df['anxiety_score'].mean():.2f} ± {df['anxiety_score'].std():.2f}")
print(f"  • Self-Esteem Score: {df['self_esteem_score'].mean():.2f} ± {df['self_esteem_score'].std():.2f}")
print(f"  • Depression Score:  {df['depression_score'].mean():.2f} ± {df['depression_score'].std():.2f}")

# ============================================================================
# STEP 4: DERIVE WELLNESS SCORE AND RISK LEVEL
# ============================================================================
print("\n[4/15] Computing wellness scores and risk levels...")

composite_mean = df[['adhd_score', 'anxiety_score', 'self_esteem_score', 'depression_score']].mean(axis=1)
df['wellness_score'] = 100 - (composite_mean / 5 * 100)

# Define risk levels
def classify_risk(score):
    if score > 67:
        return 0  # Healthy
    elif score >= 34:
        return 1  # At Risk
    else:
        return 2  # Burnout

df['risk_level'] = df['wellness_score'].apply(classify_risk)

risk_dist = df['risk_level'].value_counts().sort_index()
print("✓ Risk level distribution:")
print(f"  • Class 0 (Healthy):  {risk_dist.get(0, 0)} samples ({risk_dist.get(0, 0)/len(df)*100:.1f}%)")
print(f"  • Class 1 (At Risk):  {risk_dist.get(1, 0)} samples ({risk_dist.get(1, 0)/len(df)*100:.1f}%)")
print(f"  • Class 2 (Burnout):  {risk_dist.get(2, 0)} samples ({risk_dist.get(2, 0)/len(df)*100:.1f}%)")

# ============================================================================
# STEP 5: PREPARE FEATURE SET
# ============================================================================
print("\n[5/15] Preparing feature set...")

# Drop raw 1-5 columns
raw_cols = ['purposeless_use', 'distracted_by_sm', 'restless_without_sm', 
            'easily_distracted', 'bothered_by_worries', 'difficulty_concentrating',
            'compare_to_others', 'feelings_about_comparisons', 'seek_validation',
            'feel_depressed', 'interest_fluctuation', 'sleep_issues', 'needs_counselling']

cols_to_drop = [col for col in raw_cols if col in df.columns]
cols_to_drop.extend(['social_media_platforms', 'wellness_score'])  # Drop these too

feature_cols = ['age', 'gender', 'relationship_status', 'occupation', 'social_media_hours',
                'adhd_score', 'anxiety_score', 'self_esteem_score', 'depression_score']

# Ensure all feature columns exist
feature_cols = [col for col in feature_cols if col in df.columns]

X = df[feature_cols].copy()
y = df['risk_level'].copy()

print(f"✓ Feature set: {len(feature_cols)} features × {len(X)} samples")
print(f"  Features: {', '.join(feature_cols)}")

# ============================================================================
# STEP 6: ENCODE CATEGORICAL VARIABLES
# ============================================================================
print("\n[6/15] Encoding categorical variables...")

encoders = {}
categorical_features = ['gender', 'relationship_status', 'occupation']

for col in categorical_features:
    if col in X.columns:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col].astype(str))
        encoders[col] = le
        print(f"✓ Encoded '{col}': {len(le.classes_)} classes")

# Save encoders
joblib.dump(encoders, 'label_encoders.pkl')
print("✓ Saved label encoders")

# Handle social_media_hours if it's categorical
if 'social_media_hours' in X.columns and X['social_media_hours'].dtype == 'object':
    # Map to numeric
    hours_mapping = {
        'Less than 1 hour': 0.5,
        'Less than an Hour': 0.5,
        'Between 1 and 2 hours': 1.5,
        'Between 2 and 3 hours': 2.5,
        'Between 3 and 4 hours': 3.5,
        'Between 4 and 5 hours': 4.5,
        'More than 5 hours': 6.0
    }
    X['social_media_hours'] = X['social_media_hours'].map(hours_mapping).fillna(3.0)
    print("✓ Converted social_media_hours to numeric")

# ============================================================================
# STEP 7: TRAIN-TEST SPLIT
# ============================================================================
print("\n[7/15] Splitting dataset...")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"✓ Train set: {len(X_train)} samples")
print(f"✓ Test set:  {len(X_test)} samples")

# ============================================================================
# STEP 8: APPLY SMOTE FOR CLASS BALANCE
# ============================================================================
print("\n[8/15] Applying SMOTE for class balance...")

smote = SMOTE(random_state=42)
X_train_balanced, y_train_balanced = smote.fit_resample(X_train, y_train)

print(f"✓ Before SMOTE: {len(X_train)} samples")
print(f"✓ After SMOTE:  {len(X_train_balanced)} samples")
train_dist = pd.Series(y_train_balanced).value_counts().sort_index()
for cls in range(3):
    print(f"  • Class {cls}: {train_dist.get(cls, 0)} samples")

# ============================================================================
# STEP 9: SCALE FEATURES
# ============================================================================
print("\n[9/15] Scaling features...")

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_balanced)
X_test_scaled = scaler.transform(X_test)

joblib.dump(scaler, 'scaler.pkl')
print("✓ Fitted and saved StandardScaler")

# ============================================================================
# STEP 10: TRAIN RANDOM FOREST
# ============================================================================
print("\n[10/15] Training Random Forest...")

rf_model = RandomForestClassifier(
    n_estimators=200,
    class_weight='balanced',
    random_state=42,
    n_jobs=-1,
    max_depth=15,
    min_samples_split=5,
    min_samples_leaf=2
)
rf_model.fit(X_train_scaled, y_train_balanced)
rf_pred = rf_model.predict(X_test_scaled)
rf_pred_proba = rf_model.predict_proba(X_test_scaled)

rf_metrics = {
    'accuracy': accuracy_score(y_test, rf_pred),
    'precision': precision_score(y_test, rf_pred, average='weighted', zero_division=0),
    'recall': recall_score(y_test, rf_pred, average='weighted', zero_division=0),
    'f1': f1_score(y_test, rf_pred, average='weighted', zero_division=0),
    'roc_auc': roc_auc_score(y_test, rf_pred_proba, multi_class='ovr', average='weighted')
}

joblib.dump(rf_model, 'random_forest.pkl')
print(f"✓ Random Forest trained — Accuracy: {rf_metrics['accuracy']:.3f}, F1: {rf_metrics['f1']:.3f}")

# ============================================================================
# STEP 11: TRAIN LOGISTIC REGRESSION
# ============================================================================
print("\n[11/15] Training Logistic Regression...")

lr_model = LogisticRegression(
    max_iter=1000,
    solver='lbfgs',
    random_state=42,
    class_weight='balanced'
)
lr_model.fit(X_train_scaled, y_train_balanced)
lr_pred = lr_model.predict(X_test_scaled)
lr_pred_proba = lr_model.predict_proba(X_test_scaled)

lr_metrics = {
    'accuracy': accuracy_score(y_test, lr_pred),
    'precision': precision_score(y_test, lr_pred, average='weighted', zero_division=0),
    'recall': recall_score(y_test, lr_pred, average='weighted', zero_division=0),
    'f1': f1_score(y_test, lr_pred, average='weighted', zero_division=0),
    'roc_auc': roc_auc_score(y_test, lr_pred_proba, multi_class='ovr', average='weighted')
}

joblib.dump(lr_model, 'logistic_regression.pkl')
print(f"✓ Logistic Regression trained — Accuracy: {lr_metrics['accuracy']:.3f}, F1: {lr_metrics['f1']:.3f}")

# ============================================================================
# STEP 12: TRAIN XGBOOST
# ============================================================================
print("\n[12/15] Training XGBoost...")

xgb_model = xgb.XGBClassifier(
    objective='multi:softprob',
    num_class=3,
    eval_metric='mlogloss',
    random_state=42,
    n_estimators=150,
    max_depth=6,
    learning_rate=0.1,
    subsample=0.8,
    colsample_bytree=0.8
)
xgb_model.fit(X_train_scaled, y_train_balanced)
xgb_pred = xgb_model.predict(X_test_scaled)
xgb_pred_proba = xgb_model.predict_proba(X_test_scaled)

xgb_metrics = {
    'accuracy': accuracy_score(y_test, xgb_pred),
    'precision': precision_score(y_test, xgb_pred, average='weighted', zero_division=0),
    'recall': recall_score(y_test, xgb_pred, average='weighted', zero_division=0),
    'f1': f1_score(y_test, xgb_pred, average='weighted', zero_division=0),
    'roc_auc': roc_auc_score(y_test, xgb_pred_proba, multi_class='ovr', average='weighted')
}

joblib.dump(xgb_model, 'xgboost_model.pkl')
print(f"✓ XGBoost trained — Accuracy: {xgb_metrics['accuracy']:.3f}, F1: {xgb_metrics['f1']:.3f}")

# ============================================================================
# STEP 13: SELECT BEST MODEL AND SAVE METRICS
# ============================================================================
print("\n[13/15] Selecting best model...")

all_models = {
    'Random Forest': rf_metrics,
    'Logistic Regression': lr_metrics,
    'XGBoost': xgb_metrics
}

# Select best based on F1 score
best_model_name = max(all_models, key=lambda k: all_models[k]['f1'])
best_metrics = all_models[best_model_name]
best_metrics['model_name'] = best_model_name

print(f"✓ Best model: {best_model_name} (F1: {best_metrics['f1']:.3f})")

# Save metrics
with open('metrics.json', 'w') as f:
    json.dump(best_metrics, f, indent=2)

# Save comparison
comparison = {
    name: {k: round(float(v), 4) if isinstance(v, (int, float)) else v for k, v in metrics.items()}
    for name, metrics in all_models.items()
}
with open('model_comparison.json', 'w') as f:
    json.dump(comparison, f, indent=2)

print("✓ Saved metrics.json and model_comparison.json")

# Save confusion matrix for best model
if best_model_name == 'Random Forest':
    best_pred = rf_pred
elif best_model_name == 'Logistic Regression':
    best_pred = lr_pred
else:
    best_pred = xgb_pred

cm = confusion_matrix(y_test, best_pred)
np.save('confusion_matrix.npy', cm)
print("✓ Saved confusion matrix")

# ============================================================================
# STEP 14: PLOT ROC CURVES
# ============================================================================
print("\n[14/15] Plotting ROC curves...")

plt.figure(figsize=(10, 8))
plt.style.use('dark_background')

colors = {'Random Forest': '#00d4aa', 'Logistic Regression': '#7c3aed', 'XGBoost': '#f59e0b'}
predictions = {
    'Random Forest': rf_pred_proba,
    'Logistic Regression': lr_pred_proba,
    'XGBoost': xgb_pred_proba
}

for model_name, pred_proba in predictions.items():
    fpr = dict()
    tpr = dict()
    roc_auc = dict()
    
    for i in range(3):
        y_test_binary = (y_test == i).astype(int)
        fpr[i], tpr[i], _ = roc_curve(y_test_binary, pred_proba[:, i])
        roc_auc[i] = auc(fpr[i], tpr[i])
    
    # Plot macro-average
    all_fpr = np.unique(np.concatenate([fpr[i] for i in range(3)]))
    mean_tpr = np.zeros_like(all_fpr)
    for i in range(3):
        mean_tpr += np.interp(all_fpr, fpr[i], tpr[i])
    mean_tpr /= 3
    
    mean_auc = auc(all_fpr, mean_tpr)
    plt.plot(all_fpr, mean_tpr, color=colors[model_name], lw=2.5,
             label=f'{model_name} (AUC = {mean_auc:.3f})', alpha=0.9)

plt.plot([0, 1], [0, 1], 'k--', lw=1.5, alpha=0.5, label='Chance')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate', fontsize=12, fontweight='bold')
plt.ylabel('True Positive Rate', fontsize=12, fontweight='bold')
plt.title('🌿 ZenFeed — ROC Curves (One-vs-Rest)', fontsize=14, fontweight='bold', color='#00d4aa')
plt.legend(loc="lower right", fontsize=10, framealpha=0.9)
plt.grid(alpha=0.2, linestyle='--')
plt.tight_layout()
plt.savefig('roc_curve.png', dpi=150, facecolor='#0d1117')
plt.close()

print("✓ Saved roc_curve.png")

# ============================================================================
# STEP 15: COMPUTE FEATURE IMPORTANCE WITH SHAP
# ============================================================================
print("\n[15/15] Computing SHAP feature importance...")

# Determine which model object to use
if best_model_name == 'Random Forest':
    best_model_obj = rf_model
elif best_model_name == 'Logistic Regression':
    best_model_obj = lr_model
else:
    best_model_obj = xgb_model

try:
    if best_model_name == 'Logistic Regression':
        # SHAP doesn't work well with LR for multiclass, use coefficients
        raise ValueError("Using coefficient-based importance for LR")
    
    # Sample data for SHAP (use subset for speed)
    sample_size = min(100, len(X_test_scaled))
    X_sample = X_test_scaled[:sample_size]
    
    explainer = shap.TreeExplainer(best_model_obj)
    shap_values = explainer.shap_values(X_sample)
    
    # Get mean absolute SHAP values across all classes
    if isinstance(shap_values, list):
        # For multiclass, average across classes
        mean_shap = np.mean([np.abs(sv).mean(axis=0) for sv in shap_values], axis=0)
    else:
        mean_shap = np.abs(shap_values).mean(axis=0)
    
    feature_importance = dict(zip(feature_cols, mean_shap))
    
except Exception as e:
    print(f"  SHAP failed ({str(e)}), using model feature importance...")
    if hasattr(best_model_obj, 'feature_importances_'):
        feature_importance = dict(zip(feature_cols, best_model_obj.feature_importances_))
    else:
        # For Logistic Regression, use coefficient magnitudes
        coef_importance = np.abs(best_model_obj.coef_).mean(axis=0)
        feature_importance = dict(zip(feature_cols, coef_importance))

# Sort and save top 10
feature_importance = dict(sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)[:10])
feature_importance = {k: float(v) for k, v in feature_importance.items()}

with open('feature_importance.json', 'w') as f:
    json.dump(feature_importance, f, indent=2)

print("✓ Saved feature_importance.json")
print("\nTop 5 risk factors:")
for i, (feat, imp) in enumerate(list(feature_importance.items())[:5], 1):
    print(f"  {i}. {feat}: {imp:.4f}")

# ============================================================================
# FINAL SUMMARY
# ============================================================================
print("\n" + "=" * 60)
print("🌿 TRAINING COMPLETE — MODEL PERFORMANCE SUMMARY")
print("=" * 60)

print(f"\n{'Model':<25} {'Accuracy':>10} {'Precision':>10} {'Recall':>10} {'F1':>10} {'AUC-ROC':>10}")
print("-" * 85)
for model_name, metrics in all_models.items():
    marker = "🏆" if model_name == best_model_name else "  "
    print(f"{marker} {model_name:<23} {metrics['accuracy']:>10.3f} {metrics['precision']:>10.3f} "
          f"{metrics['recall']:>10.3f} {metrics['f1']:>10.3f} {metrics['roc_auc']:>10.3f}")

print("\n" + "=" * 60)
print(f"✅ Best Model: {best_model_name}")
print(f"✅ All models saved as .pkl files")
print(f"✅ Ready for deployment to Flask API")
print("=" * 60)
