# Engagement Response Bank — pre-canned replies for the launch post

> The launch post will pull 6 categories of comments. The first 4
> hours are the highest-leverage window of the entire campaign —
> a sharp, specific reply within 60 minutes is worth 100 generic
> "thanks!" replies on day 3.

---

## A. "Cool project!" / "Congrats!" / generic positive

**Don't reply with "thanks!"** Reply with a *specific question back*.

> "Thanks [name] — quick one for you: of the five modalities, which
> would you rip out first for a real-world pilot? I keep going
> back-and-forth on the NL→SQL layer."

Why: turns the comment into a thread. LinkedIn algorithm rewards
threaded conversations more than likes.

---

## B. "Isn't this just attrition prediction?"

> "Fair pushback. Single-classifier attrition prediction is the
> first 20% of the problem. The other 80% is *what to do about it*
> — which is why AttriSense layers Cox PH (the *when*) and the
> EconML T-Learner (the *which intervention for which person*) on
> top. The first model says risk = 0.81; the third model says
> compensation correction lowers it by 22 points but learning budget
> only lowers it by 3. That's the difference between an alert and an
> action."

---

## C. "How are you handling bias / fairness?"

> "Great question. Three layers: (1) every prediction is gated by an
> EEOC four-fifths disparate-impact audit before it reaches the
> screen — if the ratio drops below 0.80 between protected classes,
> the recommendation is suppressed and the dashboard tells the user
> why; (2) the dashboard never displays raw `Emp_ID` — it shows a
> salted SHA-256 Review_ID (`RV-NNNNNN`) so reviewers can't anchor
> on memory and silently override the model; (3) the paper has a
> per-department fairness audit table so the disparate-impact ratio
> is reproducible. Synthetic data, MIT — all in the repo."

---

## D. "Are you using real data?"

> "Synthetic. 5,000 rows, generated programmatically from published
> HR-attrition distributions, deterministic (`seed=42`), MIT. The
> system is designed to re-point at any HRIS — Workday, BambooHR,
> ADP, etc. — but the public artefact ships with synthetic data
> only. There's a synthetic-data notice at the top of the README and
> a longer explanation in the beginner's guide DOCX."

---

## E. "What did you use AI / Copilot / GPT for?"

> "Line-grain disclosure in `AI_CONTRIBUTIONS.md` in the repo. Short
> version: every architectural and modelling decision was mine —
> the choice of five separable modalities, the Review_ID layer,
> the fairness gate, the SMOTE-after-split fix, the RAG provider
> fallback design. Boilerplate (Streamlit layout, theme CSS, Pillow
> drawing primitives, the markdown→DOCX renderer) was AI-drafted and
> human-reviewed. The paper text and the modelling pipelines are
> human-authored."

---

## F. "I'm hiring — DM me?"

🎯 **Goldcard.** Drop the cold-DM template (`03_cold_dm_templates.md`
template #2) immediately. **Do not delay until tomorrow.** Reply
publicly with: *"Just sent you a note 🙏 — happy to walk through any
layer."*

---

## Hour-by-hour discipline (Tue May 12)

| Hour | What you do | What you don't do |
|------|-------------|-------------------|
| H+0 | Post live · video in comment 1 · share with 5 friends to seed early signal | Refresh analytics |
| H+0 → H+4 | Reply to **every** comment within 60 min · keep replies *specific* | Generic "thanks" replies |
| H+4 | Screenshot analytics → save as `outputs/launch_metrics_h4.png` | Compare to anyone else's launch |
| H+4 → H+8 | Cross-post Twitter thread · send 5 DMs · keep replying | Read DMs from people you don't recognise |
| H+8 → bedtime | Reply to anything still open · plan H+24 follow-up | Stay up past 10 PM |
| H+24 | One quote-of-yourself follow-up post: *"24 hr in — biggest surprise from the comments was X"* | Repost the original |

---

## Saturday review questions

- Which comment sparked the most thread depth? → that's a TDS or
  carousel topic for Week 3.
- Which DM converted to a real conversation? → re-read it,
  copy what worked.
- Which DM didn't convert? → study the silence; don't copy what
  didn't work.
- Pipeline tracker: ≥ 1 active recruiter conversation? If no, the
  launch post needs a quote-tweet relaunch on Monday.
