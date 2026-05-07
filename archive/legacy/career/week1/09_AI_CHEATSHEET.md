# 🤖 Cross-AI Cheat Sheet — Use AttriSense Across ChatGPT / Claude / Gemini / Perplexity

> Paste any of these prompts into any AI tool. They give the model
> enough context to be useful immediately, without you having to
> re-explain the project every time.

---

## 🔑 The Master Context Block

> Paste this **at the start of every new chat** with any AI tool.
> It primes the model with everything it needs to know.

```
I am Sharada Dogiparthi, an MSBA candidate at California State University, East Bay (graduating soon, looking for AI/ML/Data Science internship or full-time roles).

I have built an open-source project called AttriSense — a workforce-analytics platform that predicts employee flight risk. Here's the project context:

PROJECT: AttriSense (originally "employee-flight-risk-ai-engine")
GITHUB: https://github.com/Dogiparthi-Sharada/employee-flight-risk-ai-engine
TECH STACK:
  - Python 3.11
  - Random Forest + SMOTE (scikit-learn, imbalanced-learn) — ROC-AUC 0.91, PR-AUC 0.74
  - FAISS dense vector index over 500 synthetic exit interviews
  - OpenAI text-embedding-3-small for embeddings
  - LangChain SQL agent (NL-to-SQL) — 86% exact-match on 50-question gold set
  - GPT-4 / GPT-4o-mini for retention rationale generation
  - Streamlit dashboard with Plotly viz
  - SQLite for tabular data
  - 5,000-employee synthetic corpus calibrated to public HR-attrition distributions

KEY METRICS:
  - ROC-AUC: 0.91
  - PR-AUC: 0.74
  - Brier (calibration): 0.061
  - NL-to-SQL accuracy: 86% exact-match, 92% semantic-match
  - Latency: median 11.7s end-to-end (vs 2.3 days analyst baseline)

CURRENT GOALS:
  1. Get an AI/ML internship or full-time role (specifically pursuing Lumentum)
  2. Submit IEEE conference paper (target: IEEE Big Data Industry Track)
  3. arXiv preprint this week
  4. Coordinate LinkedIn launch with project

CONTEXT NOTES:
  - Built collaboratively with AI coding tools (Copilot, Claude, GPT-4) — disclosed in AI_CONTRIBUTIONS.md
  - All data is synthetic (no real PII)
  - MIT license
  - I am being interviewed by Lumentum (photonics/semiconductors)

Now help me with: [YOUR QUESTION HERE]
```

---

## 📚 Prompt Library — Common Tasks

### 🎯 Interview prep

```
Using the AttriSense project context above, please:
1. Give me 5 likely technical questions a Lumentum interviewer would ask about the predictive model.
2. For each, write a 60-second crisp answer in my voice (slightly informal, business-aware, technically precise).
3. Identify the one weakness in my project a sharp interviewer would attack — and how I should respond.
```

### 🎤 LinkedIn copywriting

```
I want to write a LinkedIn post about AttriSense. The audience is hiring managers and recruiters at Lumentum, and the broader AI/data community.

Constraints:
- First line must be a strong hook (scroll-stopper)
- 150-300 words total
- Tone: confident builder, business-first, humble-grateful
- Must tag the tools I used (OpenAI, LangChain, Streamlit, etc.)
- Must end with a single engagement question
- 12-15 hashtags max

Write 3 distinct variants — different opening hooks, same project.
```

### 📄 Paper section drafting

```
I need to expand Section 5 (Evaluation) of my IEEE paper on AttriSense. I have these raw numbers:
[paste your real model output here]

Write the section in IEEE conference style — formal, third-person, with proper subsection structure. Include a discussion of why PR-AUC matters more than ROC-AUC for this problem. Limit to 800 words.
```

### 🔍 Code review and improvement

```
Here's my predictive_engine.py file:
[paste code]

Act as a senior ML engineer reviewing this for production readiness. Specifically:
1. Identify any data-leakage risks
2. Suggest 3 highest-leverage improvements
3. Flag anything that would fail a hiring-manager code review
Keep it to bullet points, no fluff.
```

