# 🎤 Lightning Talk Proposal — Template + Venues

> Goal: get one **lightning talk** (5-15 min) accepted somewhere local.
> Why: a single accepted talk converts to (a) credibility line on resume, (b) a recording you can repurpose forever, (c) ~50 in-person warm leads.

---

## 🎯 The talk

**Title (top option):**
> *"AttriSense — Lessons From Building an Open-Source People-Analytics System as a Grad Student"*

**Backup titles:**
- *"From Capstone to Production: 5 Decisions I Wish I'd Made Earlier"*
- *"Why HR Analytics Is Stuck — and One Architectural Pattern That Helps"*
- *"SHAP + RAG + NL→SQL: A Multi-Modal Recipe for Domain AI"*

**Length:** 10-15 minutes (lightning) or 25-30 minutes (regular slot)

**Abstract:**

```
Most HR analytics systems are descriptive dashboards. Predictive
flight-risk models exist but rarely make it to managers because
the explanations are unconvincing.

In this talk I'll walk through AttriSense — an open-source,
multi-modal framework I built as my MSBA capstone — and the three
non-obvious design decisions that made it actually usable:

1. Why SHAP attributions feed the RAG retrieval (not just the
   dashboard).

2. Why the NL→SQL agent has a separate verifier loop.

3. The mistake I made with accuracy that cost me 6 weeks.

Code is open source. Paper is on arXiv. I'd love feedback.

Bio: Sharada Dogiparthi is an MSBA candidate at Cal State East
Bay focused on applied ML and analytics for HR/operations. Open
to roles in the Bay Area.
```

---

## 🎯 Where to submit

### Tier 1 — High signal, low barrier (submit this week)

| Venue | Format | Submit how | Notes |
|---|---|---|---|
| **Bay Area Women in Analytics** | 15-min talk | Email organizer via meetup.com | High match for profile |
| **SF Bay Area Pythonistas / PyData** | Lightning (5 min) or regular | meetup.com → message organizer | Heavy data science audience |
| **SF Bay ACM** | 15-min talk | acm.sfbay.org → talk submissions | More academic |
| **CSUEB Student Research Symposium** | Poster or talk | Internal CSUEB calendar | Use it for practice + faculty visibility |
| **Local college Data Science club** | Anywhere | Direct cold email to faculty advisor | Easy first venue for practice |

### Tier 2 — Bigger venues, longer review cycles

| Venue | Format | Notes |
|---|---|---|
| **PAPIs.io** | 20-min industry talk | CFP closes early in year |
| **ODSC West** | Workshop or talk | High prestige, San Francisco/Oakland |
| **MLOps World** | 20-min talk | Industry-leaning |
| **The HR Tech Conference** | Sponsored slot or sponsored content | Las Vegas, expensive but high-leverage |
| **PyData NYC / SF** | Talk | Highly competitive |

### Tier 3 — Online / async venues

| Venue | Format |
|---|---|
| **LinkedIn Live** (host yourself, 30 min) | Self-hosted |
| **YouTube Live** (host yourself) | Self-hosted |
| **Towards Data Science Author Webinar Series** | Already an author? Easy in. |
| **Discord / Slack community talks** (DataTalks.Club, MLOps Community, etc.) | Lower barrier |

---

## 📩 The submission email (cold, to a meetup organizer)

```
Subject: Talk pitch — AttriSense (open-source HR analytics framework)

Hi [Organizer],

I'm Sharada Dogiparthi, an MSBA candidate at Cal State East Bay.
I'd love to be considered for a 10-15 minute slot at an upcoming
[meetup name] event.

Talk title: "AttriSense — Lessons From Building an Open-Source
People-Analytics System as a Grad Student"

Three concrete takeaways:
• Why SHAP attributions should feed the RAG retrieval, not just
  the dashboard.
• Why a verifier loop matters for any NL→SQL agent in production.
• The accuracy mistake that cost me 6 weeks (and what I do now).

Project: https://github.com/Dogiparthi-Sharada/attrisense
Paper: [arXiv link]
Demo: [Streamlit link]

Happy to provide a 90-second pre-recorded preview if useful.
Flexible on timing — would love to be involved.

Sharada Dogiparthi
[email]
[LinkedIn]
```

---

## 🛠️ Slide structure (15-minute talk)

| Time | Slide | Content |
|---|---|---|
| 0:00 | Title | Name, project, university, one-line value prop |
| 0:30 | Hook | "Most HR analytics is descriptive. Here's what predictive looks like in practice." |
| 1:30 | The problem | The 3 gaps: prevalence, explainability, access |
| 3:00 | Architecture | The 3-layer diagram. 30 seconds per layer. |
| 5:00 | The non-obvious decisions | 3 slides, 1 design choice each |
| 9:00 | Demo | 2-3 min screen recording embedded |
| 11:30 | Results | The metrics table |
| 12:30 | Lessons | "What I got wrong" — the vulnerability part |
| 14:00 | What's next | Causal uplift, IEEE submission, patent path |
| 14:30 | CTA | Repo + paper + LinkedIn QR code |
| 14:45 | Q&A | Hard out at 15 |

**Slide-design rule:** one idea per slide. <20 words per slide. Big architecture diagram. Screenshot demos, don't try to live-demo unless asked.

---

## 🎯 Why even one accepted talk pays for itself

Even the smallest accepted talk gives you:

1. ✅ **A line on your resume:** *"Speaker, [Venue], May 2026"*
2. ✅ **A recording** you can post and link forever
3. ✅ **Permission to email** the audience afterward — every meetup has an opt-in list
4. ✅ **Trust transfer** from the venue's brand to yours
5. ✅ **A LinkedIn post angle** *("Spoke at [Venue] last night — slides + recording in the comments")*
6. ✅ **A reason to talk to other speakers** at the same event (warm intro, very high reply rate)

For 4-6 hours of total prep, the ROI is enormous.

---

## 💡 If no talk gets accepted in Week 4

Don't wait. **Host one yourself.**

- Pick a Friday afternoon
- Post a LinkedIn event: *"AttriSense Live Walk-Through — Q&A Open"*
- Use LinkedIn Live or Streamyard
- 30 minutes, free, no gatekeepers
- Anyone who shows up is now a warm contact

Self-hosted talks count for almost everything an accepted talk does, except the venue prestige line. And on iterations 2-3, you'll have the audience to land an accepted talk anyway.
