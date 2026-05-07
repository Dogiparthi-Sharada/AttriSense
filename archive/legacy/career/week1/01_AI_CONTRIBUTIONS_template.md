# AI_CONTRIBUTIONS.md

> Save this file as `AI_CONTRIBUTIONS.md` in the repository root.
> This is the standard 2026 disclosure expected by major academic
> venues (ACM, IEEE, NeurIPS, KDD) and increasingly by employers.

---

# AI Contributions Disclosure

This project was developed with the assistance of Large Language
Model coding tools. In line with the disclosure norms emerging
across academic and industrial communities in 2025–2026, this
document provides a transparent record of how AI assistants were
used during development.

## AI Tools Used

- **GitHub Copilot** (in-IDE code completion and suggestions)
- **Claude 3.7 / Opus** (architecture discussion, debugging,
  documentation drafting, paper writing assistance)
- **OpenAI GPT-4 / GPT-4o** (boilerplate generation, exploratory
  prototyping, prompt engineering for the embedded LLM agents)

## How AI Was Used

| Activity | AI Role | Human Role |
|---|---|---|
| Architecture & design decisions | Brainstorming partner | Final author of all decisions |
| Boilerplate code (Streamlit layouts, Plotly chart scaffolds) | Generated initial drafts | Reviewed, modified, tested |
| Algorithm implementation (Random Forest pipeline, SMOTE, FAISS index, LangChain agent) | Suggested standard patterns | Selected, integrated, tuned, validated |
| Prompt engineering for the NL→SQL and RAG agents | Iterative refinement partner | Specified intent, tested edge cases |
| Documentation, README, paper drafting | Initial drafts | Edited, fact-checked, finalized |
| Debugging and error resolution | Diagnostic partner | Identified the actual root causes |
| Evaluation harness and metrics selection | Suggested standard metrics | Chose what to measure and why |

## What AI Did *Not* Do

- AI was **not** a co-author on the project. AI assistants cannot
  consent to publication agreements and do not appear in the author
  list of any related paper.
- AI did **not** make architectural or business-impact decisions.
  All such decisions were made by the human author.
- AI did **not** run any experiments. All training, evaluation, and
  reporting were executed by the human author on her own machine.
- AI-generated code was **not** committed without human review.

## Verification

Every commit in this repository was authored by a human after review
of any AI-generated suggestions. The author takes full responsibility
for the correctness, security, and ethical implications of every line
of code.

The git history, including commit timing and authorship, is publicly
auditable.

## Why This Matters

Transparent AI-use disclosure is not a sign of weakness — it is the
emerging standard for responsible engineering and research. A
candidate who uses AI well, and is honest about it, is more credible
in 2026 than one who claims not to.

---

*This disclosure follows the practices recommended by the ACM Code
of Ethics, the IEEE author guidelines (2024 update), and the
NeurIPS / ICLR / KDD policies on responsible use of AI in research.*

— Sharada Dogiparthi
M.S. Business Analytics, California State University, East Bay
