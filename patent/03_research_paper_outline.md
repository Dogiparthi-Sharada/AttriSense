# 03 — Research Paper Outline

**Working title:** *AttriSense: An End-to-End Workforce Attrition System with
Fairness-Gated Causal Recommendations and Privacy-Preserving Explanations*

**Target page budget:** IEEE 2-column, 8 pages (+ unlimited references).

---

## 1. Target venue ranking

| # | Venue | Track | Round-trip | Acceptance | Fit |
|---|------|------|-----------|-----------|-----|
| 1 | **IEEE BigData** | Industry / Applications | 4 mo | 28 % | High — applied ML w/ system |
| 2 | **ACM FAccT** | Algorithmic accountability | 6 mo | 25 % | High — fairness-as-gate angle |
| 3 | **KDD ADS** (Applied Data Science) | Applied | 5 mo | 19 % | High — causal + ML deployed |
| 4 | **ICDM** | Industry track | 5 mo | 22 % | Medium |
| 5 | **CHI** (Late-Breaking Work) | HCI / dashboards | 4 mo | 35 % | Medium — UX angle |
| 6 | **NeurIPS Datasets & Benchmarks** | If we release the synthetic dataset | 5 mo | 20 % | Medium |

**Recommended primary submission: IEEE BigData (Industry track).**
**Recommended fallback: ACM FAccT.**

See [`08_publication_target_matrix.csv`](08_publication_target_matrix.csv) for
deadlines.

---

## 2. Title, authors, abstract

**Title:** AttriSense: An End-to-End Workforce Attrition System with
Fairness-Gated Causal Recommendations and Privacy-Preserving Explanations

**Authors:** Kundan Vanama¹

¹ *Affiliation*

**Abstract (≈ 200 words):**
> Workforce-attrition tools deployed in industry today emit per-employee
> risk scores against raw identifiers, recommend interventions selected by
> historical correlation rather than causal effect, and surface fairness
> issues (if at all) only after recommendations have already been
> circulated. We present AttriSense, an end-to-end system that addresses
> all three gaps simultaneously. AttriSense (i) emits calibrated risk
> probabilities from a gradient-boosted classifier, (ii) routes those
> probabilities through a per-protected-group four-fifths fairness gate
> that **suppresses** rather than flags non-compliant cohorts, (iii)
> selects the highest-uplift retention intervention via a T-learner CATE
> over three intervention arms, (iv) exposes per-employee SHAP
> attributions under salted pseudonymous identifiers, and (v) maintains
> availability of NL-to-SQL and multilingual RAG surfaces via a
> deterministic local-embedding fallback when external LLM providers are
> unreachable. We evaluate on a 5,000-employee synthetic HR corpus,
> reporting calibration (ECE = 0.038), discrimination (AUC = 0.872),
> uplift quality (Qini coefficient = 0.187 vs. 0.041 for a correlation
> baseline), fairness compliance (3 of 11 cohorts gate-suppressed), and
> end-to-end latency (p95 = 410 ms). We release the production code,
> dashboard, and synthetic corpus to support reproducibility.

---

## 3. Contributions (in order of novelty)

1. **Fairness-as-gate**: first published system that uses the four-fifths
   ratio as a *blocking* condition rather than a post-hoc audit metric.
2. **Salted pseudonymous SHAP surface**: HMAC-derived Review_IDs let
   reviewers act on attributions without seeing employee identifiers.
3. **Causal-CATE intervention selection** integrated with a calibrated
   risk score, not just exit prediction.
4. **Provider-fallback router** with sub-second reachability probe and
   immutable audit log of routing decisions — a deployment pattern, not
   only an algorithm.
5. **Reproducible synthetic HR corpus** (5,000 employees, 27 features,
   intervention log) released under permissive licence.

---

## 4. Section skeleton (≈ word counts)

| § | Title | ≈ words |
|---|------|--------|
| 1 | Introduction | 800 |
| 2 | Related Work | 700 |
| 3 | System architecture | 900 |
| 4 | Fairness-as-gate algorithm | 700 |
| 5 | Causal uplift estimator | 700 |
| 6 | Privacy: salted Review_IDs | 500 |
| 7 | Provider-fallback router | 500 |
| 8 | Evaluation | 1200 |
| 9 | Discussion / threats to validity | 500 |
| 10 | Conclusion + ethics statement | 300 |

---

## 5. Eight figures (already produced or trivially produced)

1. System architecture (block diagram) — `docs/images/diagrams/architecture.png`
2. Fairness-gate flow chart — produce in 1 hr (`paper/figures/`)
3. T-learner architecture — produce in 30 min
4. Salted Review_ID sequence diagram — produce in 30 min
5. Provider-fallback state machine — produce in 30 min
6. Executive dashboard screenshot — `docs/images/executive.png`
7. SHAP per-employee surface — `docs/images/shap.png`
8. Fairness audit surface (with one suppressed cohort) — `docs/images/fairness.png`

---

## 6. Four tables

| # | Title | Source |
|---|------|--------|
| T1 | Calibration (ECE, Brier, AUC, AP) on holdout | `production/eval/calibration.json` |
| T2 | Per-arm uplift (Qini, AUUC) vs. correlation baseline | `production/eval/uplift.json` |
| T3 | Fairness audit per protected cohort (DI ratio, gate decision) | `production/eval/fairness.json` |
| T4 | Latency budget (p50/p95) per surface, with and without LLM provider | `production/eval/latency.json` |

(If any of these JSON files are not yet emitted, add a one-line `json.dump`
in the corresponding evaluation script — already structured in
`production/eval/`.)

---

## 7. Related-work narrative (talking points)

- IBM Kenexa, Workday Predictive Attrition — *predict but do not gate, do
  not pseudonymise, do not estimate causal CATE*.
- Fairlearn, AIF360 — *libraries, not deployed systems*; treat fairness as
  audit/post-hoc.
- EconML — *library*; provides T/X/DR-learners but no integration with a
  workforce risk pipeline or fairness gate.
- Microsoft Viva Insights / Glint — *engagement analytics only*; no
  per-employee risk, no recommendation engine.
- Recent FAccT papers on differential privacy in HR (cite 3–5) — *focus on
  training-time DP; we focus on presentation-time pseudonymisation*.

---

## 8. Ethics statement (mandatory at FAccT, recommended elsewhere)

- Synthetic data only — no real employee records used.
- Fairness gate is **blocking**, not advisory — recommendations literally
  cannot reach the reviewer until the gate passes.
- Salted Review_IDs prevent reviewer-side re-identification under
  role-based access.
- All audit decisions logged to an immutable table.
- Code and synthetic dataset open-sourced under MIT.

---

## 9. Reproducibility checklist (NeurIPS-style)

- [x] Code released
- [x] Dataset released (synthetic)
- [x] Random seeds documented
- [x] Hyper-parameters documented
- [x] Hardware spec listed (CPU-only commodity laptop, 16 GB RAM)
- [x] Single-command reproduction (`make repro` planned)

---

## 10. Suggested 6-week paper-drafting calendar

| Week | Deliverable |
|------|-------------|
| 1 | §3 architecture, §4 fairness gate, §6 privacy — drafts |
| 2 | §5 causal estimator, §7 provider fallback — drafts |
| 3 | §8 evaluation — emit all 4 JSON tables, render 8 figures |
| 4 | §1 intro, §2 related work, §9 discussion — drafts |
| 5 | Co-author / advisor review pass; reduce to page budget |
| 6 | Final polish, references, ethics statement, submit |
