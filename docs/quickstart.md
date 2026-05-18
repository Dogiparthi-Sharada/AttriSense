<!--
AttriSense — docs/quickstart.md
Author : Sharada Dogiparthi <dogiparthi.sharada@gmail.com>
Version: 1.0.0
Date   : 2026-05-07
License: MIT — see LICENSE in repo root.
Copyright (c) 2026 Sharada Dogiparthi. All rights reserved.
-->

# Quickstart

Get the AttriSense dashboard running in **under five minutes** — on Windows, macOS, or Linux.

## TL;DR (the fastest path)

=== "Windows (PowerShell)"

    ```powershell
    git clone https://github.com/Dogiparthi-Sharada/AttriSense.git
    cd AttriSense
    py -3.11 -m venv .venv
    .\.venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    python launch_streamlit_app.py
    ```

=== "Windows (cmd.exe)"

    ```cmd
    git clone https://github.com/Dogiparthi-Sharada/AttriSense.git
    cd AttriSense
    py -3.11 -m venv .venv
    .venv\Scripts\activate.bat
    pip install -r requirements.txt
    python launch_streamlit_app.py
    ```

=== "macOS / Linux (bash/zsh)"

    ```bash
    git clone https://github.com/Dogiparthi-Sharada/AttriSense.git
    cd AttriSense
    python3.11 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    python launch_streamlit_app.py
    ```

=== "csh / tcsh"

    ```csh
    git clone https://github.com/Dogiparthi-Sharada/AttriSense.git
    cd AttriSense
    python3.11 -m venv .venv
    source .venv/bin/activate.csh
    pip install -r requirements.txt
    python launch_streamlit_app.py
    ```

Open the URL Streamlit prints — default `http://localhost:8503`. Done.

---

## Prerequisites

| Thing | Why | Check (Windows / Unix) |
|---|---|---|
| Python **3.11+** | langchain 1.0, EconML, type hints | `py --version` / `python --version` |
| `pip` | Package install | `pip --version` |
| ~1 GB disk | venv + indexes + SQLite db | `Get-PSDrive C` / `df -h .` |
| (optional) `OPENAI_API_KEY` | AI Assistant + multilingual RAG | `$env:OPENAI_API_KEY` / `echo $OPENAI_API_KEY` |
| (optional) Docker Desktop | Containerised run | `docker --version` |

The dashboard **runs without an OpenAI key**. Tabs that need an LLM fall back to deterministic local heuristics — see [AI Assistant](features/ai-assistant.md) and [Multilingual RAG](features/multilingual-rag.md).

### Installing Python 3.11+ on Windows

