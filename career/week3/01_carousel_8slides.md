# Architecture Carousel — 8 Slides (Tue May 19, 8:30 AM PT)

> **Format:** LinkedIn carousel, 1080×1080 per slide, PDF upload.
> **Tool:** Figma or Canva. **Theme:** Pixel pastel — cream `#FBF7F2`
> canvas, lavender `#B8B5E1` / peach `#F5C4A0` / sage `#B5D4A8`
> accents, dark ink `#3D3A35` text. Match the dashboard.

---

## Slide-by-slide spec

### Slide 1 — Cover

> **Headline:** *AttriSense — five modalities, one dashboard.*
> **Sub:** *Open-source workforce intelligence. MIT.*
> **Visual:** small Pixel-pastel architecture thumbnail bottom-right.
> **Footer:** swipe arrow → · github.com/Dogiparthi-Sharada/attrisense

### Slide 2 — Why one dashboard isn't enough

> **Headline:** *Single-classifier attrition prediction is the first 20%.*
>
> **Body (3 lines):**
> – Classifier: *who is at risk?*
> – Survival: *when do they leave?*
> – Causal: *which intervention helps THIS person?*
>
> **Footer:** *AttriSense ships all three. Plus RAG. Plus NL→SQL.*

### Slide 3 — Modality 1: classifier

> **Headline:** *🔵 Who? — RandomForest + SMOTE*
>
> **Body:**
> – ROC-AUC 0.91 · PR-AUC 0.74
> – SMOTE *after* train/test split (the v1 mistake everyone makes)
> – Calibration error 6.1%
> – SHAP per-employee driver decomposition
>
> **Visual:** SHAP waterfall screenshot (one employee).

### Slide 4 — Modality 2: survival

> **Headline:** *🟣 When? — Cox proportional-hazards (lifelines)*
>
> **Body:**
> – Concordance 0.78
> – Per-employee survival curve
> – Median time-to-event by department
> – Translates risk score → calendar-aware action
>
> **Visual:** Cox survival curve screenshot with 95% band.

### Slide 5 — Modality 3: causal uplift

> **Headline:** *🟢 Which intervention? — EconML T-Learner*
>
> **Body:**
> – Three intervention arms: comp, manager rotation, learning
> – Per-employee CATE
> – So retention budget isn't flat-distributed
> – Causal uplift, not flat retention spend
>
> **Visual:** uplift bar chart (3 arms).

### Slide 6 — Modality 4: multilingual RAG (with fallback)

> **Headline:** *🟠 What did similar leavers say? — Multilingual RAG*
>
> **Body:**
> – EN / ES / HI exit-interview text
> – 250 ms DNS+TCP+HTTPS reachability probe
> – Hashing fallback (256-d, MD5) when network blocks OpenAI
> – Per-provider FAISS index dirs (1536-d ≠ 256-d)
>
> **Visual:** RAG provider-fallback flow diagram.

### Slide 7 — Modality 5: NL→SQL with TF-IDF safety net

> **Headline:** *🟡 Plain English to SQL — with a TF-IDF safety net*
>
> **Body:**
> – LangChain primary path
> – TF-IDF gold-question fallback (50-question gold set)
> – 11/50 answered correctly without the LLM at all
> – Dashboard never blocks on a 3rd-party endpoint
>
> **Visual:** NL→SQL input box + result.

### Slide 8 — The layer most projects skip

> **Headline:** *The piece I'm proudest of isn't a model.*
>
> **Body:**
> – Every dashboard view replaces `Emp_ID` with a salted SHA-256
>   **Review_ID** (`RV-NNNNNN`)
> – Reviewers can't anchor on memory and silently override the model
> – Salt rotatable per pilot via `ATTRISENSE_REVIEW_ID_SALT`
> – Plus: every prediction is gated by an EEOC four-fifths
>   fairness audit before it reaches the screen
>
> **Visual:** before/after screenshot (Emp_ID `E001` → `RV-771131`).

### Slide 9 — CTA (yes, 9 — LinkedIn allows up to 20)

> **Headline:** *Try it.*
>
> **Body:**
> – Live demo: attrisense.streamlit.app
> – 7-page IEEE paper in repo
> – 79-page beginner's guide DOCX in repo
> – MIT: github.com/Dogiparthi-Sharada/attrisense
>
> **Footer:** *Open to AI Engineering / Applied ML / People-Analytics roles.*

---

## LinkedIn post body (the carousel caption)

> *Last week I launched AttriSense.*
>
> *This week I want to walk through the architecture — because the
> single-screenshot version of "ML retention model" has been done a
> hundred times, and the interesting story is **what the other four
> modalities are doing.***
>
> *Carousel below.*
>
> *Most surprising slide for me to write was Slide 8 — the
> Review_ID layer. It's not a model. It's a 25-line salted-hash
> module. And it does more for fairness in practice than any of the
> four classification metrics, because it stops reviewers from
> bypassing the model in the first place.*
>
> *Curious where you'd push back. Replies open.*
>
> *Demo: https://attrisense.streamlit.app · Repo: https://github.com/Dogiparthi-Sharada/attrisense*
>
> #AI #MachineLearning #ResponsibleAI #PeopleAnalytics #OpenSource

---

## Build notes

- **Generate the slide PNGs directly from Pixel pastel diagrams** —
  the same code that built `docs/images/diagrams/*.png` can render
  carousel-sized art via `scripts/generate_doc_diagrams.py`. Add an
  `--carousel` flag if needed.
- **Export as PDF** for LinkedIn (PDF carousels load faster and
  preserve text crispness vs. 9 individual PNG uploads).
- **Save the source** to `outputs/carousel_v2.pdf` and the slide
  PNGs to `outputs/carousel_v2/slide_{1..9}.png` for reuse in the
  Month-in-Review post.
