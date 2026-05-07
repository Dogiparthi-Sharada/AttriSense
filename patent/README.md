# AttriSense — Patent, Publication & Career Collateral

This directory contains the strategic IP, publication, and career-marketing
collateral for the **AttriSense** project. Use it as the single source of truth
when:

- pitching the work to a patent attorney or USPTO Track One filing
- submitting to IEEE / ACM venues
- packaging a capstone deliverable for university / portfolio
- targeting FAANG / FAANG-adjacent ML / Applied-Scientist / Data-Scientist roles

| File | Purpose | Audience |
|------|---------|----------|
| [`01_patent_strategy.md`](01_patent_strategy.md) | 7 defensible claims + prior-art delta + provisional-vs-utility decision tree | Patent attorney, IP counsel, founder |
| [`02_provisional_application_draft.md`](02_provisional_application_draft.md) | Drop-in skeleton for a USPTO provisional (Title, Field, Background, Summary, Detailed Description, Claims, Abstract) | Self-file / attorney-file |
| [`03_research_paper_outline.md`](03_research_paper_outline.md) | IEEE-format paper outline with target venues, novelty positioning, 8 figures, 4 tables, contributions list | Conference / journal submission |
| [`04_capstone_report.md`](04_capstone_report.md) | 12-section academic capstone aligned to ABET / typical CS-MS rubric | University capstone, portfolio jury |
| [`05_faang_marketing_playbook.md`](05_faang_marketing_playbook.md) | 30-day plan to convert AttriSense into FAANG offers — resume bullets, behavioural-interview STARs, system-design talking points, tailored target-company hooks | Job seeker |
| [`06_one_pager_external.md`](06_one_pager_external.md) | Public-safe one-pager (no IP-sensitive language) for LinkedIn / portfolio site / recruiter outreach | Recruiters, hiring managers |
| [`07_demo_script.md`](07_demo_script.md) | 7-minute live-demo runbook with timing cues for VP / interview / patent disclosure meetings | Presenter |
| [`08_publication_target_matrix.csv`](08_publication_target_matrix.csv) | Ranked venue list (IEEE BigData, ICDM, KDD ADS, FAccT, CHI, ACL, NAACL) with deadlines + acceptance rates + fit score | Author |
| [`09_FAQ.md`](09_FAQ.md) | Defensive Q&A for patent reviewers, peer reviewers, and FAANG interviewers | Author |

## How to use this directory

1. **Patent first** — read `01_patent_strategy.md`, then drop your inventor
   details into `02_provisional_application_draft.md` and file the provisional.
   You then have **12 months** to convert to a utility.

2. **Paper next** — `03_research_paper_outline.md` references the same
   experiments as the codebase, so the paper can be drafted directly from the
   `paper/` and `production/` directories without new experiments.

3. **Capstone in parallel** — `04_capstone_report.md` is structured for an
   academic committee; it doubles as the long-form artefact you upload to the
   portfolio site referenced from the resume bullets in
   `05_faang_marketing_playbook.md`.

4. **Marketing on a 30-day cadence** — follow the playbook week-by-week. The
   one-pager and demo script are the assets you actually share externally.

## Status (2026-05-07)

- Provisional draft: ready for inventor signature
- Paper outline: experiments already run in `production/` — draft 0 in 2 weeks
- Capstone: aligned to current code; ready for committee submission
- FAANG marketing: 30-day calendar starts the day this directory is committed
