# 🗓️ Week 1 — Day-by-Day Execution Plan

> **Today is Friday, May 1, 2026.** Interview at 11:00 AM PST.
> This plan starts AFTER the interview, picking up Saturday morning.
> Every step is small enough to do in one sitting.

---

## ✅ Day 0 — TODAY (Friday, May 1) — INTERVIEW DAY

**Only one priority today: nail the interview.**

- [ ] **Now (8:15 AM PST):** Read [`00_INTERVIEW_PLAYBOOK_TODAY.md`](00_INTERVIEW_PLAYBOOK_TODAY.md) once
- [ ] **8:30–9:30:** Practice 90-second pitch out loud 5 times. Then eat breakfast. Don't touch the codebase.
- [ ] **9:30–10:30:** Quick re-read of the project code (just `predictive_engine.py`, `rag_engine.py`, `ai_sql_constructor.py`). Don't add features.
- [ ] **10:45:** Open the meeting link, test camera/mic
- [ ] **10:55:** Join the call. Smile. Breathe.
- [ ] **11:00–11:45ish:** Interview
- [ ] **Right after:** Send a thank-you email within 60 minutes (template in `06_thank_you_email_template.md`)
- [ ] **Friday evening:** Rest. Don't post on LinkedIn yet. Don't deploy anything. Just rest.

---

## Day 1 — Saturday, May 2 — Polish & Disclosure Hygiene

**Goal:** Repo looks professional, AI use is documented, synthetic-data caveat is loud.

- [ ] **Morning (1 hr):** Add `AI_CONTRIBUTIONS.md` to repo root (template in `01_AI_CONTRIBUTIONS_template.md`)
- [ ] **Morning (1 hr):** Add the synthetic-data banner to top of README (template in `02_README_banner_snippet.md`)
- [ ] **Afternoon (2 hr):** Generate the architecture diagram in Excalidraw (link below)
- [ ] **Afternoon (1 hr):** Add the 5-minute "How a hiring manager can evaluate this" section to README

**Deliverable:** Push commit titled *"docs: AI contributions disclosure + synthetic-data banner + architecture diagram"*.

---

## Day 2 — Sunday, May 3 — Live Demo Deployment

**Goal:** Recruiters do not clone repos. They click links. Make the link work.

- [ ] **Morning (1 hr):** Sign up for Streamlit Community Cloud (free) → https://streamlit.io/cloud
- [ ] **Morning (1 hr):** Set OpenAI key as a secret in Streamlit Cloud
- [ ] **Afternoon (2 hr):** Deploy the dashboard. Fix any path issues.
- [ ] **Afternoon (30 min):** Add the live demo URL prominently to the top of README + as a badge
- [ ] **Afternoon (30 min):** Test it works in incognito

**Deliverable:** A clickable, public URL like `https://attrisense.streamlit.app` that anyone (including a Lumentum hiring manager) can open in 1 click.

---

## Day 3 — Monday, May 4 — Repo Rename + Visual Polish

**Goal:** Brand identity. AttriSense, not "employee-flight-risk-ai-engine".

- [ ] **Morning (30 min):** Check `attrisense.com` and `attrisense.ai` availability on Namecheap or Porkbun. If both taken → use `RetainAI` or `StaySignal` instead.
- [ ] **Morning (30 min):** Rename repo on GitHub: Settings → Repository name → `attrisense`. Update local clone:
  ```bash
  cd employee-flight-risk-ai-engine
  git remote set-url origin https://github.com/Dogiparthi-Sharada/attrisense.git
  cd .. && mv employee-flight-risk-ai-engine attrisense
  ```
- [ ] **Morning (1 hr):** Search-and-replace old name in code:
  ```bash
  grep -rn "employee-flight-risk-ai-engine" .
  grep -rn "Lumentum HR AI" .   # change to "AttriSense (originally built for Lumentum interview)"
  ```
- [ ] **Afternoon (2 hr):** Add README badges (build, license, demo, paper). Update dashboard header to say "AttriSense" prominently.
- [ ] **Evening (1 hr):** Re-screenshot the dashboard with new name visible. Save 4–5 best screenshots to `/doc/screenshots/`.

**Deliverable:** Repo renamed. All collateral consistently uses "AttriSense". Live demo still works post-rename.

---

## Day 4 — Tuesday, May 5 — RECORD THE DEMO VIDEO

**Goal:** A 60-second screen recording that auto-plays in the LinkedIn feed.

- [ ] **Morning (1 hr):** Write the video script (template in `03_video_script_60s.md`)
- [ ] **Morning (2 hr):** Record using Screen Studio (free trial) or Loom or OBS:
  - Open dashboard, walk through KPIs (10s)
  - Click into a high-risk employee, show SHAP-like risk drivers (15s)
  - Demo the NL→SQL: type "show me high-risk Manufacturing engineers under 12 months tenure" (15s)
  - Show the exit-interview RAG output (10s)
  - End on the GitHub URL + your name (10s)
- [ ] **Afternoon (2 hr):** Edit in CapCut (free):
  - Trim to 60–75 seconds max
  - Burn in captions (essential — 85% of LinkedIn views are sound-off)
  - Add subtle zoom-ins on key moments
  - Export 1080×1080 (square) — best LinkedIn format
