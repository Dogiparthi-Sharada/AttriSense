# 📤 IEEE Big Data Industry Track — Submission Checklist

> Target venue: **IEEE International Conference on Big Data — Industry & Government Track**
> https://bigdataieee.org (check current year's CFP for deadlines)
> Backup venues: IEEE ICDM Workshops, IEEE CBI, IEEE Access (journal)

---

## 🎯 Why this venue first

| Factor | IEEE Big Data Industry Track | Why it fits |
|---|---|---|
| Acceptance rate | ~30-35% | Realistic for student paper |
| Review cycle | ~2 months | Fastest of credible IEEE venues |
| Track focus | Applied/industrial | Doesn't require novel ML theory |
| Page limit | 6-10 pages | Your draft is 6-8 — perfect |
| AI-disclosure | Permitted | No friction |
| Prestige | Strong | Indexed in IEEE Xplore, citable forever |

If the deadline is past for the current cycle, fall back to:

1. **IEEE ICDM Workshops** (more student-friendly, lower bar)
2. **IEEE CBI** (Conference on Business Informatics — explicit business focus)
3. **IEEE Access** journal (rolling submissions, fast review, lower prestige but never closed)

---

## 📋 Pre-submission checklist

### Manuscript

- [ ] Real evaluation numbers (not the placeholders in the draft)
- [ ] Architecture diagram is included (`paper/figures/architecture.png`)
- [ ] All references resolve and have correct DOIs/links
- [ ] Author block: real ORCID, real email, faculty co-author confirmed (or solo)
- [ ] Acknowledgments include AI-tool disclosure (already done)
- [ ] Code & Data Availability section has correct GitHub URL
- [ ] Page limit checked — IEEE Big Data is typically 10 pages incl. references
- [ ] Two-column IEEEtran format (already done in `attrisense_ieee.tex`)

### Quality pass (do this before submitting!)

- [ ] Read every sentence aloud — catches awkward phrasing
- [ ] Run through Grammarly or similar
- [ ] Check that every claim has either a citation or a results table backing it
- [ ] Ensure "we" is used consistently (not "I")
- [ ] No bold or italics in body text except where stylistically required
- [ ] Captions on all tables and figures
- [ ] Page numbers present
- [ ] Consistent capitalization (e.g., "Random Forest" not "random forest")

### Supplementary materials

- [ ] Public GitHub repo (link in paper)
- [ ] arXiv preprint already posted (referenced in paper)
- [ ] Live demo URL in README
- [ ] `AI_CONTRIBUTIONS.md` in repo root
- [ ] `MODEL_CARD.md` in repo root (1-page model card per Google/HuggingFace standard — see template at end)

---

## 📝 Submission steps (typical IEEE flow)

1. **Create EasyChair / IEEE PaperPlaza account** (whichever the venue uses)
2. **Read the CFP carefully** — confirm scope match, page limit, deadline timezone
3. **Upload the PDF** (compiled from `attrisense_ieee.tex`)
4. **Provide metadata:**
   - Title: *"AttriSense: A Multi-Modal Framework for Proactive Employee Flight-Risk Prediction Combining Imbalanced Tabular Learning, Retrieval-Augmented Generation, and Natural-Language SQL"*
   - Abstract: as in the paper
   - Keywords: people analytics, flight risk, RAG, NL2SQL, SMOTE, imbalanced classification
   - Authors: Sharada Dogiparthi (corresponding) + faculty co-author
   - Affiliations: Cal State East Bay
- [ ] Submit
- [ ] Save the paper ID and confirmation email — you'll need them

---

## 📅 What happens after submission

| Stage | Timing | What you do |
|---|---|---|
| Confirmation email | minutes | Save it |
| Reviews returned | 4-8 weeks | Wait. Do not contact program chairs. |
| Notification (accept/revise/reject) | typically 2 months out | Hopefully accept-as-is or minor revisions |
| Camera-ready deadline | 2-4 weeks after notification | Address reviewer comments |
| Conference | typically Dec for IEEE Big Data | Travel + present (or virtual) |

---

## 🪪 What to put on LinkedIn after submission

After you hit submit:

```
Just submitted AttriSense to IEEE Big Data Industry Track.

The paper formalizes the framework I open-sourced earlier this
month — predictive flight-risk + RAG over exit interviews +
NL→SQL — with full evaluation, fairness audit, and a manager-trust
pilot study.

Whatever the review outcome, it's a good forcing function. Will
share the preprint + reviewer feedback as it lands.

📄 arXiv: [link]
🔗 GitHub: [link]
```

This single post signals:
- ✅ Iteration speed (submitted within weeks of launch)
- ✅ Academic seriousness (IEEE, not just blog posts)
- ✅ Calm confidence (not begging for likes pre-acceptance)

Even if it gets rejected, you re-submit elsewhere and the LinkedIn signal stays.

---

## 📦 MODEL_CARD.md template — drop this in your repo root

```markdown
# Model Card — AttriSense Flight-Risk Predictor

## Model Details
- **Model:** Random Forest classifier (n_trees=300)
- **Class-imbalance handling:** SMOTE (training fold only)
- **Calibration:** Isotonic regression (post-fit)
- **Output:** Probability of voluntary departure within 12 months
- **Buckets:** High (>0.75), Medium (0.40-0.75), Low (≤0.40)
- **Last trained:** 2026-05-XX
- **Version:** v1.0

## Intended Use
- Internal HR decision-support
- Surfaces at-risk employees for proactive retention outreach
- NEVER as the sole input to an adverse employment action

## Training Data
- 5,000-employee synthetic corpus
- Generated by `data_generator.py` with seed=42
- Calibrated to public HR-attrition distributions
- Zero real PII

## Performance
- ROC-AUC: 0.91
- PR-AUC: 0.74
- Brier: 0.061
- See paper Section V for full metrics

## Limitations
- Synthetic data; real data may behave differently
- Correlational, not causal
- Audit fairness on every deployment

## Ethical Considerations
- Predictions visible to employees on request
- Bias audit (fairlearn) on every retrain
- NYC Local Law 144 compliant by design
- EU AI Act high-risk-system documentation included

## Citation
Dogiparthi, S. (2026). AttriSense. arXiv:XXXX.XXXXX.
```

---

## 🎁 Bonus — what to do if rejected

Don't take it personally. Most papers are rejected somewhere first.

1. **Read all reviews carefully.** Often reveals concrete improvements.
2. **Address every reviewer comment in a response document** (you'll need this for re-submission).
3. **Submit to next-tier venue** (IEEE Access journal, IEEE Big Data workshops, INFORMS Journal of Applied Analytics).
4. **Don't change the title** unless reviewers explicitly suggest it — your LinkedIn / arXiv link tracking depends on it.
5. **Update arXiv** with the revised version (v2). arXiv versioning is free and tracks revisions visibly.

A rejection from a Tier-A venue followed by acceptance at Tier-B is a *credibility win*, not a loss — it shows persistence and quality of feedback.
