# 🎴 LinkedIn Carousel — 6-Slide Architecture Deep-Dive

> Build in **Canva** (free template: search "linkedin carousel tech").
> Export as PDF (LinkedIn auto-converts PDF carousels into native swipeable posts).
> Schedule for **Tuesday May 19, 8:30 AM PT** (Week 3).

---

## 🎨 Visual style guide

- **Format:** 1080×1350 (portrait) — the highest-engagement LinkedIn carousel size
- **Pages:** 6 (LinkedIn caps at 10, but 6 is the sweet spot for completion rate)
- **Color palette:**
  - Primary: `#667eea` (purple-blue, matches dashboard)
  - Accent: `#FFA15A` (orange — for highlights)
  - Background: `#0f172a` (deep navy) for slides 1, 6 / `#ffffff` (clean white) for slides 2–5
  - Text: white on dark, near-black (#1a1a1a) on light
- **Font:** Inter or system sans-serif. Consistent across all slides.
- **Brand mark:** "AttriSense" in top-left of every slide (small, ~12pt)
- **Page number:** "1/6" "2/6" etc. in bottom-right
- **Last slide:** GitHub URL + your name + "DMs open"

---

## 🎴 Slide 1 — The Hook (dark BG, white text)

```
                  AttriSense
       ─────────────────────────────────

       How I built an AI system that
       predicts employee flight risk
       — before the resignation email.


              [SWIPE FOR ARCHITECTURE →]


              MSBA capstone · open source
              IEEE preprint · live demo
```

**Visual:** A subtle background graphic — abstract neural-network style or just a clean geometric pattern. No photos.

---

## 🎴 Slide 2 — The Problem (white BG)

```
                The 3 gaps in HR analytics

   ┌─────────────────────┐
   │ 🚪 The Trust Gap     │  Black-box risk scores.
   │                      │  Managers refuse to act.
   └─────────────────────┘

   ┌─────────────────────┐
   │ 📚 The Qualitative   │  Tabular features only.
   │     Gap              │  Exit interviews ignored.
   └─────────────────────┘

   ┌─────────────────────┐
   │ 🐢 The Access Gap    │  HR waits 2.3 days for
   │                      │  every analyst query.
   └─────────────────────┘
```

---

## 🎴 Slide 3 — The Architecture (white BG, the diagram)

Drop the architecture diagram from `week1/08_ARCHITECTURE_DIAGRAM_SPEC.md` here.

Caption text below the diagram:
```
Three layers, one workflow:
🎯 Predictive   →   🧠 RAG   →   💬 NL→SQL
```

---

## 🎴 Slide 4 — The Numbers (white BG)

```
              Numbers that matter

   ┌──────────────┐  ┌──────────────┐
   │  ROC-AUC     │  │  PR-AUC      │
   │  0.91        │  │  0.74        │
   └──────────────┘  └──────────────┘

   ┌──────────────┐  ┌──────────────┐
   │  NL→SQL acc  │  │  Latency     │
   │  86%         │  │  11.7s       │
   └──────────────┘  │  (was 2.3d)  │
                     └──────────────┘

       PR-AUC > ROC-AUC because
       the positive class is rare.

       Pick the metric that matches
       the cost of the error.
```

---

## 🎴 Slide 5 — The Decision Layer (white BG)

```
        From score → conversation

   Employee: Priya · Eng · 8mo · 81% risk

   Top SHAP drivers:
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   ▸ Below-band salary
   ▸ No promotion in 18 mo
   ▸ Manager span = 14
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   RAG retrieves 5 similar past leavers
   → grounds the manager rationale
   → produces a 3-bullet action plan

       That's not a number.
       That's a Monday-morning conversation.
```

---

## 🎴 Slide 6 — CTA (dark BG, white text)

```
              Open source · MIT license


       🔗 github.com/Dogiparthi-Sharada/attrisense
       🎬 attrisense.streamlit.app
       📄 arXiv preprint linked in comments


              Built by Sharada Dogiparthi
              MSBA · Cal State East Bay
              Open to AI/ML/People Analytics roles


              📩 DMs open. Coffee on me.
```

---

## ✍️ Caption text for the LinkedIn post (the body of the carousel post)

```
A week ago I posted about AttriSense — an open-source AI system that
predicts employee flight risk.

A lot of you asked for the architecture. So here it is, 6 slides.

Three layers:
1️⃣ Random Forest + SMOTE for the predictive base
2️⃣ FAISS RAG over exit-interview text for qualitative grounding
3️⃣ LangChain SQL agent so HR can talk to the data lake in English

The unlock isn't any one piece — it's how they compose. SHAP
attributions feed the RAG retrieval query. RAG output grounds the
manager-facing rationale. NL→SQL means non-technical HR users can
explore the data without filing analyst tickets.

PR-AUC of 0.74. NL→SQL accuracy 86%. End-to-end latency 11.7s
versus 2.3 days baseline.

If you're building people analytics, ML platforms, or HR tech —
swipe through and tell me what I got wrong.

Repo + paper + live demo in the comments.

#PeopleAnalytics #LLM #RAG #LangChain #MachineLearning #HRTech
#OpenSource #DataScience #MSBA #CSUEB #OpenToWork
```

---

## 📊 Why carousels outperform single posts

LinkedIn analytics consistently show:

- **Carousels: 3–5× higher reach** than single-image posts (algorithm rewards swipes as engagement)
- **Completion rate is the metric** — keep it 6 slides, not 10
- **First slide must be a hook** — otherwise no swipes
- **Last slide must have a clear CTA** — otherwise the swipes don't convert

---

## ✅ Pre-publish checklist

- [ ] All 6 slides have consistent fonts/colors
- [ ] Brand mark on every slide
- [ ] Page numbers (1/6, 2/6, ...) on every slide
- [ ] No typos (especially on slide 1 and slide 6 — most-read)
- [ ] PDF exported, file size under 100MB
- [ ] Tested on phone screen (carousels are 80% mobile)
- [ ] Caption is under 1,300 characters (LinkedIn truncates beyond)
- [ ] Hashtags: 12–15 max
- [ ] Scheduled for Tue May 19, 8:30 AM PT
- [ ] First-comment with links is pre-drafted

---

## 🎁 Bonus: 3 alternative carousel angles for future weeks

Once this one performs, you can re-use the format:

1. **"3 things I got wrong"** — slide deck of design mistakes and what you fixed. *Vulnerability posts crush on LinkedIn.*
2. **"What an MSBA actually teaches you"** — case for business framing in ML. Rare framing, very shareable.
3. **"From class project to arXiv preprint"** — the publication journey. Educational angle for student audience.
