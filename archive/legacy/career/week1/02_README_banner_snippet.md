# README banner snippet

> Paste this at the very top of `README.md`, immediately under the
> project title. It serves three purposes simultaneously:
> 1. Eliminates any "is this real PII?" objection from a recruiter
> 2. Makes the live demo and paper *one click away*
> 3. Establishes professional polish in the first 5 seconds

---

```markdown
# AttriSense
*Open-source workforce intelligence — predictive flight-risk + RAG over exit interviews + NL→SQL*

[![Live Demo](https://img.shields.io/badge/Live_Demo-Streamlit-FF4B4B?logo=streamlit)](https://attrisense.streamlit.app)
[![arXiv](https://img.shields.io/badge/arXiv-preprint-b31b1b?logo=arxiv)](https://arxiv.org/abs/XXXX.XXXXX)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/)
[![Made with Streamlit](https://img.shields.io/badge/Made%20with-Streamlit-FF4B4B?logo=streamlit)](https://streamlit.io)

> **🛡️ Synthetic Data Notice.** This project ships with a
> 5,000-employee **fully synthetic** dataset, generated programmatically
> and calibrated against published HR-attrition distributions. **No real
> employee data, no PII, no proprietary information** is included or used.
> The system is designed to be re-pointed at any HRIS (Workday,
> BambooHR, ADP) for production deployment.

> **🎓 Origin.** Originally developed as an MSBA capstone project at
> California State University, East Bay. Generalized into the
> open-source AttriSense platform for community use.

> **🤖 AI Disclosure.** This codebase was developed with the
> assistance of LLM coding tools (GitHub Copilot, Claude, GPT-4).
> See [`AI_CONTRIBUTIONS.md`](AI_CONTRIBUTIONS.md) for full transparency.

---

## ⚡ Evaluate this project in 5 minutes (for hiring managers)

1. **See the live app** → [attrisense.streamlit.app](https://attrisense.streamlit.app) — interactive dashboard, no install needed
2. **Watch the 60-second demo** → [demo.mp4](doc/demo.mp4)
3. **Skim the architecture** → [doc/architecture.png](doc/architecture.png)
4. **Read the paper** → [paper/attrisense_ieee.pdf](paper/attrisense_ieee.pdf) or [arXiv preprint](https://arxiv.org/abs/XXXX.XXXXX)
5. **Read the AI-use disclosure** → [AI_CONTRIBUTIONS.md](AI_CONTRIBUTIONS.md)

If you'd rather run it locally:
```bash
git clone https://github.com/Dogiparthi-Sharada/attrisense.git
cd attrisense && pip install -r requirements.txt
streamlit run dashboard.py
```

---
```

After this banner, keep your existing README content (Features, Architecture, etc.).
