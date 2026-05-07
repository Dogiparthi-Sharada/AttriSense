# Career Playbook — v2 (refreshed May 7, 2026)

> **Origin.** Forked from `archive/legacy/career/` on **May 7, 2026**.
> The archive is preserved untouched.
>
> **Why v2.** The Week 1–4 plan was written when AttriSense was a
> 3-modality system (RandomForest + RAG + NL→SQL). The repo has since
> grown into a **5-modality** platform with Pixel-pastel UI, salted
> Review_ID pseudonymization, RAG provider fallback, a 7-page IEEE-style
> conference PDF, an offline beginner's guide DOCX, and an Engineering-VP
> pitch deck. Every outward-facing artefact (LinkedIn post, Twitter
> thread, video script, resume bullets, carousel spec, vulnerability post,
> month-in-review post) has been rewritten so the story matches the code.

---

## What changed in the repo since v1

| Area | v1 (archive) | v2 (now) |
|------|--------------|----------|
| Models | RandomForest + SMOTE | **+ Cox PH (lifelines) · + T-Learner (EconML)** |
| RAG | OpenAI embeddings + FAISS | **+ Hashing fallback · DNS/TCP/HTTPS reachability probe · per-provider FAISS dirs** |
| NL→SQL | LangChain + GPT only | **+ TF-IDF gold-question fallback** (50-question gold set) |
| Identity bias | Emp_ID shown verbatim | **Review_ID = SHA-256(salt ‖ Emp_ID)[:6] → `RV-NNNNNN`** (env-salt rotatable) |
| UI | Dark slate | **Pixel pastel — cream canvas, lavender/peach/sage accents, dark axes for chart legibility** |
| Paper | LaTeX draft, no PDF | **7-page IEEE PDF compiled, Fig 1 + Tables I–IV + Algorithm 1 + 25 refs** |
| Docs | mkdocs (loose) | **mkdocs --strict passes · 7-second build · 0 warnings** |
| Beginner's guide | Tossed-off DOCX | **Cover + Word TOC + 8 chapters + ASCII diagrams + Pixel diagrams (~79 pages)** |
| Pitch deck | none | **`outputs/AttriSense_VP_Pitch.pptx` — 15 slides + speaker notes (Engineering VP audience)** |

---

## North Star (unchanged from v1)

By end of Week 4 you have:

1. ✅ Crushed the interview (Day 0 — already done).
2. ✅ Public live demo at `https://attrisense.streamlit.app`.
3. ✅ Repo branded "AttriSense" — banner, badges, screenshots.
4. ✅ 60–75 sec demo video posted natively to LinkedIn.
5. ✅ arXiv / SSRN preprint published.
6. ✅ Faculty + CSUEB Tech Transfer outreach sent.
7. ✅ LinkedIn launch post (Tue May 12) → carousel (Tue May 19) → vulnerability post → month-in-review.
8. ✅ Pipeline tracker with ≥ 1 conversation that converts to a "next step."

---

## Calendar (preserved from v1 — campaign anchors haven't moved)

| Week | Dates | Theme | Anchor day |
|------|-------|-------|------------|
| Week 1 | May 2 – May 8 (Sat–Fri) | Polish & disclosure | Day 0 = Fri May 1 (interview) |
| Week 2 | May 11 – May 17 | Launch | **Tue May 12 — LinkedIn launch** |
| Week 3 | May 18 – May 24 | Compound | **Tue May 19 — architecture carousel** |
| Week 4 | May 25 – May 31 | Convergence | Tue May 27 — month-in-review |

---

## Folder layout

```
career/
├── README.md                          ← this file
├── week1/   Polish & disclosure
│   ├── README.md
│   ├── 01_AI_CONTRIBUTIONS.md         ← drop into repo root
│   ├── 02_README_banner_snippet.md    ← drop into top of README.md
│   ├── 03_video_script_75s.md         ← refreshed for 5 modalities
│   ├── 04_resume_bullets.md           ← Cox PH, fairness, Review_ID highlighted
│   ├── 05_interview_pitch_90s.md      ← out-loud pitch
│   └── 06_thank_you_email.md
├── week2/   Launch
│   ├── README.md
│   ├── 01_linkedin_launch_post.md     ← THE launch post
│   ├── 02_twitter_thread_10t.md       ← X thread
│   ├── 03_cold_dm_templates.md        ← 5 templates
│   ├── 04_engagement_response_bank.md
│   └── 05_pipeline_tracker.md
├── week3/   Compound
│   ├── README.md
│   ├── 01_carousel_8slides.md         ← architecture carousel
│   ├── 02_vulnerability_post.md       ← "3 things I got wrong"
│   ├── 03_IEEE_submission_checklist.md
│   └── 04_recruiter_2nd_touch.md
└── week4/   Convergence
    ├── README.md
    ├── 01_offer_negotiation_playbook.md
    ├── 02_meetup_talk_proposal.md
    ├── 03_month_in_review_post.md     ← closing-the-loop post
    ├── 04_provisional_patent_guide.md
    └── 05_90_day_roadmap.md
```
