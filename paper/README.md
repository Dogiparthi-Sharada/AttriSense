<!--
AttriSense — paper/README.md
Author : Sharada Dogiparthi <dogiparthi.sharada@gmail.com>
Version: 1.0.0
Date   : 2026-05-07
License: MIT — see LICENSE in repo root.
Copyright (c) 2026 Sharada Dogiparthi. All rights reserved.
-->

# 📄 AttriSense — IEEE Paper, Venues, Patent Path, and Coordinated Launch Plan

This folder contains a draft IEEE-format conference paper plus the full
strategy for turning the AttriSense project into:

1. A peer-reviewed IEEE publication
2. A provisional US patent (optional, but worth pursuing)
3. A coordinated LinkedIn launch that maximizes job-search visibility

---

## 1. The Paper Draft

**File:** [`attrisense_ieee.tex`](attrisense_ieee.tex)

It’s written in the official **IEEEtran** conference template
(two-column, the format every IEEE conference accepts).

### How to compile

**Easiest — Overleaf (recommended):**
1. Go to https://overleaf.com → New Project → Upload Project
2. Drag `attrisense_ieee.tex` in
3. Click **Recompile**. Done.

**Locally (if TeX Live installed):**
```bash
cd paper
pdflatex attrisense_ieee.tex
pdflatex attrisense_ieee.tex   # second pass for refs
```

You will see a 6–8 page PDF that reads like a real IEEE submission.

### What still needs human polish before submission

- [ ] Add **Sharada’s real ORCID** to the author block.
- [ ] Replace `[Faculty Co-Author --- TBD]` with an actual CSUEB MSBA
      faculty co-author. *Talk to your capstone advisor first* —
      faculty co-authorship dramatically increases acceptance odds and
      gives you institutional cover for IRB / ethics later.
- [ ] Add the architecture diagram (Section IV references Fig.~1 but
      it’s omitted). Use Excalidraw or Mermaid → export PNG → drop in
      with `\includegraphics`.
- [ ] Re-run all numbers in the Evaluation section against your *actual*
      trained model. The numbers in the draft are illustrative
      placeholders calibrated to typical HR-attrition outcomes — they
      need to be your real measurements.
- [ ] Run the fairness audit on real `fairlearn` output.
- [ ] Get the manager-trust pilot survey (n=12) actually executed —
      even informally with classmates. The Wilcoxon p-value must be
      real, not illustrative.

---

## 2. Where to Submit — Conference & Journal Targets

Ranked by realistic acceptance probability for an MSBA-student paper
with strong applied work but no novel ML theory.

### 🟢 Tier A — High probability of acceptance (target these first)

| Venue | Type | Why it fits |
|---|---|---|
| **IEEE Big Data — Industry & Government Track** | Conf | Accepts applied data-science systems; shorter review cycle; high prestige |
| **IEEE International Conference on Data Mining (ICDM) — Workshops** | Conf workshop | Workshops on Data Mining for HR / People Analytics accept student papers |
| **IEEE International Conference on Big Data Analytics (ICBDA)** | Conf | Applied analytics focus; reasonable acceptance rate |
| **ACM SIGKDD — Applied Data Science Track / Workshops** | Conf | The KDD Workshop on ML for HR accepts applied work |
| **IEEE Conference on Business Informatics (CBI)** | Conf | Explicit business-analytics scope; MSBA-friendly |
| **IEEE International Conference on AI in HR / WCCI workshops** | Conf | New venues, hungry for submissions |
| **INFORMS Journal on Applied Analytics** (formerly *Interfaces*) | Journal | Loves business-impact case studies with ROI math |

### 🟡 Tier B — Stretch, but worth the upside

| Venue | Why |
|---|---|
| **IEEE Transactions on Computational Social Systems** | Direct fit for HR/social applications |
| **IEEE Access** (open access, fast review) | High acceptance, indexed everywhere |
| **CHI Late-Breaking Work** | If you reframe around the manager-trust pilot study (HCI angle) |

### 🔵 Tier C — Always do these in parallel (free, fast, citable)

| Venue | Why |
|---|---|
| **arXiv (cs.LG / cs.HC)** | Citable in 24 hours, indexed by Google Scholar. *Do this first.* |
| **SSRN (Business / Information Systems eJournal)** | Same idea, business-school audience |
| **Towards Data Science / Medium** | Drives traffic to the repo |

### ✅ Recommended sequence

1. **Week 1:** Submit to **arXiv** as `[cs.LG]` preprint. Add the arXiv badge to the README. *You are now a “published author”* — you can put “arXiv preprint, 2025” on your resume immediately.
2. **Week 2:** Cross-post on **SSRN** (business audience).
3. **Week 3:** Submit to **IEEE Big Data Industry Track** (or the next open IEEE venue with a near-term deadline — check `wikicfp.com`).
4. **Month 2–3:** Polish for **INFORMS Journal on Applied Analytics**. This is the highest-value MSBA-relevant journal and is *very* friendly to applied work with real business framing.

