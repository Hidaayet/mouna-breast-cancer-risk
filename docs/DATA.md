# Data Strategy — Mouna

---

## 1. Datasets Used (Stage 1 — Research Prototype)

### 1.1 Wisconsin Breast Cancer Dataset
- **Source:** UCI Machine Learning Repository
- **URL:** archive.ics.uci.edu/dataset/17/breast+cancer+wisconsin+diagnostic
- **Samples:** 569 (357 benign, 212 malignant)
- **Features:** 30 numeric features from fine needle aspirate
- **Use:** Model benchmarking and initial pipeline validation
- **Limitation:** FNA features only — no questionnaire or biomarker data

### 1.2 Breast Cancer Risk Factor Dataset
- **Source:** Kaggle / published studies
- **Features:** Demographic + reproductive risk factors
- **Use:** Questionnaire feature training

### 1.3 Synthetic Biomarker Augmentation
- GGT and ALT distributions generated from published population statistics
- Correlation with cancer risk based on published meta-analyses
- Clearly labeled as synthetic — not used for clinical claims

---

## 2. Stage 2 Data Requirements (Clinical Validation)

- Minimum 1,000 Tunisian women aged 30-75
- Prospective collection with informed consent
- Features: full questionnaire + GGT + ALT from routine blood tests
- Outcome: biopsy-confirmed diagnosis or 2-year follow-up
- Ethics approval: Institut Salah Azaiez (Tunis) or equivalent

---

## 3. Data Privacy

- No personally identifiable information stored
- All data pseudonymized at collection
- Local processing only — no cloud transmission of patient data
- GDPR-compatible data handling
```