### 🎬 Video script

```
Write a 60-second video script for AttriSense aimed at LinkedIn auto-play.
- First 3 seconds must work without sound
- Captions must carry the meaning
- End with a clear CTA (visit GitHub URL)
- Include shot-by-shot timing
```

### 📊 Resume tailoring

```
Tailor my AttriSense project bullets for a [specific role at specific company] job description:

[paste JD here]

Use scaled metrics, action verbs, and the exact keywords from the JD where they fit honestly. 5 bullets max, ATS-optimized.
```

### 💡 Project extension brainstorm

```
Given the AttriSense project context, suggest 5 extensions that:
1. Would take 1-3 days each to build
2. Would meaningfully impress a hiring manager at a [specific company type]
3. Don't require any data I don't already have

For each, give: name, 1-line value prop, implementation outline, and how to demo it.
```

### 🔬 Patent brainstorm

```
Acting as a patent attorney specializing in software, review the AttriSense system architecture and identify:
1. The 2-3 most defensible novel-combination claims
2. For each, write a draft independent claim in proper patent language
3. Identify the closest prior art (IBM, Workday, Eightfold, Visier) and how my claim differs

I am preparing an Invention Disclosure Form for my university Tech Transfer office.
```

### 🎓 Faculty co-author pitch

```
Help me write an email to a CSUEB MSBA professor asking them to be a co-author on the AttriSense IEEE paper.
- Polite but not deferential
- Concrete about what I've already done
- Specific about what I'd want from them (review + co-authorship)
- Under 200 words
- Subject line included
```

### 🧪 Mock interview drill

```
You are a senior ML engineer at Lumentum interviewing me for a Data Scientist intern role.
Conduct a 10-question rapid-fire technical screen on AttriSense.
- Wait for my answer after each question
- Score each answer 1-10 and tell me what would have made it a 10
- After all 10, give me an overall hire/no-hire with one-paragraph reasoning
```

---

## 🛠️ Tool-specific tips

### **ChatGPT (GPT-4o / 4.5)**
- Best for: brainstorming, copy variants, quick refactors
- Tip: turn ON Custom Instructions with your AttriSense context (Settings → Personalization → Custom Instructions)
- Use Projects feature to keep AttriSense conversations together

### **Claude (3.7 / Opus 4)**
- Best for: long-form polish, paper writing, nuanced reasoning
- Tip: Claude handles long context windows beautifully — paste entire files
- Best at "act as senior engineer reviewing this code" prompts

### **Perplexity**
- Best for: researching Lumentum's recent press, leadership, public statements before the interview
- Prompt: *"Find recent news (last 6 months) on Lumentum's strategic priorities, any HR-tech or AI initiatives, and recent public statements by [interviewer name]."*

### **Gemini (advanced)**
- Best for: integration with Google Workspace if you draft in Docs
- Useful for analyzing screenshots if the recruiter sends architecture images

### **Cursor / Windsurf** (AI IDEs)
- Best for: actually editing the AttriSense codebase
- Tip: keep `AI_CONTRIBUTIONS.md` open as a reference tab so the AI adheres to your disclosure norms

---

## 🚨 Things to NEVER ask AI

- ❌ "Should I lie about when I built this on my resume?" — already answered: no, use the iteration framing
- ❌ Personal/financial decisions about Lumentum — those are yours alone
- ❌ Anything that requires real Lumentum-internal info — AI doesn't have it, will make stuff up
- ❌ Final wording of legally significant docs (patent claims, contracts) — get a human

---

## 📁 Save this file

Save this entire document to:
- A note in **Notion** / **Obsidian** / **Apple Notes**
- A pinned message in your own Telegram saved-messages
- Email it to yourself with subject "AttriSense AI Cheat Sheet"

You should be able to grab the master context block from any device in 10 seconds.