---

## 3. AI-Assisted Code — Is It OK to Publish?

**Yes — if you disclose it properly.** This is now standard practice, not a red flag.

### What major venues require (as of 2026)

- **ACM, IEEE, NeurIPS, ICLR, KDD** all explicitly *permit* AI-assisted writing and coding, *provided*:
  1. The author takes full responsibility for correctness.
  2. The use is disclosed in the Acknowledgments section.
  3. The AI is not listed as a co-author (it can’t consent to the publication agreement).
- **arXiv** has no AI restriction at all.
- **Most journals** now require an "AI Use Disclosure" paragraph.

### What to actually write (already in the draft)

The paper’s Acknowledgments and Methodology sections already include:

> *“The codebase was developed collaboratively with LLM coding
> assistants (GitHub Copilot, Claude~3.7, GPT-4); the use of AI
> assistants is explicitly documented in the project repository's
> `AI_CONTRIBUTIONS.md`, in line with emerging norms for reproducible
> AI-assisted research.”*

### Action item

Create a short `AI_CONTRIBUTIONS.md` in the repo root saying:
- Which AI tools were used (Copilot, Claude, GPT-4)
- For what purposes (boilerplate code, debugging, doc strings, this paper draft)
- That all output was human-reviewed before commit
- That the author takes full responsibility for correctness

This single file moves you from “might look sketchy” to “gold-standard transparency.”

---

## 4. Patent Path — Is It Patentable, and How to Start

### Honest assessment

The *individual algorithms* (Random Forest, SHAP, FAISS, RAG, NL2SQL) are
**prior art** and are not patentable on their own. But specific
**system-level workflows** that combine them in non-obvious ways
absolutely are — IBM, Workday, Eightfold, and Visier all hold dozens of
HR-analytics method patents on exactly this kind of combination.

### Three credible patent angles for AttriSense

1. **“System and method for explainable employee flight-risk scoring
   augmented by retrieval over qualitative exit-interview corpora.”**
   *Novelty hook:* dynamically grounding a tabular ML risk score in
   semantically retrieved free-text precedent to produce a
   manager-facing rationale.

2. **“Causal-uplift-driven personalized retention intervention
   recommendation.”**
   *Novelty hook:* selecting the intervention (raise, promotion,
   transfer, mentorship) that maximally reduces predicted flight risk,
   conditional on per-employee SHAP attribution.

3. **“Time-decayed risk-acceleration alerting in HR analytics.”**
   *Novelty hook:* alerting on the *second derivative* (acceleration) of
   risk rather than absolute level — a technique borrowed from credit-risk.

### How to actually start (cheapest legal path for a student)

#### Option A — Provisional patent via CSUEB Tech Transfer (recommended)

1. **Talk to the CSUEB Office of Research and Sponsored Programs.**
   Most universities have a Tech Transfer / Innovation office that
   helps students file provisional patents on inventions developed
   during coursework. They often **co-file and cover legal fees**
   in exchange for a small share of any future commercial revenue.
2. **Request an Invention Disclosure Form (IDF).** This is a 2–4 page
   form describing what you built and why it’s novel.
3. **The university decides** within 30–60 days whether to file. If
   they pass, you keep all rights and can file independently.

#### Option B — File a provisional yourself

