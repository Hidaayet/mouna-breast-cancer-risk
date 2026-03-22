from flask import Flask, request, jsonify, render_template
import numpy as np
import joblib
import os

app = Flask(__name__)

# load model artifacts
BASE = os.path.dirname(os.path.abspath(__file__))
scaler       = joblib.load(os.path.join(BASE, '../data/models/scaler.pkl'))
feature_cols = joblib.load(os.path.join(BASE, '../data/models/feature_cols.pkl'))
ensemble     = joblib.load(os.path.join(BASE, '../data/models/mouna_ensemble.pkl'))

def engineer_input(d):
    """Apply same feature engineering as training pipeline."""
    d['reproductive_years']   = d['age_menopause'] - d['age_menarche']
    d['age_bmi_interaction']  = d['age'] * d['bmi'] / 100
    d['biomarker_score']      = (np.log1p(d['ggt']) * 0.6 +
                                  np.log1p(d['alt']) * 0.4)
    d['ggt_elevated']         = int(d['ggt'] > 40)
    d['alt_elevated']         = int(d['alt'] > 35)
    d['both_elevated']        = int(d['ggt'] > 40 and d['alt'] > 35)
    d['family_risk_score']    = (d['brca_mutation'] * 5 +
                                  d['family_history_1st'] * 2 +
                                  d['family_history_2nd'] * 1)
    d['hormonal_score']       = (d['hrt_use'] * 2 +
                                  d['oral_contraceptive_use'] * 1 +
                                  int(d['age_menarche'] <= 11) +
                                  int(d['age_menopause'] >= 55))
    d['lifestyle_score']      = (d['alcohol_drinks_week'] * 1.5 +
                                  d['smoking'] * 1 +
                                  (2 - d['physical_activity']) * 1)
    d['nulliparous']          = int(d['parity'] == 0)
    d['age_group']            = (0 if d['age'] <= 40 else
                                  1 if d['age'] <= 50 else
                                  2 if d['age'] <= 60 else 3)
    d['bmi_category']         = (0 if d['bmi'] < 18.5 else
                                  1 if d['bmi'] < 25 else
                                  2 if d['bmi'] < 30 else 3)
    return d

def get_risk_category(prob):
    if prob < 0.25:   return "Low Risk",       "#00e5a0", "Routine screening per guidelines."
    elif prob < 0.50: return "Moderate Risk",  "#ff9640", "Enhanced surveillance recommended. Consider annual clinical breast exam."
    elif prob < 0.75: return "High Risk",       "#ff4d6d", "Specialist referral recommended. Consider mammography if available."
    else:             return "Very High Risk",  "#ff0044", "Urgent specialist referral. Mammography and/or genetic counseling strongly advised."

def get_top_factors(features_dict):
    """Return top risk factors for plain-language explanation."""
    factors = []
    if features_dict['age'] >= 60:
        factors.append(f"Age {int(features_dict['age'])} — risk increases significantly after 50")
    if features_dict['brca_mutation']:
        factors.append("BRCA mutation — very high genetic risk")
    if features_dict['family_history_1st']:
        factors.append("First-degree family history — doubles baseline risk")
    if features_dict['bmi'] >= 30:
        factors.append(f"BMI {features_dict['bmi']:.1f} — obesity increases postmenopausal risk")
    if features_dict['hrt_use']:
        factors.append("HRT use — combined therapy increases risk")
    if features_dict['prior_benign_biopsy']:
        factors.append("Prior benign biopsy — atypical hyperplasia increases risk 4x")
    if features_dict['alcohol_drinks_week'] >= 3:
        factors.append(f"{int(features_dict['alcohol_drinks_week'])} drinks/week — dose-dependent risk increase")
    if features_dict['ggt'] > 40:
        factors.append(f"Elevated GGT ({features_dict['ggt']:.0f} U/L) — above normal range")
    if features_dict['breastfeed_years'] >= 2:
        factors.append(f"Breastfeeding {features_dict['breastfeed_years']:.1f} years — protective factor ✓")
    if features_dict['physical_activity'] == 2:
        factors.append("Regular physical activity — protective factor ✓")
    return factors[:5]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()

        # build feature dict
        features = {
            'age':                    float(data['age']),
            'bmi':                    float(data['bmi']),
            'age_menarche':           float(data['age_menarche']),
            'age_menopause':          float(data['age_menopause']),
            'parity':                 int(data['parity']),
            'breastfeeding':          int(data['breastfeeding']),
            'breastfeed_years':       float(data['breastfeed_years']),
            'family_history_1st':     int(data['family_history_1st']),
            'family_history_2nd':     int(data['family_history_2nd']),
            'brca_mutation':          int(data['brca_mutation']),
            'alcohol_drinks_week':    int(data['alcohol_drinks_week']),
            'smoking':                int(data['smoking']),
            'physical_activity':      int(data['physical_activity']),
            'hrt_use':                int(data['hrt_use']),
            'oral_contraceptive_use': int(data['oral_contraceptive_use']),
            'prior_benign_biopsy':    int(data['prior_benign_biopsy']),
            'ggt':                    float(data['ggt']),
            'alt':                    float(data['alt']),
        }

        # engineer features
        features = engineer_input(features)

        # build feature vector in correct order
        X = np.array([[features[f] for f in feature_cols]])
        X_scaled = scaler.transform(X)

        # predict
        prob = ensemble.predict_proba(X_scaled)[0, 1]
        risk_score = round(prob * 100, 1)

        category, color, recommendation = get_risk_category(prob)
        top_factors = get_top_factors(features)

        return jsonify({
            'risk_score':     risk_score,
            'category':       category,
            'color':          color,
            'recommendation': recommendation,
            'top_factors':    top_factors,
            'disclaimer':     'This is a research prototype. Results must be interpreted by a qualified healthcare professional.'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)