- [ ] **Evening:** Save final video as `attrisense_demo_60s.mp4`. Don't post yet.

**Deliverable:** A polished 60–75 second MP4 ready for LinkedIn native upload.

---

## Day 5 — Wednesday, May 6 — Paper to arXiv

**Goal:** "arXiv preprint, 2026" on your resume by Thursday morning.

- [ ] **Morning (1 hr):** Open `paper/attrisense_ieee.tex` on Overleaf. Compile. Read once.
- [ ] **Morning (1 hr):** Replace placeholder evaluation numbers with your real model output (re-run `predictive_engine.py` if needed).
- [ ] **Morning (1 hr):** Add the architecture diagram (export from Excalidraw → save as `paper/figures/architecture.png` → reference in tex).
- [ ] **Afternoon (1 hr):** Email your CSUEB capstone advisor: *"Would you be willing to be co-author on this paper? Draft attached."* Use template in `04_faculty_coauthor_email.md`.
- [ ] **Afternoon (1 hr):** Even without co-author, submit to arXiv as solo author under `cs.LG` (cross-list `cs.HC`):
  - https://arxiv.org → Register → Submit
  - You may need an endorser if it's your first arXiv submission. Email a CSUEB CS/IS faculty member to endorse.
- [ ] **Afternoon (30 min):** Cross-post to SSRN under "Information Systems eJournal" (no endorser needed, instant indexing).

**Deliverable:** arXiv submission ID. SSRN posted ID. Both linked from README and resume.

---

## Day 6 — Thursday, May 7 — Tech Transfer + LinkedIn Prep

**Goal:** Patent door opened. LinkedIn post ready to ship Friday.

- [ ] **Morning (1 hr):** Email CSUEB Office of Research / Tech Transfer (template in `05_csueb_tech_transfer_email.md`). Subject: *"MSBA student inventor — request for invention disclosure consultation."*
- [ ] **Morning (2 hr):** Final pass on the LinkedIn post. Use the FINAL CUT in `LINKEDIN_POST.md`. Customize 2–3 lines to feel like your voice.
- [ ] **Afternoon (1 hr):** Format with **AuthoredUp** Chrome extension (free) — adds bold/italic that LinkedIn supports.
- [ ] **Afternoon (1 hr):** Update LinkedIn profile:
  - Headline: *"MSBA @ CSUEB | Building AttriSense — open-source workforce intelligence | arXiv preprint 2026 | Open to AI/ML roles"*
  - Featured: pin 4 items (GitHub, live demo, arXiv, video)
  - Banner: refresh in Canva (free template)
  - Turn on Creator Mode
- [ ] **Afternoon (30 min):** Schedule the post in Buffer (free) for **Tuesday May 12, 8:30 AM PT** (or Friday May 8 if you want to ship sooner).

**Deliverable:** LinkedIn profile fully updated, post scheduled, Tech Transfer email sent.

---

## Day 7 — Friday, May 8 — Buffer Day & Send Thank-Yous

**Goal:** Slack day. Don't underestimate the importance of rest.

- [ ] Send a follow-up email to the Lumentum recruiter, *but only if* there's been radio silence since the interview. Template in `06_thank_you_email_template.md`.
- [ ] Reply to any Tech Transfer / advisor / arXiv emails that came in
- [ ] Optional: write the technical Towards Data Science article (3 hrs) — save for next week

**Deliverable:** Inbox at zero. Clear head for next week's launch.

---

## 📦 What's in this folder

| File | Purpose |
|---|---|
| `00_INTERVIEW_PLAYBOOK_TODAY.md` | **Read FIRST** — interview prep for today |
| `01_AI_CONTRIBUTIONS_template.md` | Template for `AI_CONTRIBUTIONS.md` (Day 1) |
| `02_README_banner_snippet.md` | Markdown banner to paste at top of README (Day 1) |
| `03_video_script_60s.md` | Word-for-word script for demo video (Day 4) |
| `04_faculty_coauthor_email.md` | Email to MSBA capstone advisor (Day 5) |
| `05_csueb_tech_transfer_email.md` | Email to Tech Transfer Office (Day 6) |
| `06_thank_you_email_template.md` | Post-interview thank-you (today, after interview) |
| `07_resume_bullets.md` | 5 ATS-optimized resume bullets you can copy in now |
| `08_ARCHITECTURE_DIAGRAM_SPEC.md` | Spec for the Excalidraw diagram (Day 1) |
| `09_AI_CHEATSHEET.md` | Cross-AI-tool prompt library — paste into ChatGPT/Claude/etc. |

---

## 🎯 The North Star

By Friday May 8 you will have:

1. ✅ Crushed the interview
2. ✅ Public live demo URL
3. ✅ Repo renamed to AttriSense
4. ✅ 60-second video ready to post
5. ✅ arXiv preprint published
6. ✅ Faculty co-author email sent
7. ✅ Tech Transfer email sent
8. ✅ LinkedIn profile fully optimized
9. ✅ Post scheduled for Tuesday May 12

That's the most a single person can ship in 7 days. Don't try to do more. Don't try to do less.
