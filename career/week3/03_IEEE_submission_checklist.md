# IEEE Big Data 2026 — Industry Track Submission Checklist

> **Target:** IEEE Big Data 2026 — Industry, Government & Healthcare
> Applications Track. **Why:** the Industry Track values *deployed
> systems* and *production lessons* over novel algorithms — exactly
> the AttriSense story.
>
> **Submit:** Monday May 25 (after this week's polish pass).

---

## Submission package

| ☐ | Item | Where | Status |
|---|------|-------|--------|
| ☐ | `paper/attrisense_ieee.pdf` (7 pp, IEEEtran) | Repo | ✅ Built |
| ☐ | Cover letter (1 pg) | `paper/cover_letter.md` | Draft below |
| ☐ | Author block — Sharada Dogiparthi, MSBA, CSUEB | Page 1 of paper | ✅ |
| ☐ | ORCID ID | https://orcid.org/ | ☐ Register if missing |
| ☐ | Affiliation: California State University, East Bay | Page 1 of paper | ✅ |
| ☐ | 250-word abstract | Paper §Abstract | ✅ |
| ☐ | 5 keywords | Paper §Keywords | ✅ |
| ☐ | IEEE copyright form | Conference portal | ☐ |
| ☐ | Conflict of interest declaration | Conference portal | ☐ |
| ☐ | Submission portal URL | https://bigdataieee.org/BigData2026/ | ☐ Verify |

---

## Cover letter (drop into `paper/cover_letter.md`)

> Dear Industry Track Program Chairs,
>
> I am submitting *"AttriSense: A Five-Modality Open-Source Workforce
> Intelligence Platform with Production Hardening and Fairness
> Gating"* for consideration in the Industry, Government & Healthcare
> Applications Track at IEEE Big Data 2026.
>
> The submission contributes three things to the Industry Track
> conversation:
>
> 1. **A deployable architecture pattern** combining five model
>    modalities — RandomForest+SMOTE classification, Cox
>    proportional-hazards survival, EconML T-Learner causal uplift,
>    multilingual retrieval-augmented generation with provider
>    fallback, and a TF-IDF-safety-netted natural-language SQL
>    interface — into a single dashboard with reproducible synthetic
>    benchmarks (ROC-AUC 0.91, PR-AUC 0.74, Cox concordance 0.78).
>
> 2. **Three production-hardening lessons** that the academic
>    literature underweights: SMOTE-after-split, third-party
>    endpoint resilience via reachability-probed provider fallback,
>    and identification-bias mitigation through salted-hash
>    pseudonymization at the rendering layer.
>
> 3. **An EEOC four-fifths fairness gate** as a *blocking* check
>    rather than a post-hoc audit, with a per-department disparate-
>    impact table for reproducibility.
>
> The system is MIT-licensed at https://github.com/Dogiparthi-Sharada/attrisense
> with a live demo at https://attrisense.streamlit.app, deterministic
> synthetic-data benchmarks, and a 79-page beginner's-guide
> companion document for practitioner adoption.
>
> Reviewers may run the full pipeline in under five minutes via
> `make train && streamlit run production/streamlit_app.py`. All
> tables, the algorithm, and Figure 1 are reproducible from
> `seed=42`.
>
> Thank you for your consideration.
>
> Sincerely,
> Sharada Dogiparthi
> MSBA Candidate, California State University, East Bay
> [email · ORCID · LinkedIn]

---

## Last-mile polish (do this Sunday May 24)

1. ☐ Paper renders cleanly with `pdflatex -shell-escape paper/attrisense_ieee.tex` — no overfull hboxes flagged.
2. ☐ All four tables (perf, ablation, CATE, fairness) numbered and referenced in the body.
3. ☐ Figure 1 (architecture) has a legend matching the Pixel pastel palette.
4. ☐ Algorithm 1 (provider fallback) typeset with `algorithmic` package.
5. ☐ References pass `bibtex` clean — 25 refs, all with DOIs or stable URLs.
6. ☐ Page count = 7 (8 with refs is also fine for IEEEtran two-column).
7. ☐ Anonymisation: Industry Track is **not** double-blind by default — leave the author block in. Confirm on the conference page.

---

## After submission

- **arXiv mirror.** Upload the same PDF to arXiv (cs.LG, secondary
  cs.CY for fairness). arXiv ID lands in 1–2 business days, then
  add the badge to the README banner.
- **SSRN mirror.** Industry / management track. Drives different
  traffic than arXiv.
- **Add to LinkedIn:** *"📄 Submitted AttriSense to IEEE Big Data
  2026 (Industry Track) today. Preprint on arXiv this week."*
  This is its own tiny LinkedIn moment — schedule for ≈ 9 AM on the
  day arXiv goes live.
