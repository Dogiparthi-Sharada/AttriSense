# LinkedIn Launch Post — Tuesday May 12, 8:30 AM PT

> **Length:** 1,300 chars (LinkedIn cap is 3,000; engagement curves
> peak at 1,200–1,800). **Format:** hook → tension → reveal → proof
> → CTA. **Native video** in the comments — DO NOT YouTube-link.

---

## Post body (copy-paste ready)

> *Most HR analytics tells you who left.*
>
> *AttriSense tells you who's about to — and what to do about it.*
>
> I'm finally launching the platform I built as my MSBA capstone at
> Cal State East Bay: a five-modality, open-source workforce-
> intelligence engine that answers four questions in one dashboard.
>
> 🔵 **Who is at flight risk?** — RandomForest + SMOTE, ROC-AUC 0.91, PR-AUC 0.74.
> 🟣 **When are they likely to leave?** — Cox proportional-hazards, concordance 0.78. Survival curve per employee.
> 🟢 **Which intervention helps THIS person?** — EconML T-Learner across three arms: compensation, manager rotation, learning budget.
> 🟠 **What did similar leavers say?** — Multilingual RAG over EN/ES/HI exit-interview text, with a hashing fallback when the OpenAI endpoint is unreachable.
> 🟡 **What does HR want to know right now?** — Natural-language SQL with a TF-IDF gold-question safety net.
>
> The piece I'm proudest of isn't a model. It's the **Review_ID
> layer** — every dashboard view replaces the raw employee ID with a
> salted SHA-256 pseudonym (`RV-NNNNNN`), so reviewers can't anchor
> on memory and silently override the model.
>
> Every prediction is gated by an EEOC four-fifths fairness audit
> before it reaches the screen.
>
> 🔗 Live demo (no install): https://attrisense.streamlit.app
> 📄 7-page IEEE paper + 79-page beginner's guide DOCX in the repo
> ⭐ MIT-licensed: github.com/Dogiparthi-Sharada/attrisense
>
> 75-second walkthrough video in the comments 👇
>
> #AI #MachineLearning #PeopleAnalytics #ResponsibleAI #OpenSource

---

## In the comments (drop these as your own first reply)

**Comment 1 — the video**
> "Walkthrough — 75 seconds, sound off works (captions burned in):
> [native video upload]"

**Comment 2 — for the technically curious**
> "If the architecture diagram is more your speed, the 7-page paper
> has Fig 1 and the four-table results section: [link to PDF in repo]"

**Comment 3 — the disclosure**
> "Built with LLM coding tools — line-grain disclosure here:
> [link to AI_CONTRIBUTIONS.md]. Decisions and design were mine;
> boilerplate and refactors were AI-assisted."

---

## Variant A — for if you have a referrer / mutual

> *Six months ago I had one model. Today I have five — and the part
> I'm proudest of still isn't a model.*
>
> [...same body...]

## Variant B — short / mobile-first

> AttriSense — open-source workforce intelligence.
>
> 5 modalities. 1 dashboard. 1 fairness gate.
>
> ROC-AUC 0.91 · Cox concordance 0.78 · per-employee causal uplift ·
> multilingual RAG with provider fallback · NL→SQL with TF-IDF safety net.
>
> No raw employee IDs ever rendered — salted Review_ID by default.
>
> Demo: attrisense.streamlit.app · MIT · github.com/Dogiparthi-Sharada/attrisense

---

## Posting protocol (don't skip)

1. **8:30 AM PT** — first hour of West Coast tech LinkedIn is gold.
2. Post **without** the video. Wait 60 seconds, then drop the video
   as the first comment. (LinkedIn down-ranks posts with off-platform
   links; native video in the comment beats a video in the post when
   you also have a clickable Streamlit URL.)
3. **Reply to every single comment for the first 4 hours.** Even
   "congrats!" — reply with one specific question back.
4. **Cross-post 30 minutes later** to Twitter/X (`02_twitter_thread_10t.md`).
5. **DMs out:** 5 warm-ish-people DMs (`03_cold_dm_templates.md`)
   *after* the post is live. "Hey, I just launched this — would love
   your eyes" beats "hey, can you look at my project?"
6. **Hour 4 check-in:** screenshot the post analytics. Save to
   `outputs/launch_metrics_h4.png`. You'll need this for the
   Month-in-Review post in Week 4.
7. **Day 1 close:** reply to anything still open. Mute notifications
   at 9 PM. Sleep.
