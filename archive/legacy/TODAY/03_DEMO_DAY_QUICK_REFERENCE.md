# ⚡ Demo Day Quick Reference — Print This Page

> Single-page cheat sheet. Memorize the bold lines.

---

## 🕐 Today's timeline

| Time | What |
|---|---|
| 9:30 AM | Final demo dry-run on your laptop. Streamlit running, browser tabs open. |
| 10:00 AM | Charge laptop + phone to 100%. Phone hotspot ready as Wi-Fi backup. |
| 10:15 AM | Quiet, distraction-free room. Water. Notebook + pen. |
| 10:30 AM | Re-read week1/00_INTERVIEW_PLAYBOOK_TODAY.md. Final breath. |
| 10:55 AM | Join the call 5 min early. Test camera + mic. |
| 11:00 AM | **Show up. Be calm. The work is real.** |
| ~12:00 PM | Wrap. Take notes immediately while fresh. |
| 7:00 PM | Send the thank-you email (week1/06_thank_you_email_template.md). |

---

## 🎯 The 5 lines to memorize

### 1. Opening (when asked "tell me about yourself")
> *"I'm an MSBA candidate at Cal State East Bay finishing my capstone. I built AttriSense — an open-source, multi-modal HR-analytics framework — predictive flight-risk plus RAG over exit interviews plus a natural-language SQL agent. I'm here because the role overlaps strongly with what I've been building."*

### 2. AI-disclosure (when asked "did you write this yourself?")
> *"Yes — Copilot and Claude were collaborators throughout. The work that's mine is the architecture, the trade-offs, the evaluation methodology, and being able to defend every line. Generation is cheap right now. Judgment is the differentiator."*

### 3. Limitations (when asked "what doesn't it do?")
> *"It's correlational, not causal. It tells you who is likely to leave; it doesn't tell you what intervention would change that. Causal uplift modeling is the v3 work. The data is also synthetic — calibrated to public HR distributions but not validated on real corporate data."*

### 4. The patent / paper signal (work it in naturally if asked about future work)
> *"I'm in conversation with my university's tech transfer office about a provisional patent on the SHAP-conditioned RAG architecture. Paper goes up on arXiv next week and I'm targeting IEEE Big Data Industry Track for formal submission."*

### 5. Closing — your reciprocal question (always have ONE ready)
> *"What does success look like in the first 6 months for someone in this role? And — separately — what's the team's biggest open technical question right now?"*

---

## 🔗 URLs to know cold

```
Repo:    github.com/Dogiparthi-Sharada/employee-flight-risk-ai-engine
Demo:    [your Streamlit URL]
arXiv:   [arxiv link when live]
Paper:   in /paper/ folder of repo
Email:   [your personal email]
LinkedIn: linkedin.com/in/[your-handle]
```

**Have these ON YOUR PHONE LOCK SCREEN.** Or written on paper. Don't fumble.

---

## 🚦 Hard questions and one-line answers

| Q | A |
|---|---|
| "Why Random Forest, not XGBoost?" | *"RF was the chosen baseline — PR-AUC 0.74 with SMOTE in the training fold only. XGBoost likely gives 1-3% lift; benchmarking it for v2."* |
| "Is the data real?" | *"Synthetic, 5K employees, calibrated to public HR distributions. Real corporate data is the next milestone — looking for a partner."* |
| "How is this different from `[existing tool]`?" | *"Most tools are descriptive dashboards. AttriSense composes prediction + retrieval + NL-SQL into a single workflow. The novel piece is using SHAP attributions as the retrieval query, not just the explanation."* |
| "What was hardest?" | *"Catching the SMOTE fold-leak in evaluation. My V1 numbers were inflated by 4-6 points. Caught it on review, fixed it, the model is honest now."* |
| "Why are you leaving your current role?" *(if asked)* | *"I'm not looking to leave under stress — I'm looking for a role where applied ML at scale is the core of the work. AttriSense is the proof I want to do this full-time."* |
| "Salary expectation?" | *"I'd love to hear the range you have in mind for this role first — happy to talk specifics once we're aligned on fit."* |
| "When can you start?" | *"Two weeks' notice from acceptance, give or take a graduation date in [June]."* |

---

## 🛑 Things NOT to say

- ❌ "I'm not really an ML expert, but..."  → never undersell. Just answer.
- ❌ "I think it works..." → it works. Say "it works."
- ❌ "AI wrote most of it" → see the AI-disclosure line above. Frame as collaboration.
- ❌ "I don't know" without "...let me think about it" or "...here's how I'd find out"
- ❌ Bad-mouthing current employer
- ❌ Asking about salary in the first 5 minutes

---

## 📓 Mid-interview note-taking

While they talk, write down:
- ✏️ One specific thing they said about the team
- ✏️ One specific thing they said about the role
- ✏️ One name they mentioned (their teammate, their manager, a tool, a paper)
- ✏️ One question that surprised you

You'll use ALL of these in the thank-you email tonight. Specificity wins.

---

## 🎬 If you're asked to live-demo

1. **Open the Streamlit demo in a fresh browser window** before the call
2. **Share screen, but only that window** — not your whole desktop
3. **Walk through this 90-second path:**
   - Open dashboard → "this is the manager view, top KPIs"
   - Drill into one employee → "here's their risk score with SHAP drivers"
   - Open NL→SQL tab → ask: *"how many high-risk employees are in engineering this quarter?"*
   - Read the answer aloud, point at the SQL it generated
4. **Stop.** Don't show every feature. Let them ask.

---

## 🚨 If something breaks

- Demo URL is down → screenshot folder on desktop, walk through screenshots
- Wi-Fi dies → switch to phone hotspot (already paired)
- Laptop crashes → continue on phone, audio only — answer questions, send links after
- You blank on a question → *"Great question — let me think about that for a second."* Pause. Then answer.

**They are not testing whether everything goes perfectly. They are testing how you handle when it doesn't.**

---

## 💎 Three reminders

1. **You belong in the room.** They invited you. The work is real.
2. **Generosity beats brilliance.** Be the candidate who's easy to talk to.
3. **The thank-you email tonight matters as much as the interview itself.**

You've got this. Onward.
