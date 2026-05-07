<!--
AttriSense — career/week4/05_90_day_roadmap.md
Author : Sharada Dogiparthi <dogiparthi.sharada@gmail.com>
Version: 1.0.0
Date   : 2026-05-07
License: MIT — see LICENSE in repo root.
Copyright (c) 2026 Sharada Dogiparthi. All rights reserved.
-->

# 90-Day Roadmap — June 1 → August 30, 2026

> **Purpose:** publish a 90-day forward plan in the repo as a public
> commitment device. **Why public:** every recruiter who clicks
> through to it sees concrete next moves, which is leverage in
> conversations and a magnet for inbound on the parts you're
> explicitly working on.

---

## Drop into `ROADMAP.md` at the repo root

```markdown
# AttriSense — 90-Day Roadmap (June 1 – August 30, 2026)

*Maintained by Sharada Dogiparthi. Last updated: May 31, 2026.*

This document is a public commitment to where AttriSense is going
over the next 90 days. Updated weekly. PRs welcome.

## Theme: from synthetic to deployed

The first 90 days of AttriSense were about *building the substrate*.
The next 90 are about *putting it under load*: real data, on-prem
fallback, fairness audit at scale, and the first paying or
not-paying pilot.

## Three pillars

### 1. Real-data pilot — partner with one HR team

- ☐ **Week 1–2 (June 1–14)** — 5 outbound conversations with HR
  teams (start-ups, mid-market). Goal: 1 partner signed for a
  6-week sandbox pilot under NDA.
- ☐ **Week 3–6 (June 15 – July 12)** — Run the pilot. Connect
  AttriSense to the partner's HRIS extract (Workday / BambooHR /
  ADP). Salt rotated. Fairness audit on partner's protected-class
  proportions. Weekly feedback session.
- ☐ **Week 7–8 (July 13–26)** — Pilot retro. Public case study (with
  approval) with anonymised metrics.
- ☐ **Week 9–10 (July 27 – Aug 9)** — Apply pilot lessons to v2 of
  the synthetic data generator (better realism on tenure
  distributions and hiring-cohort effects).

### 2. On-prem provider fallback — beyond OpenAI + hashing

- ☐ **June** — Add **AWS Bedrock** as a primary provider option
  (Anthropic Claude embeddings + Titan as fallback). Same
  reachability-probe pattern, same per-provider FAISS dirs.
- ☐ **July** — Add **Azure OpenAI** as a third option (the most
  common enterprise IT-approved path).
- ☐ **August** — Add **Ollama** as a fully-local primary option for
  air-gapped environments. Document the cost/latency trade-offs in
  `docs/providers.md`.

### 3. Fairness audit at scale

- ☐ **June** — Move the EEOC four-fifths gate from per-batch to
  per-record streaming. Document the latency cost.
- ☐ **July** — Add an **intersectional** fairness audit (not just
  one protected class at a time). Reference: Buolamwini & Gebru's
  intersectional Gender Shades framing.
- ☐ **August** — Stress-test on a **50k-employee synthetic corpus**
  (10× current). Profile + memo + paper-quality fairness audit
  table for the eventual journal version.

## Smaller items

- ☐ Public NYC Local Law 144-style bias-audit report template.
- ☐ Streamlit Cloud → Hugging Face Spaces mirror (fewer cold starts).
- ☐ EU AI Act high-risk-system documentation template.
- ☐ Conference talk delivered at PyData / WIA / ODSC.
- ☐ IEEE Big Data 2026 acceptance / camera-ready / arXiv v2.
- ☐ Beginner's guide → second edition with pilot lessons.

## Stretch (October+)

- ☐ Ship a `pip install attrisense` package. CLI + Python API.
- ☐ Multi-tenant pilot — two HR teams running side-by-side.
- ☐ Cox PH → DeepSurv upgrade for non-linear hazard.
- ☐ Causal arm catalogue beyond the current three.

## How I track this

- `docs/roadmap_log.md` — weekly bullets, what shipped, what slipped.
- `outputs/roadmap_metrics.csv` — KPIs that matter at 90-day cadence.
- A pinned issue per pillar; comments welcome from the community.

## How to help

- 🛠️ **Engineers**: PRs against `production/src/attrisense/providers/`
  for new fallback options.
- 📊 **HR practitioners**: real-anonymised case studies of attrition
  drivers we should be modelling but aren't (`issues/practitioner-input`).
- 📜 **Legal / compliance**: review the EU AI Act + NYC LL 144
  templates and call out gaps.
- 🎤 **Speakers**: if you run a meetup that wants the talk, open an
  issue with the title `talk: <event>`.

## License

MIT. Same as the rest of the project. The roadmap is a soft
commitment — not a contract — and may shift as pilot lessons land.
```

---

## After publishing

1. **Link from the README banner** under "What's next."
2. **One LinkedIn post** the day it lands: *"📍 90-day forward
   roadmap for AttriSense is now public — partner pilot, on-prem
   fallback, fairness at scale. Repo link in comments. Always
   open to feedback and PRs."*
3. **Send to the 5 people who helped most** (the names that ended
   up in the README acknowledgements). One-line DM:
   *"90-day plan is up — your input went into pillar [N]. Thank you."*

---

## Thank-you list (Sun May 31)

Make a list of **5 people** who genuinely moved the campaign.
Send a *personalised, specific, link-light* note to each.

| # | Name | What they did | Note sent? |
|---|------|---------------|------------|
| 1 |  |  | ☐ |
| 2 |  |  | ☐ |
| 3 |  |  | ☐ |
| 4 |  |  | ☐ |
| 5 |  |  | ☐ |

The note should reference one *specific* thing they said or did.
Generic "thank you for your support" notes do not land. *"Your
SMOTE-before-split call-out on May 14 became the lead anecdote in
the vulnerability post — thank you"* lands.
