# Provisional Patent Decision Guide

> **Purpose:** decide whether to file a US provisional patent on any
> AttriSense subsystem **before** signing an offer that contains a
> broad IP-assignment clause. Document the decision either way —
> the documentation itself is leverage.
>
> ⚠️ **This is not legal advice.** Talk to a real patent attorney
> before filing. CSUEB Tech Transfer Office can refer one.

---

## Decision tree

```
Is AttriSense MIT-licensed and publicly visible?           ── YES (May 2026)
        │
        ▼
Is anything in it genuinely novel + non-obvious + useful?  ── ?
        │  (most "novel" student projects are NOT patent-novel; that's OK)
        ▼
Could a competitor read the public repo and replicate?     ── YES (it's MIT)
        │
        ▼
Is the value in the *implementation* or the *idea*?
        │
        ▼ Implementation                ▼ Idea
   File defensive publication      Consider provisional
   (lock prior art, $0)            ($75–$3,500, 12 mo. window)
```

For most parts of AttriSense the right answer is **defensive
publication**, not provisional patent. The IEEE paper + arXiv
preprint already serve as prior art and lock the date.

---

## Candidates — what *might* be patentable

| Subsystem | Patent-novel? | Action |
|-----------|---------------|--------|
| RandomForest + SMOTE retention model | No — well-known | None |
| Cox PH on HR data | No — known application | None |
| EconML T-Learner for retention interventions | Maybe — novel *application* of known method | Defensive publication |
| **Reachability-probed RAG provider fallback with per-provider FAISS dirs** | Possibly — implementation detail is non-obvious | **Consult attorney** |
| **Salted-hash Review_ID rendering layer for identification-bias mitigation** | Possibly — pseudonymisation at the rendering layer (not storage) is unusual | **Consult attorney** |
| EEOC four-fifths fairness gate as *blocking* check | No — known compliance pattern | None |
| NL→SQL with TF-IDF gold-question fallback | No — known fallback pattern | None |
| Five-modality dashboard composition | No — composition of known parts | None |

**Two candidates** rise to "consult an attorney": the RAG
provider-fallback design and the Review_ID rendering pattern. The
others are firmly prior-art territory.

---

## If you decide to file

- **Provisional only.** $75 micro-entity, $150 small-entity. 12
  months to convert to a full utility patent (much more $$).
- **Inventor:** you (Sharada Dogiparthi).
- **Assignee:** can be you personally OR CSUEB if Tech Transfer is
  involved. Tech Transfer split: ask the office *before* filing.
- **Disclosure:** you must file *within 12 months* of public
  disclosure (the May 12 launch is the disclosure date). Don't
  miss this window.

## If you decide NOT to file (most likely)

- **Document the decision** in `paper/patent_decision.md` with the
  date, the reason, and a link to the IEEE paper as prior art.
- **Defensive publication** is automatic once the arXiv preprint
  goes live. Save the arXiv URL.
- **In offer negotiations**, flag the documentation when reviewing
  the IP-assignment clause: *"I've made a documented decision not
  to pursue patent protection on AttriSense. The system is
  MIT-licensed and disclosed via arXiv. I'd like a written
  carve-out in the offer letter confirming AttriSense is excluded
  from IP assignment."*

---

## Whatever you decide, by Sat May 30:

- ☐ Decision documented (file path: `paper/patent_decision.md`)
- ☐ CSUEB Tech Transfer informed (one email, even if "I've decided
  not to file — here's why")
- ☐ arXiv preprint live and linked (the prior-art lock)
- ☐ MIT licence file present and current in the repo
- ☐ Carve-out language ready for offer-letter negotiation

---

## Why this matters even if you don't file

A documented patent decision is **leverage in negotiation.** It
shows the recruiter and hiring manager that:

1. You take IP seriously.
2. AttriSense is *yours*, with prior-art lock-in via arXiv.
3. The carve-out you're asking for in the offer letter is principled,
   not greedy.

Most offer letters have IP-assignment clauses broad enough to sweep
in personal projects. Don't sign one without reading it. Don't
sign one with AttriSense in scope without a written carve-out.