1. Download from [python.org/downloads](https://www.python.org/downloads/windows/) (the official installer).
2. **Tick "Add Python to PATH"** before clicking Install.
3. Verify in a new PowerShell:

    ```powershell
    py --version          # should print 3.11.x or higher
    py -3.11 --version    # explicit 3.11 selector
    ```

If you have multiple Python versions, the `py` launcher with `-3.11` is the safest way to be specific.

### Installing Git on Windows

[git-scm.com/download/win](https://git-scm.com/download/win) — accept defaults. Adds `git` to PATH and bundles a "Git Bash" shell that runs Linux-style commands if PowerShell feels alien.

---

## Step 1 — Clone the repo

=== "Windows (PowerShell)"

    ```powershell
    git clone https://github.com/Dogiparthi-Sharada/AttriSense.git
    cd AttriSense
    ```

=== "macOS / Linux"

    ```bash
    git clone https://github.com/Dogiparthi-Sharada/AttriSense.git
    cd AttriSense
    ```

## Step 2 — Create a virtual environment

=== "Windows (PowerShell)"

    ```powershell
    py -3.11 -m venv .venv
    .\.venv\Scripts\Activate.ps1
    ```

    !!! warning "Execution policy gotcha"
        If PowerShell rejects `Activate.ps1` with *"running scripts is disabled on this system"*, run this **once** in an elevated PowerShell:

        ```powershell
        Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
        ```

        Then retry activation.

=== "Windows (cmd.exe)"

    ```cmd
    py -3.11 -m venv .venv
    .venv\Scripts\activate.bat
    ```

=== "macOS / Linux"

    ```bash
    python3.11 -m venv .venv
    source .venv/bin/activate
    ```

=== "csh / tcsh"

    ```csh
    python3.11 -m venv .venv
    source .venv/bin/activate.csh
    ```

When the venv is active, your prompt shows `(.venv)` at the front.

## Step 3 — Install runtime dependencies

```bash
pip install -r requirements.txt
```

(Same on every platform — once the venv is active, `pip` is the venv's pip.)

For the production dashboard layer + dev tooling:

=== "Windows (PowerShell)"

    ```powershell
    cd production
    pip install -e ".[dev]"
    cd ..
    ```

=== "macOS / Linux"

    ```bash
    cd production
    pip install -e ".[dev]"
    cd ..
    ```

For the Causal Uplift extras (heavier; ~200 MB of EconML + numba):

```bash
cd production
pip install -e ".[causal]"
cd ..
```

## Step 4 — Generate data + train model

The repo ships with a pre-built `hr_enterprise.db` and `attrisense_model.joblib`. To regenerate from scratch (same on every platform once venv is active):

```bash
python generate_demo_workforce_data.py        # → attrisense_synthetic_hr.csv
python train_retention_risk_model.py          # → hr_enterprise.db, .joblib, calibration plots
python build_exit_interview_vector_index.py   # → faiss_hr_index/  (needs OPENAI_API_KEY)
```

Skip the third step if you don't have an OpenAI key — the AI Assistant simply hides itself.

## Step 5 — Run a dashboard

### Original demo (port 8503)

```bash
python launch_streamlit_app.py
```

### Production dashboard

=== "Windows (PowerShell)"

    ```powershell
    cd production
    streamlit run streamlit_app.py
    ```

    !!! note "About `make` on Windows"
        `make` is a Unix tool. On Windows you have three options:

        1. **Run the underlying commands directly** (as shown above — `streamlit run streamlit_app.py`).
        2. **Use Git Bash** (bundled with Git for Windows) — `make run` works there.
        3. **Install Make for Windows** — [GnuWin32 Make](http://gnuwin32.sourceforge.net/packages/make.htm) or `choco install make` if you use Chocolatey.

        Every `make <target>` in this project is just a shorthand for shell commands you can find in [`production/Makefile`](https://github.com/Dogiparthi-Sharada/AttriSense/blob/main/production/Makefile). See [Make targets](reference/make-targets.md) for direct equivalents.

=== "macOS / Linux"

    ```bash
    cd production
    make run                 # auto-picks a free port
    # OR
    streamlit run streamlit_app.py
    ```

### Docker

=== "Windows (PowerShell)"

    ```powershell
    cd production
    docker build -t attrisense:latest -f Dockerfile ..
    docker run --rm -p 8503:8503 --env-file ..\.env attrisense:latest
    ```

=== "macOS / Linux"

    ```bash
    cd production
    make docker-build
    make docker-run
    ```

Browse to `http://localhost:8503`.

## Step 6 — (Optional) Configure secrets

=== "Windows (PowerShell)"

    ```powershell
    Copy-Item .env.example .env
    # edit .env in any text editor and add: OPENAI_API_KEY=sk-...
    notepad .env
    ```

=== "Windows (cmd.exe)"

    ```cmd
    copy .env.example .env
    notepad .env
    ```

=== "macOS / Linux"

    ```bash
    cp .env.example .env
    chmod 600 .env
    # edit .env and add OPENAI_API_KEY=sk-...
    ```

The dashboard auto-loads `.env` at startup. See [Secrets handling](operations/secrets.md).

!!! warning "Don't commit `.env`"
    The repo's `.gitignore` already excludes it, but verify with `git status` before any commit. Keys leaked to git history are a rotation event — see [Secrets handling](operations/secrets.md#rotation-playbook).

---

## Verify everything works

=== "Windows (PowerShell)"

    ```powershell
    cd production
    pytest tests/ -v       # 31 tests should pass
    python -c "from attrisense.fairness import run_audit; print('fairness module OK')"
    ```

=== "macOS / Linux"

    ```bash
    cd production
    make test          # 31 pytest tests, expect 31 passed
    make fairness      # generates fairness_report.json
    make eval          # runs NL→SQL gold-question harness
    ```

=== "Windows direct equivalents"

    ```powershell
    cd production
    pytest tests/ -v
    python -m attrisense.fairness          # reads DB, writes outputs/fairness_report.json
    python -m attrisense.nl_sql_eval       # reads gold questions, writes outputs/nl_sql_eval_report.json
    ```

---

## What to click first

Open the dashboard, then:

1. **Executive** — see the KPI strip and risk distribution.
2. **SHAP Insights** — pick any high-risk employee, look at the waterfall.
3. **Compare** — drop two employee IDs side-by-side.
4. **Causal Uplift** — look at the recommended intervention column.
5. **Fairness** — confirm the four-fifths-rule failure flag (this is intentional — see [why](features/fairness-audit.md#what-it-answers)).

Then read [Architecture overview](architecture/overview.md) to understand what's happening behind each tab.

---

## Troubleshooting (the short list)

| Symptom | Fix |
|---|---|
| `ModuleNotFoundError: No module named 'streamlit'` | venv not activated. PowerShell: `.\.venv\Scripts\Activate.ps1`. Bash: `source .venv/bin/activate`. |
| `running scripts is disabled on this system` (PowerShell) | `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned` once. |
| `'make' is not recognized` (Windows) | Use the direct `streamlit run ...` command, or run from Git Bash. |
| `OperationalError: no such table: workforce_predictions` | Run `python train_retention_risk_model.py`. |
| `openai.APIConnectionError: Connection error` | Corporate firewall. The dashboard auto-falls back to local hashing embeddings — no action needed. See [troubleshooting](troubleshooting.md#openai-connection-error). |
| KeyError on Compare tab | Old version. Pull latest — the fix is in [`production/src/attrisense/compare.py`](https://github.com/Dogiparthi-Sharada/AttriSense/blob/main/production/src/attrisense/compare.py). |
| Streamlit port already in use | `streamlit run streamlit_app.py --server.port 8502` |
| `py: command not found` (Windows) | The Python launcher wasn't installed. Re-run the python.org installer and tick "Install launcher for all users". |

The full guide lives at [Troubleshooting](troubleshooting.md).
