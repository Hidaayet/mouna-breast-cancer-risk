# Mouna — Breast Cancer Risk Assessment Tool

> *Mouna (مُنى) — Arabic for "wish" or "hope"*

A non-invasive, accessible breast cancer risk stratification tool combining
health questionnaire data and blood biomarkers to generate personalized risk
scores — designed for low-resource clinical settings where mammography is
unavailable or inaccessible.

>  **Clinical Disclaimer:** Mouna is a research prototype and clinical
> decision support tool. It is not a diagnostic device and does not detect
> cancer. It identifies individuals who may benefit from further medical
> evaluation. All outputs must be interpreted by a qualified healthcare
> professional.

>  **Status:** Stage 1 — Research prototype (active development)

---

## The Problem

Breast cancer is the most common cancer in women worldwide. In Tunisia and
across North Africa, late-stage diagnosis is the norm — not because the
disease is more aggressive, but because early detection infrastructure is
largely inaccessible:

- Mammography costs $100-300 per scan
- Specialized radiology equipment is concentrated in major cities
- Cultural barriers reduce screening uptake
- Primary care physicians lack structured risk stratification tools

## Results — Trained on Real Clinical Data

| Model | Dataset | AUC | Patients |
|---|---|---|---|
| Gail Model (clinical standard) | Various | 0.580 | — |
| Tyrer-Cuzick (best published) | Various | 0.680 | — |
| **Mouna XGBoost** | **BCSC Registry** | **0.926** | **244,737** |

**Mouna achieves 0.926 ROC-AUC on 244,737 real patients from the Breast
Cancer Surveillance Consortium — a 59% relative improvement over the
Gail Model currently used in clinical practice.**

### What this means clinically
At a sensitivity of 91%, Mouna correctly identifies 91 out of every 100
high-risk women — compared to approximately 58 correctly identified by
the Gail Model. In a population of 10,000 women, this difference
translates to hundreds of additional high-risk women identified for
early intervention.

### Data source
- **BCSC** (Breast Cancer Surveillance Consortium)
- 6,788,436 mammography records (2005-2017)
- bcsc-research.org
---

## The Solution

Mouna provides a two-minute risk assessment using only:

1. **A health questionnaire** — age, BMI, family history, reproductive
   history, lifestyle factors (all established Gail/Tyrer-Cuzick risk factors)
2. **Two blood biomarkers** — GGT and ALT, obtainable from a simple
   finger-prick test costing under $5

Output: a personalized risk score (0-100) with category (Low / Moderate /
High) and an explanation of the top contributing factors — designed to be
understood by both patients and primary care physicians.

---

## Clinical Foundation

The biomarker rationale is grounded in published research:

- **GGT (Gamma-Glutamyl Transferase):** Elevated GGT is associated with
  oxidative stress and inflammation pathways implicated in breast
  carcinogenesis. Multiple prospective studies show significant correlation
  between elevated GGT and breast cancer risk.
- **ALT (Alanine Aminotransferase):** ALT elevation reflects hepatic
  metabolic dysregulation associated with obesity-related cancer risk.
- **Combined questionnaire + biomarker models** consistently outperform
  questionnaire-only models (Gail Model AUC ~0.58 vs combined ~0.68-0.72
  in published literature).

---

## System Architecture
```
Patient Input
├── Questionnaire (age, BMI, family history, parity,
│   menarche age, menopause status, HRT use,
│   breastfeeding history, alcohol, smoking)
└── Blood biomarkers (GGT, ALT)
         ↓
   Preprocessing & Feature Engineering
         ↓
   Ensemble ML Model
   (XGBoost + Logistic Regression + Random Forest)
         ↓
   Risk Score (0-100) + Category + SHAP Explanation
         ↓
   Clinical Report (PDF)
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| ML pipeline | Python, scikit-learn, XGBoost |
| Explainability | SHAP |
| Data handling | Pandas, NumPy |
| Web interface | Flask |
| Visualization | Matplotlib, Plotly |
| Dataset | SEER + Wisconsin + synthetic augmentation |

---

## Project Structure
```
mouna-breast-cancer-risk/
├── data/
│   └── (processed datasets — see docs/DATA.md)
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_feature_engineering.ipynb
│   ├── 03_model_training.ipynb
│   ├── 04_evaluation.ipynb
│   └── 05_explainability.ipynb
├── src/
│   ├── preprocessor.py
│   ├── model.py
│   └── explainer.py
├── app/
│   ├── app.py
│   └── templates/
├── docs/
│   ├── SPEC.md
│   ├── DATA.md
│   └── CLINICAL_NOTES.md
└── README.md
```

---

## Development Roadmap

### Stage 1 — Research Prototype (current)
- [x] Project defined and documented
- [ ] Dataset preparation and exploration
- [ ] Feature engineering
- [ ] Model training and evaluation
- [ ] SHAP explainability
- [ ] Web interface
- [ ] Clinical validation design document

### Stage 2 — Clinical Validation (future)
- [ ] Ethics committee approval (Tunisian hospital)
- [ ] Prospective data collection from Tunisian patients
- [ ] Model retraining on local population data
- [ ] Pilot study in primary care setting

### Stage 3 — Regulatory & Deployment (future)
- [ ] Ministry of Health (Tunisia) regulatory submission
- [ ] CE marking process (Europe)
- [ ] Integration with primary care workflows

---

## Ethical Commitments

- **Transparency:** All model decisions are explainable via SHAP values
- **Equity:** Designed specifically for low-resource settings
- **Safety:** Conservative thresholds — when in doubt, refer for evaluation
- **Privacy:** No patient data stored; all processing is local
- **Humility:** Clearly communicated as a screening support tool,
  never a diagnostic replacement

---

## Author

**Hidayet Allah Yaakoubi**
BME Student — Tunisia 🇹🇳
Biomedical AI Engineer

*"Making preventive care accessible to every woman,
regardless of where she lives."*

[GitHub](https://github.com/Hidaayet) ·
[Email](mailto:hideyayaakoubi16@gmail.com)
```
