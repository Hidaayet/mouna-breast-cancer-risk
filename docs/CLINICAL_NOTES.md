# Clinical Notes — Mouna Risk Assessment Tool

**Version:** 1.0 (Research Prototype)
**Author:** Hidayet Allah Yaakoubi
**Status:** Pre-validation — not for clinical use

---

## 1. Intended Use

Mouna is intended as a **clinical decision support tool** for use by
primary care physicians and trained healthcare workers in low-resource
settings. It is designed to:

- Identify women who may benefit from further breast cancer screening
- Support — not replace — clinical judgment
- Generate structured risk reports for physician review
- Facilitate referral decisions in resource-limited environments

Mouna is NOT intended to:
- Diagnose breast cancer
- Replace mammography or clinical breast examination
- Be used by patients without physician involvement
- Provide definitive medical advice

---

## 2. Target Population

- Women aged 30-75
- No prior breast cancer diagnosis
- Accessible primary care setting
- Low-resource environment where mammography is unavailable

---

## 3. Risk Factors Included

### 3.1 Questionnaire Features

| Feature | Clinical Basis |
|---|---|
| Age | Strongest single predictor — risk doubles every 10 years after 40 |
| BMI | Obesity increases postmenopausal breast cancer risk by 30-60% |
| Family history (1st degree) | 2x risk if mother or sister affected |
| Family history (2nd degree) | 1.5x risk |
| BRCA mutation (self-reported) | 5-7x lifetime risk |
| Age at menarche | Early menarche (<12) increases risk via prolonged estrogen exposure |
| Age at menopause | Late menopause (>55) increases risk |
| Parity (number of pregnancies) | Nulliparity or late first birth increases risk |
| Breastfeeding history | Protective — each year reduces risk ~4.3% |
| HRT use | Combined estrogen-progestogen increases risk |
| Oral contraceptive use | Slight increase during use, returns to baseline after |
| Alcohol consumption | Each drink/day increases risk ~7-10% |
| Smoking | Modest independent risk factor |
| Physical activity | Protective — 30+ min/day reduces risk ~10-20% |
| Prior benign breast disease | Atypical hyperplasia increases risk 4x |

### 3.2 Blood Biomarkers

| Biomarker | Normal Range | Clinical Basis |
|---|---|---|
| GGT (U/L) | 5-40 (women) | Oxidative stress marker; elevated GGT associated with systemic inflammation and cancer risk |
| ALT (U/L) | 7-35 (women) | Hepatic metabolic marker; elevation linked to obesity-related cancer risk |

**Reference:** Kunutsor et al. (2015) — GGT and cancer risk meta-analysis.
Brenner et al. (2010) — Liver enzymes and breast cancer risk.

---

## 4. Risk Score Interpretation

| Score | Category | Recommended Action |
|---|---|---|
| 0-25 | Low Risk | Routine screening per national guidelines |
| 26-50 | Moderate Risk | Enhanced surveillance; consider annual clinical breast exam |
| 51-75 | High Risk | Refer to specialist; consider mammography if available |
| 76-100 | Very High Risk | Urgent specialist referral; mammography and/or genetic counseling |

---

## 5. Known Limitations

- Model trained on predominantly Western population data (SEER)
- Tunisian/North African population-specific validation pending
- Self-reported risk factors subject to recall bias
- GGT and ALT are non-specific — elevation has many causes beyond cancer risk
- Does not account for imaging findings or prior biopsy results
- Binary family history questions miss complex pedigree information

---

## 6. Planned Clinical Validation

**Phase 1 — Retrospective validation:**
Apply model to existing Tunisian patient records (with ethics approval)
to assess performance in local population.

**Phase 2 — Prospective pilot:**
Deploy in 2-3 primary care clinics in Tunis.
Collect 500+ patient assessments over 12 months.
Compare risk scores with subsequent clinical findings.

**Phase 3 — Multi-site validation:**
Expand to rural clinics and other North African countries.

---

## 7. Ethical Considerations

- All risk assessments must be delivered with physician involvement
- Patients must provide informed consent
- High-risk results must be accompanied by clear explanation and referral pathway
- Tool must not be used to deny care or create anxiety without follow-up support
- Regular recalibration as new evidence emerges