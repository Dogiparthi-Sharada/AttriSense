<!--
AttriSense — career/week1/03_video_script_75s.md
Author : Sharada Dogiparthi <dogiparthi.sharada@gmail.com>
Version: 1.0.0
Date   : 2026-05-07
License: MIT — see LICENSE in repo root.
Copyright (c) 2026 Sharada Dogiparthi. All rights reserved.
-->

# 75-Second Video Script — AttriSense LinkedIn Demo (v2)

> Total runtime: **75 seconds** (the extra 15 covers Cox PH +
> fairness gate + Review_ID — the parts that didn't exist in v1).
> Captions burned in. 1080×1080 square. Tools: Screen Studio / Loom /
> OBS → CapCut.

---

## 🎙️ Voiceover (read aloud, natural pace)

**[0:00 – 0:08] HOOK**
*"AttriSense predicts which employees are about to leave — before the
resignation email arrives. Five model modalities. One dashboard.
Seventy-five seconds."*

**[0:08 – 0:18] DASHBOARD OVERVIEW**
*"5,000 synthetic employees. 8.96% are flagged High Flight Risk.
Manufacturing has 342 high-risk people, mostly in the under-12-month
tenure band. Every prediction here passed an EEOC four-fifths
fairness gate before it hit the screen."*

**[0:18 – 0:32] DRILL INTO ONE EMPLOYEE**
*"Click into one of them. Review_ID `RV-841207` — Engineering,
8 months tenure, 81% probability of leaving. Notice we don't show
the raw employee ID; reviewers anchor on memory. The model's top three
drivers, from SHAP: below-band salary, no promotion in 18 months,
manager span of 14."*

**[0:32 – 0:44] SURVIVAL CURVE**
*"AttriSense doesn't just answer 'who is at risk' — it answers
'when'. The Cox proportional-hazards model gives you a survival
curve per employee. RV-841207 has a 50% survival probability at
day 180. That's not a number, that's a Q3 calendar item."*

**[0:44 – 0:58] CAUSAL UPLIFT**
*"And the T-Learner tells you which intervention will actually move
the needle for this person. Compensation correction: minus 22 points
of risk. Manager rotation: minus 8. Learning budget: minus 3. Causal
uplift, not a flat retention budget."*

**[0:58 – 1:08] NL → SQL DEMO**
*"And HR doesn't need to file an analyst ticket. Plain English."*
*[type into NL→SQL box]:* `show me high-risk Manufacturing engineers under 12 months tenure`
*"Eight seconds. Forty-seven employees. If the LLM goes down, a
TF-IDF gold-question fallback still answers the top 50 questions."*

**[1:08 – 1:15] CLOSE**
*"Open-source. MIT. Live demo, 7-page paper, beginner's guide DOCX —
all linked. Built as part of my MSBA at Cal State East Bay.
AttriSense — workforce intelligence that respects both the data and
the people in it."*

---

## 🎥 Shot list (1080×1080)

| Time | What's on screen | Caption (burned in) |
|------|------------------|---------------------|
| 0:00 – 0:03 | AttriSense logo on Pixel pastel banner | *"AttriSense"* |
| 0:03 – 0:08 | Dashboard load, KPI cards, fairness ribbon visible | *"Predict employee flight risk before they leave"* |
| 0:08 – 0:18 | Department risk donut + stacked bar | *"Manufacturing: 342 High Risk · Under 12 mo · Fairness ✓"* |
| 0:18 – 0:32 | Click into employee detail, SHAP waterfall | *"RV-841207 · 81% risk · top 3 drivers"* |
| 0:32 – 0:44 | Cox PH survival curve, KM band shaded | *"50% survival at day 180 — Cox PH"* |
| 0:44 – 0:58 | T-Learner uplift bars (3 arms) | *"Compensation: −22 pts · Manager rotation: −8 pts · Learning: −3 pts"* |
| 0:58 – 1:08 | NL→SQL input box, then results table | *"Ask in English. 8 seconds. With a TF-IDF safety net."* |
| 1:08 – 1:15 | GitHub URL + your name on Pixel banner | *"github.com/Dogiparthi-Sharada/attrisense"* |

---

## 🎨 CapCut tips

- **Music:** soft tech-bed at 20% volume. CapCut's free royalty-free
  library; search "corporate inspirational" or "minimal tech."
- **Captions:** **always** burn in. 85% of LinkedIn views are
  sound-off. White text, black drop shadow, lower-third.
- **Cuts:** every 4–6 seconds. No shot lasts more than 6.
- **Zoom-ins:** subtle 1.05× → 1.10× on the SHAP waterfall, the Cox
  curve, and the NL→SQL typing moment. Makes the 75-second runtime
  feel kinetic.
- **End card:** last 3 seconds = static frame with GitHub URL +
  AttriSense logo + your name. Hold this clearly so people can
  screenshot.

**Export:** 1080×1080, 30fps, MP4 (H.264). Aim for under 100 MB.

---

## 🎤 If you're nervous about your voice

1. **Record yourself.** Authenticity wins on LinkedIn. AirPods or a
   $30 lavalier. Practice the script 3× before recording.
2. **ElevenLabs voice clone.** 10-min setup, 1-min sample. Free tier
   is enough for one 75-second clip.
3. **Music + captions only.** Slow the pacing to 90 seconds and let
   the captions carry the story.
