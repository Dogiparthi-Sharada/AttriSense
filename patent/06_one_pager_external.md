# 06 — One-Pager (External / Public-Safe)

> Use this verbatim for portfolio sites, LinkedIn featured section, and
> recruiter outreach. Contains **no** patent-sensitive language; the IP
> details are in `01_patent_strategy.md` and `02_provisional_application_draft.md`.

---

## AttriSense

**An end-to-end workforce attrition system with fairness-gated causal
recommendations and privacy-preserving explanations.**

Open source · Python + Streamlit · 5,000-employee synthetic corpus · 13
analytical surfaces · p95 latency 410 ms on a laptop.

---

### Why it exists

Off-the-shelf attrition tools predict who is likely to leave but typically
(1) display predictions against raw employee identifiers, (2) recommend
interventions ranked by historical correlation rather than causal effect,
and (3) surface fairness issues only after recommendations have already
been circulated. AttriSense closes all three gaps simultaneously, in a
single application that runs on commodity hardware.

### What it does

- **Calibrated risk score** per employee (AUC = 0.872, ECE = 0.038).
- **Fairness gate**: blocks recommendations for any cohort below the
  EEOC four-fifths disparate-impact threshold (3 of 11 cohorts blocked
  in our evaluation).
- **Causal recommendations**: T-learner CATE selects the highest-uplift
  intervention from three arms; Qini = 0.187 vs. 0.041 for the
  correlation baseline.
- **Salted pseudonymous IDs**: reviewers see `RV-XXXXXX`, never the raw
  employee identifier; mapping table isolated.
- **Provider-resilient UX**: 250 ms reachability probe, deterministic
  local fallback for NL→SQL (TF-IDF gold corpus) and multilingual RAG
  (256-d hashing vectoriser).

### Where to look

- **Live demo (7 min):** *insert YouTube unlisted link*
- **Repository:** `github.com/<your-handle>/AttriSense`
- **Beginner's guide (DOCX, 79 pp):** `outputs/AttriSense_Beginners_Guide.docx`
- **VP pitch deck:** `outputs/AttriSense_VP_Pitch.pptx`
- **Paper draft:** `paper/`

### Built by

**Kundan Vanama** · *MS Computer Science · ML Engineer*
*linkedin.com/in/<your-handle> · <your-handle>@<your-domain>*
