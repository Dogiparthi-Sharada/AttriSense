# Month-in-Review LinkedIn Post (Wed May 27, 8:30 AM PT)

> **The post that closes the loop.** Reference everything that
> happened in the prior 28 days, in numbers. This is the post that
> recruiters bookmark to forward to their hiring managers.

---

## Post body (~1,600 chars)

> *28 days ago I launched AttriSense.*
>
> *Quick honesty check on what shipped — and what didn't.*
>
> **What shipped 🚀**
> – Live demo at attrisense.streamlit.app (X demo sessions to date)
> – 5 model modalities: RandomForest+SMOTE (ROC-AUC 0.91 · PR-AUC 0.74), Cox PH (concordance 0.78), EconML T-Learner causal uplift, multilingual RAG with hashing fallback, NL→SQL with TF-IDF safety net
> – EEOC four-fifths fairness gate as a *blocking* check
> – Salted-hash Review_ID layer for identification-bias mitigation
> – Pixel-pastel UI (cream canvas, dark-ink axes — actually legible)
> – 7-page IEEE paper · submitted to Big Data 2026 (Industry Track) · arXiv preprint live
> – 79-page beginner's-guide DOCX (cover + Word TOC + 8 chapters + diagrams)
> – mkdocs --strict passing · 0 warnings
> – 8-slide architecture carousel · "3 things I got wrong" vulnerability post
> – 15-slide Engineering-VP pitch deck
>
> **What didn't 🪞**
> – I underestimated how long the paper would take. Took 3× longer than I planned.
> – My first SMOTE pipeline leaked synthetic neighbours from train into test. Test AUC was a fake 0.96. Fixed it. Honest 0.91.
> – My first RAG layer hung the dashboard when the network was slow. Added a reachability probe + hashing fallback. Render path no longer blocks on a 3rd party.
> – I shipped raw `Emp_ID` to the dashboard for the first 3 months and didn't realise it was an identification-bias risk. The 25-line Review_ID module does more for fairness than any classification metric.
>
> **What I learned 📚**
> – PR-AUC > ROC-AUC for imbalanced classes. Always.
> – SMOTE-after-split. Always.
> – Don't let a 3rd-party API into your render path without a fallback. Always.
> – Pseudonymise at the rendering layer, not the storage layer. The reviewer is the bias risk.
>
> **What's next 🛣️**
> – Real-data pilot conversations (DM if interested)
> – On-prem provider fallback (Bedrock + local hashing)
> – Fairness audit at 50k-employee scale
> – First conference talk (CFP submitted to PyData / Bay Area WIA / ODSC)
>
> *Open to AI Engineering / Applied ML / People-Analytics roles.
> Repo: https://github.com/Dogiparthi-Sharada/attrisense ·
> Demo: https://attrisense.streamlit.app · Paper + DOCX in repo.*
>
> *Massive thanks to everyone who commented, DM'd, retweeted, sent
> a pull request, or just clicked the demo. Names in the
> README acknowledgements.*
>
> #MachineLearning #ResponsibleAI #OpenSource #PeopleAnalytics

---

## Posting protocol

1. **8:30 AM PT Wednesday** — mid-week is right for retrospective
   posts (Tue is for launches; Fri is for vulnerability).
2. **Pin this post to your profile** for the rest of the month.
3. **No video this time.** The post is the artefact. Linking to the
   carousel and the vulnerability post in the comments is enough.
4. **Comment 1 (your own first reply):**
   > *"Numbers are real. Carousel is here: [link]. Vulnerability
   > post is here: [link]. The 'what didn't' section is the one I
   > re-read most."*
5. **Reply discipline:** by now, comments will skew quality over
   quantity. Make every reply count.

---

## After posting

- **Send thank-you DMs** to the top 5 people who supported the
  campaign (not all 50 — the top 5). Personalised, specific.
  *"Your comment on May 13 about [specific thing] genuinely shifted
  how I framed [specific thing] in the vulnerability post. Thank
  you."*
- **Update README acknowledgements.** Names of people who PR'd,
  reviewed, or gave high-leverage feedback.
- **Save the analytics screenshot** for the 90-day roadmap and for
  any future "year in review" content.
