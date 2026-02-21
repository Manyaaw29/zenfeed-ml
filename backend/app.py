"""
🌿 ZenFeed — Flask REST API
Production-grade backend for mental wellness risk screening.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
import json
import os
from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
import shap
import warnings
from dotenv import load_dotenv

warnings.filterwarnings('ignore')

# Load environment variables from .env file
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# ============================================================================
# LOAD MODELS AND RESOURCES AT STARTUP
# ============================================================================
print("🌿 ZenFeed API — Loading models...")

try:
    models = {
        "Random Forest": joblib.load("../model/random_forest.pkl"),
        "Logistic Regression": joblib.load("../model/logistic_regression.pkl"),
        "XGBoost": joblib.load("../model/xgboost_model.pkl")
    }
    scaler = joblib.load("../model/scaler.pkl")
    label_encoders = joblib.load("../model/label_encoders.pkl")
    
    with open("../model/feature_importance.json", "r") as f:
        feature_importance = json.load(f)
    
    with open("../model/metrics.json", "r") as f:
        metrics = json.load(f)
    
    print("✓ Models loaded successfully")
    print(f"✓ Available models: {list(models.keys())}")
    
except Exception as e:
    print(f"❌ Error loading models: {str(e)}")
    raise

# Feature columns (must match training order)
FEATURE_COLS = ['age', 'gender', 'relationship_status', 'occupation', 'social_media_hours',
                'adhd_score', 'anxiety_score', 'self_esteem_score', 'depression_score']

# ============================================================================
# MONGODB CONNECTION
# ============================================================================
MONGO_URI = os.environ.get("MONGO_URI")
mongo_client = None
db = None
predictions_collection = None

if MONGO_URI:
    try:
        mongo_client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        mongo_client.admin.command('ping')
        db = mongo_client['zenfeed']
        predictions_collection = db['predictions']
        print("✓ MongoDB connected")
    except (ConnectionFailure, ServerSelectionTimeoutError) as e:
        print(f"⚠ MongoDB connection failed: {str(e)}")
        print("  Using fallback JSON storage")
        mongo_client = None
else:
    print("⚠ MONGO_URI not set — using fallback JSON storage")

# Fallback JSON file
FALLBACK_FILE = "predictions_fallback.json"
if not os.path.exists(FALLBACK_FILE):
    with open(FALLBACK_FILE, 'w') as f:
        json.dump([], f)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def save_prediction_mongodb(data):
    """Save prediction to MongoDB, fallback to JSON."""
    try:
        if predictions_collection is not None:
            predictions_collection.insert_one(data)
            return True
        else:
            raise Exception("MongoDB not available")
    except Exception as e:
        # Fallback to JSON
        try:
            with open(FALLBACK_FILE, 'r') as f:
                records = json.load(f)
            records.append(data)
            with open(FALLBACK_FILE, 'w') as f:
                json.dump(records, f, indent=2)
            return True
        except Exception as json_error:
            print(f"❌ Failed to save to fallback: {str(json_error)}")
            return False

def get_predictions_from_storage():
    """Retrieve all predictions from MongoDB + fallback JSON."""
    all_predictions = []
    
    # Get from MongoDB
    if predictions_collection is not None:
        try:
            mongo_records = list(predictions_collection.find({}, {'_id': 0}))
            all_predictions.extend(mongo_records)
        except Exception as e:
            print(f"⚠ MongoDB read failed: {str(e)}")
    
    # Get from fallback JSON
    try:
        with open(FALLBACK_FILE, 'r') as f:
            json_records = json.load(f)
            all_predictions.extend(json_records)
    except Exception as e:
        print(f"⚠ Fallback JSON read failed: {str(e)}")
    
    # Deduplicate by timestamp
    seen = set()
    unique_predictions = []
    for pred in all_predictions:
        ts = pred.get('timestamp')
        if ts not in seen:
            seen.add(ts)
            unique_predictions.append(pred)
    
    return unique_predictions

def get_personalized_tips(composite_scores):
    """Generate 3 personalized tips based on highest composite score."""
    
    tip_library = {
        'adhd_score': [
            {
                'emoji': '🎯',
                'title': 'Practice Mindful Scrolling',
                'description': "Set a 15-min timer before opening any app. Ask: 'What am I here for?' This simple pause can break the autopilot habit."
            },
            {
                'emoji': '🔕',
                'title': 'Silence the Noise',
                'description': "Turn off all non-essential push notifications. Your brain needs space to think without constant digital interruptions."
            },
            {
                'emoji': '📵',
                'title': 'Phone-Free Focus Blocks',
                'description': "Pomodoro technique: 25 mins deep work with phone in another room, then 5-min break. Train your attention muscle."
            }
        ],
        'anxiety_score': [
            {
                'emoji': '🧘',
                'title': 'Schedule Your Scroll Time',
                'description': "Pick 2 fixed windows a day for social media (e.g., 12pm and 6pm). Outside those, close the apps. Structure reduces anxiety."
            },
            {
                'emoji': '📰',
                'title': 'News Detox for 7 Days',
                'description': "One trusted source, once a day. Doom-scrolling amplifies worry. Your anxiety might ease significantly with this boundary."
            },
            {
                'emoji': '💨',
                'title': 'Box Breathing Reset',
                'description': "Inhale 4s, hold 4s, exhale 4s, hold 4s. Do this before picking up your phone. It activates your calm-down system."
            }
        ],
        'self_esteem_score': [
            {
                'emoji': '🚫',
                'title': 'Curate Without Guilt',
                'description': "Unfollow any account that makes you feel worse. Your feed should inspire you, not drain your self-worth. It's okay to protect your peace."
            },
            {
                'emoji': '🪞',
                'title': 'Comparison Journal',
                'description': "When you compare yourself, write it down. Then ask: 'What do I actually know about their life?' Spotting the pattern weakens its grip."
            },
            {
                'emoji': '💛',
                'title': 'Gratitude Over Comparison',
                'description': "Write 3 specific things you appreciate about your own life each night. Training your brain to notice what's good in your reality, not theirs."
            }
        ],
        'depression_score': [
            {
                'emoji': '🌿',
                'title': 'One Offline Hour Daily',
                'description': "Replace one screen hour with something physical: walk, cook, sketch, or call a friend. Your brain craves real-world dopamine."
            },
            {
                'emoji': '😴',
                'title': 'The 9pm Screen Sunset',
                'description': "All screens off at 9pm. Blue light suppresses melatonin. Your sleep (and mood) need darkness, not an Instagram feed."
            },
            {
                'emoji': '🤝',
                'title': 'Reach Out, Not to the Feed',
                'description': "Text a real friend instead of opening an app. Human connection is what your brain actually craves when you're feeling low."
            }
        ]
    }
    
    # Find dominant composite score
    dominant = max(composite_scores, key=composite_scores.get)
    
    return tip_library.get(dominant, tip_library['adhd_score'])

def compute_shap_for_prediction(model, model_name, features_scaled):
    """Compute SHAP values for a single prediction."""
    try:
        if model_name in ['Random Forest', 'XGBoost']:
            explainer = shap.TreeExplainer(model)
            shap_values = explainer.shap_values(features_scaled)
            
            # Handle multiclass SHAP output
            if isinstance(shap_values, list):
                # Average across classes
                shap_mean = np.mean([np.abs(sv[0]) for sv in shap_values], axis=0)
            else:
                shap_mean = np.abs(shap_values[0] if len(shap_values.shape) > 1 else shap_values)
            
            shap_dict = dict(zip(FEATURE_COLS, shap_mean))
            # Sort by absolute value, return top 8
            shap_dict = dict(sorted(shap_dict.items(), key=lambda x: abs(x[1]), reverse=True)[:8])
            return {k: float(v) for k, v in shap_dict.items()}
        else:
            # For Logistic Regression, return feature importance as fallback
            return dict(list(feature_importance.items())[:8])
    except Exception as e:
        print(f"⚠ SHAP computation failed: {str(e)}")
        return dict(list(feature_importance.items())[:8])

# ============================================================================
# ROUTES
# ============================================================================

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    try:
        total_predictions = len(get_predictions_from_storage())
        
        # Count fallback records
        try:
            with open(FALLBACK_FILE, 'r') as f:
                fallback_count = len(json.load(f))
        except:
            fallback_count = 0
        
        return jsonify({
            'api_status': 'ok',
            'models_loaded': list(models.keys()),
            'mongodb_connected': predictions_collection is not None,
            'total_predictions': total_predictions,
            'fallback_count': fallback_count
        }), 200
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'code': 500
        }), 500

@app.route('/predict', methods=['POST'])
def predict():
    """Main prediction endpoint."""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = [
            'age', 'gender', 'relationship_status', 'occupation', 'social_media_hours',
            'purposeless_use', 'distracted_by_sm', 'restless_without_sm', 'easily_distracted',
            'bothered_by_worries', 'difficulty_concentrating', 'compare_to_others',
            'feelings_about_comparisons', 'seek_validation', 'feel_depressed',
            'interest_fluctuation', 'sleep_issues'
        ]
        
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({
                'error': f"Missing required fields: {', '.join(missing_fields)}",
                'code': 400
            }), 400
        
        # Get model selection (default to Random Forest)
        model_name = data.get('model', 'Random Forest')
        if model_name not in models:
            return jsonify({
                'error': f"Invalid model: {model_name}. Choose from {list(models.keys())}",
                'code': 400
            }), 400
        
        model = models[model_name]
        
        # ====================================================================
        # COMPUTE COMPOSITE SCORES
        # ====================================================================
        adhd_score = np.mean([
            data['purposeless_use'],
            data['distracted_by_sm'],
            data['easily_distracted']
        ])
        
        anxiety_score = np.mean([
            data['restless_without_sm'],
            data['bothered_by_worries']
        ])
        
        self_esteem_score = np.mean([
            data['compare_to_others'],
            data['feelings_about_comparisons'],
            data['seek_validation']
        ])
        
        depression_score = np.mean([
            data['feel_depressed'],
            data['interest_fluctuation'],
            data['sleep_issues']
        ])
        
        # Wellness score
        composite_mean = np.mean([adhd_score, anxiety_score, self_esteem_score, depression_score])
        wellness_score = round(100 - (composite_mean / 5 * 100), 2)
        
        # ====================================================================
        # ENCODE CATEGORICAL FEATURES
        # ====================================================================
        age = float(data['age'])
        
        gender = data['gender']
        if gender in label_encoders['gender'].classes_:
            gender_encoded = label_encoders['gender'].transform([gender])[0]
        else:
            gender_encoded = 0  # Default
        
        relationship_status = data['relationship_status']
        if relationship_status in label_encoders['relationship_status'].classes_:
            relationship_encoded = label_encoders['relationship_status'].transform([relationship_status])[0]
        else:
            relationship_encoded = 0
        
        occupation = data['occupation']
        if occupation in label_encoders['occupation'].classes_:
            occupation_encoded = label_encoders['occupation'].transform([occupation])[0]
        else:
            occupation_encoded = 0
        
        # Social media hours — handle both numeric and categorical
        social_media_hours = data['social_media_hours']
        if isinstance(social_media_hours, str):
            hours_mapping = {
                'Less than 1 hr': 0.5,
                'Less than 1 hour': 0.5,
                'Less than an Hour': 0.5,
                '1–2 hrs': 1.5,
                'Between 1 and 2 hours': 1.5,
                '2–3 hrs': 2.5,
                'Between 2 and 3 hours': 2.5,
                '3–4 hrs': 3.5,
                'Between 3 and 4 hours': 3.5,
                '4–5 hrs': 4.5,
                'Between 4 and 5 hours': 4.5,
                'More than 5 hrs': 6.0,
                'More than 5 hours': 6.0
            }
            social_media_hours = hours_mapping.get(social_media_hours, 3.0)
        else:
            social_media_hours = float(social_media_hours)
        
        # ====================================================================
        # PREPARE FEATURE VECTOR
        # ====================================================================
        features = np.array([[
            age,
            gender_encoded,
            relationship_encoded,
            occupation_encoded,
            social_media_hours,
            adhd_score,
            anxiety_score,
            self_esteem_score,
            depression_score
        ]])
        
        # Scale features
        features_scaled = scaler.transform(features)
        
        # ====================================================================
        # PREDICT
        # ====================================================================
        prediction = int(model.predict(features_scaled)[0])
        probability = float(model.predict_proba(features_scaled)[0][prediction])
        
        risk_levels = {0: 'Healthy', 1: 'At Risk', 2: 'Burnout'}
        risk_level = risk_levels[prediction]
        
        # ====================================================================
        # SHAP EXPLANATION
        # ====================================================================
        shap_values = compute_shap_for_prediction(model, model_name, features_scaled)
        
        # ====================================================================
        # PERSONALIZED TIPS
        # ====================================================================
        composite_scores = {
            'adhd_score': adhd_score,
            'anxiety_score': anxiety_score,
            'self_esteem_score': self_esteem_score,
            'depression_score': depression_score
        }
        personalized_tips = get_personalized_tips(composite_scores)
        
        # ====================================================================
        # BUILD RESPONSE
        # ====================================================================
        timestamp = datetime.utcnow().isoformat() + 'Z'
        
        result = {
            'prediction': prediction,
            'risk_level': risk_level,
            'probability': round(probability, 3),
            'wellness_score': wellness_score,
            'adhd_score': round(adhd_score, 2),
            'anxiety_score': round(anxiety_score, 2),
            'self_esteem_score': round(self_esteem_score, 2),
            'depression_score': round(depression_score, 2),
            'shap_values': shap_values,
            'personalized_tips': personalized_tips,
            'model_used': model_name,
            'timestamp': timestamp
        }
        
        # ====================================================================
        # SAVE TO DATABASE
        # ====================================================================
        save_data = {
            **result,
            'age': age,
            'gender': gender,
            'relationship_status': relationship_status,
            'occupation': occupation,
            'social_media_hours': social_media_hours
        }
        save_prediction_mongodb(save_data)
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'code': 500
        }), 500

@app.route('/history', methods=['GET'])
def history():
    """Get all prediction history."""
    try:
        predictions = get_predictions_from_storage()
        
        # Sort by timestamp descending
        predictions.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        
        return jsonify({
            'predictions': predictions,
            'total': len(predictions)
        }), 200
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'code': 500
        }), 500

@app.route('/stats', methods=['GET'])
def stats():
    """Aggregate statistics across all predictions."""
    try:
        predictions = get_predictions_from_storage()
        
        if not predictions:
            return jsonify({
                'total_predictions': 0,
                'risk_distribution': {'Healthy': 0, 'At Risk': 0, 'Burnout': 0},
                'avg_wellness_score': 0,
                'avg_social_media_hours': 0,
                'avg_sleep_issues': 0,
                'top_risk_factors': []
            }), 200
        
        # Risk distribution
        risk_distribution = {'Healthy': 0, 'At Risk': 0, 'Burnout': 0}
        for pred in predictions:
            risk = pred.get('risk_level', 'Unknown')
            if risk in risk_distribution:
                risk_distribution[risk] += 1
        
        # Averages
        wellness_scores = [p.get('wellness_score', 0) for p in predictions]
        avg_wellness = round(np.mean(wellness_scores), 2) if wellness_scores else 0
        
        sm_hours = [p.get('social_media_hours', 0) for p in predictions if 'social_media_hours' in p]
        avg_sm_hours = round(np.mean(sm_hours), 2) if sm_hours else 0
        
        depression_scores = [p.get('depression_score', 0) for p in predictions]
        avg_sleep_issues = round(np.mean(depression_scores), 2) if depression_scores else 0
        
        # Top risk factors from feature importance
        top_risk_factors = list(feature_importance.keys())[:3]
        
        return jsonify({
            'total_predictions': len(predictions),
            'risk_distribution': risk_distribution,
            'avg_wellness_score': avg_wellness,
            'avg_social_media_hours': avg_sm_hours,
            'avg_sleep_issues': avg_sleep_issues,
            'top_risk_factors': top_risk_factors
        }), 200
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'code': 500
        }), 500

@app.route('/feature-importance', methods=['GET'])
def get_feature_importance():
    """Return feature importance rankings."""
    try:
        return jsonify({
            'feature_importance': feature_importance,
            'model': metrics.get('model_name', 'Unknown')
        }), 200
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'code': 500
        }), 500

# ============================================================================
# RUN SERVER
# ============================================================================
if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("🌿 ZenFeed API is running")
    print("=" * 60)
    print(f"✓ Models: {list(models.keys())}")
    print(f"✓ MongoDB: {'Connected' if predictions_collection is not None else 'Using fallback JSON'}")
    print(f"✓ Endpoints: /predict, /history, /health, /stats, /feature-importance")
    print("=" * 60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