1. **USPTO Provisional Patent Application** — micro-entity fee is
   ~$130 (https://www.uspto.gov).
2. **What you need:** a written description (the paper draft is 80%
   of what’s required), drawings (the architecture diagram), and the
   filing form.
3. **What you get:** 12 months of “patent pending” status while you
   decide whether to file a full non-provisional. *This is the cheapest
   legitimate IP signal you can put on a resume or LinkedIn.*

#### Option C — Defensive publication

If you don’t want to patent but want to *prevent others from
patenting against you*, publish on **IP.com Prior Art Database** or
just put the arXiv preprint on record. This establishes prior art for
free.

### ⚠️ Critical sequencing — read this twice

> **Public disclosure (LinkedIn post, arXiv preprint, GitHub README)
> immediately destroys novelty in most international jurisdictions
> and starts a 12-month clock in the United States.**

This means:

- If you file the **provisional patent FIRST** → you preserve full
  international rights and have 12 months to write the full paper and
  post on LinkedIn. **Recommended path if patents are real.**
- If you publish on LinkedIn / arXiv FIRST → you lose international
  rights and have 12 months to file a US provisional. **Acceptable
  for a portfolio project where the goal is jobs, not licensing.**

For Sharada specifically: **the goal is a job, not a billion-dollar
exit.** I recommend the LinkedIn-first path unless CSUEB Tech Transfer
moves quickly enough to file in 1–2 weeks.

---

## 5. Coordinated Launch Plan — Paper + Patent + LinkedIn Post

This is the sequence that maximizes job-search visibility while
protecting IP optionality.

### Week 1 (this week)

- [ ] **Day 1:** Email CSUEB Tech Transfer Office. Subject:
      *“MSBA student inventor — request for invention disclosure
      consultation.”* Attach the README and the paper draft.
- [ ] **Day 2:** Polish paper numbers with real model output.
- [ ] **Day 3:** Generate the architecture diagram (Excalidraw).
- [ ] **Day 4:** Create `AI_CONTRIBUTIONS.md` in repo root.
- [ ] **Day 5:** Submit paper to **arXiv**.
- [ ] **Day 5:** While arXiv is processing, **wait 24h** before
      LinkedIn post — gives Tech Transfer Office a window to react.

### Week 2

- [ ] **Tuesday 8:30 AM PT:** Post on LinkedIn (use the final-cut from
      `LINKEDIN_POST.md`). Include arXiv link in first comment.
- [ ] **Tuesday + 4hr:** Post the “update” comment.
- [ ] **Wednesday:** DM the Lumentum recruiter with the post link.
- [ ] **Thursday:** Cross-post on SSRN.
- [ ] **Friday:** Cross-post on Towards Data Science.

### Week 3–4

- [ ] Submit to IEEE Big Data Industry Track (or next open CFP).
- [ ] Build out SHAP + fairness audit code (paper v2 fodder).
- [ ] Schedule LinkedIn carousel post for week 4.

### Month 2–3

- [ ] If CSUEB Tech Transfer files a provisional → add
      “🪪 Patent Pending” badge to the README + LinkedIn headline.
- [ ] Prepare INFORMS Journal of Applied Analytics submission.
- [ ] If accepted at IEEE → schedule conference travel and another
      LinkedIn post: *“Presenting AttriSense at IEEE Big Data — see you
      in [city].”*

---

## 6. The LinkedIn-Specific Strategy When You Have a Paper + Patent

This is what separates a normal portfolio post from a *signal-rich*
candidate post that hiring managers screenshot and forward.

### Headline upgrade

Change LinkedIn headline to:
> *“MSBA @ CSUEB | Building AttriSense — IEEE-published, Patent-Pending Workforce Intelligence Platform | Open to AI/ML Roles”*

Even *“IEEE-submitted”* and *“provisional patent in progress”* are
accurate and powerful.

### Featured section — pin all four

1. GitHub repo
2. Live Streamlit demo
3. arXiv paper PDF
4. 60-second demo video

### The 3-post launch sequence on LinkedIn

| Post | Timing | Hook |
|---|---|---|
| **#1 — Project + Paper** | Tue Week 2 | *“Three weeks ago Lumentum opened an interview door — so I rebuilt my MSBA project for them, shipped it as AttriSense, and submitted the paper to arXiv this week.”* |
| **#2 — Carousel: Architecture Deep-Dive** | Tue Week 3 | 6 Canva slides walking through the architecture. Drives a different audience (tech leads who don’t read paragraphs). |
| **#3 — Patent + Lessons Learned** | Tue Week 4 (only if patent filed) | *“Update: CSUEB Tech Transfer agreed to file a provisional patent on the SHAP+RAG retention-rationale workflow. Here’s what I learned about turning a class project into IP.”* This post **almost always goes viral** because most students don’t know patents are even possible. |

### Why this works for hiring

A recruiter who sees:
- ✅ Public GitHub repo
- ✅ Live demo
- ✅ arXiv paper
- ✅ Patent pending
- ✅ Three thoughtful LinkedIn posts in three weeks
- ✅ Genuine “thank you Lumentum” framing

…is not screening her against other candidates. They’re fast-tracking
her to the hiring manager. This is what *“built like a founder”*
looks like on a resume.

---

## 7. One-Page TL;DR for Sharada

1. The paper draft is in `attrisense_ieee.tex`. Compile on Overleaf.
2. Submit to **arXiv** first (24h, free, citable). Then IEEE Big Data
   Industry Track or INFORMS Journal of Applied Analytics.
3. **AI-assisted code is fine** — disclose it in `AI_CONTRIBUTIONS.md`
   and the paper Acknowledgments. This is now standard.
4. **Patent is feasible** for the SHAP+RAG retention-rationale
   combination. Email CSUEB Tech Transfer this week.
5. **Sequencing matters:** if pursuing the patent, file provisional
   *before* LinkedIn. Otherwise LinkedIn first, US-only patent rights.
6. **Headline upgrade after publication:** *“MSBA @ CSUEB | Building
   AttriSense — IEEE-Published, Patent-Pending”* — that single line
   converts more interviews than any other change.

You’ve got this. 🚀
