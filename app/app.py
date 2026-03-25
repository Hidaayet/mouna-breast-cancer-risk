from flask import Flask, request, jsonify, render_template
import numpy as np
import joblib
import os
import math

app = Flask(__name__)

# load BCSC-trained model artifacts
BASE = os.path.dirname(os.path.abspath(__file__))
scaler       = joblib.load(os.path.join(BASE, '../data/models/scaler_bcsc.pkl'))
feature_cols = joblib.load(os.path.join(BASE, '../data/models/feature_cols_bcsc.pkl'))
model        = joblib.load(os.path.join(BASE, '../data/models/mouna_bcsc_model.pkl'))

def engineer_input(d):
    """Apply same feature engineering as BCSC training pipeline."""
    d['nulliparous']         = int(d['age_first_birth'] == 0)
    d['age_bmi_interaction'] = d['age'] * d['bmi'] / 100
    d['postmenopausal']      = int(d['menopaus'] >= 2)
    d['postmeno_hrt']        = int(d['postmenopausal'] == 1 and d['current_hrt'] == 1)
    d['early_menarche']      = int(d['age_menarche'] <= 11)
    d['late_first_birth']    = int(d['age_first_birth'] >= 30)
    d['dense_breasts']       = int(d['BIRADS_breast_density'] >= 3)
    d['age_group']           = (0 if d['age'] <= 40 else
                                 1 if d['age'] <= 50 else
                                 2 if d['age'] <= 60 else
                                 3 if d['age'] <= 70 else 4)
    return d

def calibrate_probability(prob_raw):
    """
    Recalibrate SMOTE-trained probability to real-world prevalence.
    SMOTE trained on 50/50 balance but real BCSC prevalence is 7.5%.
    Uses log-odds adjustment (Platt scaling correction).
    """
    eps = 1e-10
    log_odds = math.log((prob_raw + eps) / (1 - prob_raw + eps))
    # correction term: shift from 50% training prevalence to 7.5% real prevalence
    correction = math.log(0.075 / 0.925) - math.log(0.5 / 0.5)
    log_odds_calibrated = log_odds + correction
    prob_calibrated = 1 / (1 + math.exp(-log_odds_calibrated))
    return prob_calibrated

def get_risk_category(prob):
    if prob < 0.06:
        return ("Low Risk", "#00e5a0",
                "Your risk profile is below average. "
                "Continue routine screening per national guidelines.")
    elif prob < 0.15:
        return ("Moderate Risk", "#ff9640",
                "Your risk profile is above average. "
                "Enhanced surveillance recommended — "
                "consider annual clinical breast exam.")
    elif prob < 0.35:
        return ("High Risk", "#ff4d6d",
                "Your risk profile is elevated. "
                "Specialist referral recommended. "
                "Consider mammography if available.")
    else:
        return ("Very High Risk", "#ff0044",
                "Your risk profile is significantly elevated. "
                "Urgent specialist referral strongly advised. "
                "Mammography and genetic counseling recommended.")

def get_top_factors(d):
    factors = []
    if d['age'] >= 60:
        factors.append(f"Age {int(d['age'])} — risk increases significantly after 60")
    if d['biophx'] == 1:
        factors.append("Prior benign biopsy — strongest single predictor in real clinical data")
    if d['postmeno_hrt'] == 1:
        factors.append("Postmenopausal HRT use — significantly increases risk")
    if d['first_degree_hx'] == 1:
        factors.append("First-degree family history — doubles baseline risk")
    if d['dense_breasts'] == 1:
        factors.append(f"Dense breast tissue (BIRADS {int(d['BIRADS_breast_density'])}) "
                       f"— increases risk and reduces mammography sensitivity")
    if d['bmi'] >= 30:
        factors.append(f"BMI {d['bmi']:.1f} — obesity increases postmenopausal breast cancer risk")
    if d['early_menarche'] == 1:
        factors.append("Early menarche (≤11) — prolonged estrogen exposure increases risk")
    if d['late_first_birth'] == 1:
        factors.append("Late first birth (≥30) — increases lifetime risk")
    if d['nulliparous'] == 1:
        factors.append("No pregnancies — nulliparity increases lifetime risk")
    if d['current_hrt'] == 0 and d['postmenopausal'] == 1:
        factors.append("No HRT use — lower hormonal risk ✓")
    if d['biophx'] == 0 and d['first_degree_hx'] == 0:
        factors.append("No family history or prior biopsy — lower baseline risk ✓")
    return factors[:5]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test')
def test():
    return jsonify({
        'status': 'ok',
        'model': 'BCSC XGBoost',
        'features': feature_cols,
        'n_features': len(feature_cols)
    })

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()

        # parse and validate inputs
        features = {
            'age':                   float(data['age']),
            'first_degree_hx':       int(float(data['first_degree_hx'])),
            'age_menarche':          float(data['age_menarche']),
            'age_first_birth':       float(data['age_first_birth']),
            'BIRADS_breast_density': int(float(data['BIRADS_breast_density'])),
            'current_hrt':           int(float(data['current_hrt'])),
            'menopaus':              int(float(data['menopaus'])),
            'bmi':                   float(data['bmi']),
            'biophx':                int(float(data['biophx'])),
        }

        # engineer features
        features = engineer_input(features)

        # build feature vector in correct order
        X = np.array([[features[f] for f in feature_cols]])
        X_scaled = scaler.transform(X)

        # raw model probability
        prob_raw = float(model.predict_proba(X_scaled)[0, 1])

        # calibrate to real-world prevalence
        prob_calibrated = calibrate_probability(prob_raw)

        # risk score 0-100
        risk_score = round(prob_calibrated * 100, 1)

        category, color, recommendation = get_risk_category(prob_calibrated)
        top_factors = get_top_factors(features)

        return jsonify({
            'risk_score':     risk_score,
            'category':       category,
            'color':          color,
            'recommendation': recommendation,
            'top_factors':    top_factors,
            'model_info':     'Trained on 244,737 real patients · BCSC registry · AUC 0.926',
            'disclaimer':     ('Research prototype. Results must be interpreted by a qualified '
                               'healthcare professional. Not a diagnostic tool.')
        })

    except KeyError as e:
        return jsonify({'error': f'Missing field: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)