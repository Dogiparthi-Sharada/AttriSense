# AttriSense Model Card

## Intended Use

AttriSense is a synthetic-data workforce intelligence demo. It predicts voluntary-turnover risk, explains high-risk scores with SHAP, simulates possible retention actions, and summarizes risk at employee, manager, and department levels.

The model is intended for portfolio demonstration, analytics prototyping, and responsible-AI discussion. It is not approved for real employment decisions.

## Data

The included records are synthetic. They contain employee ID, department, tenure, base salary, manager ID, manager tenure, voluntary-turnover label, and synthetic exit-interview text.

Synthetic data keeps the repository public and safe, but it does not represent a real company's workforce distribution.

## Model

- Primary model: Random Forest classifier with SMOTE balancing.
- Explainability: SHAP values for all high-risk employees plus a representative risk-weighted sample.
- Survival layer: Cox proportional hazards model for cohort survival curves and median expected tenure.
- Calibration layer: holdout calibration bins and Brier score.

## Limitations

- Predictions are correlational, not causal.
- Synthetic labels encode simplified risk patterns and should not be treated as real workforce behavior.
- Department and manager signals must be audited before any production deployment.
- The What-If Simulator estimates model response, not guaranteed intervention impact.
- The survival model is a demo time-to-event layer and requires real longitudinal validation before use.

## Responsible Use Policy

AttriSense should be used to support employees, not punish them. Scores should never be used as the sole basis for termination, compensation denial, promotion denial, or disciplinary action.

Any real deployment should include:

- Independent bias audit.
- Human review before action.
- Clear employee and candidate notices where required.
- NYC Local Law 144 review if used in covered employment decision contexts.
- Documentation of features, thresholds, monitoring, and appeal process.

## Monitoring Checklist

- Track calibration drift by quarter.
- Review risk rates by department and manager group.
- Compare suggested interventions against actual retention outcomes.
- Revalidate SHAP driver stability after each retrain.
- Maintain an audit log for any HR action influenced by model output.
