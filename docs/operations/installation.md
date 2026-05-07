# Installation

> Three paths: local Python, Docker, or Streamlit Community Cloud.

## Path A — Local Python (recommended for development) {#path-a--local-python-recommended-for-development}

### 1. Prereqs

- Python **3.11+** (3.10 will not work — `langchain 1.0` requires 3.11)
- `pip` (any recent version)
- `git`
- ~500 MB disk space
- (Optional) `OPENAI_API_KEY` for AI Assistant + multilingual RAG

!!! tip "Windows users"
    Install Python via [python.org](https://www.python.org/downloads/) (check **Add python.exe to PATH** + **py launcher**) or `winget install Python.Python.3.11`. Install Git via [git-scm.com](https://git-scm.com/download/win) — this also gives you a **Git Bash** shell that mimics Linux.

### 2. Clone

=== "PowerShell / cmd / bash"

    ```bash
    git clone https://github.com/Dogiparthi-Sharada/AttriSense.git
    cd AttriSense
    ```

### 3. Virtual environment

=== "PowerShell"

    ```powershell
    py -3.11 -m venv .venv
    .\.venv\Scripts\Activate.ps1
    ```

    If you see *"running scripts is disabled on this system"*:

    ```powershell
    Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
    ```

=== "cmd.exe"

    ```cmd
    py -3.11 -m venv .venv
    .venv\Scripts\activate.bat
    ```

=== "bash / zsh / Git Bash"

    ```bash
    python3.11 -m venv .venv
    source .venv/bin/activate
    # Git Bash on Windows uses: source .venv/Scripts/activate
    ```

=== "csh / tcsh"

    ```csh
    python3.11 -m venv .venv
    source .venv/bin/activate.csh
    ```

### 4. Install runtime dependencies

```bash
pip install -r requirements.txt
```

### 5. Install dev dependencies (optional but recommended)

```bash
cd production
pip install -e ".[dev]"
cd ..
```

### 6. Install causal extras (only if you'll use the Causal Uplift tab)

```bash
cd production
pip install -e ".[causal]"
cd ..
```

EconML is heavy (~200 MB with transitive deps). Skip if you're only here for the standard ML tabs.

### 7. Verify

=== "Linux / macOS / Git Bash"

    ```bash
    cd production && make test
    ```

=== "PowerShell / cmd (no make)"

    ```powershell
    cd production
    pytest tests/ -v
    ```

Expected output:

```
======== 31 passed in 4.23s ========
```

### 8. Run

=== "Linux / macOS"

    ```bash
    # Original demo
    python launch_streamlit_app.py
    # OR Production dashboard
    make -C production run
    ```

=== "PowerShell / cmd"

    ```powershell
    # Original demo
    python launch_streamlit_app.py
    # OR Production dashboard (no make required)
    streamlit run production\streamlit_app.py
    ```

!!! info "`make` on Windows"
    Windows has no `make` by default. Either (a) use the direct `streamlit run ...` / `pytest ...` commands shown above, (b) run inside **Git Bash** which ships with `make`, or (c) `choco install make` / `winget install GnuWin32.Make`.

## Path B — Docker

=== "Linux / macOS / Git Bash"

    ```bash
    cd production
    make docker-build
    make docker-run
    ```

=== "PowerShell / cmd"

    ```powershell
    cd production
    docker build -t attrisense:latest -f Dockerfile ..
    docker run --rm -p 8501:8501 --env-file ..\.env attrisense:latest
    ```

The image is `python:3.11-slim` based, ~720 MB compressed. The container exposes port 8501. Override with `-p 8080:8501` if needed.

For the full Docker walk-through see [Docker](docker.md).

## Path C — Streamlit Community Cloud

1. Fork the repo to your GitHub account.
2. Sign in to [share.streamlit.io](https://share.streamlit.io).
3. Click **Deploy an app**.
4. Select your fork → branch `main` → entry point `streamlit_app.py` (or `production/streamlit_app.py`).
5. Add secrets via the Streamlit UI:
   ```toml
   OPENAI_API_KEY = "sk-..."
   ```
6. Deploy. Public URL appears in ~60 seconds.

## Disk usage

| Item | Size |
|---|---|
| `.venv` (full install incl. EconML) | ~800 MB |
| `attrisense_synthetic_hr.csv` | ~2 MB |
| `hr_enterprise.db` | ~4 MB |
| `attrisense_model.joblib` | ~6 MB |
| `faiss_hr_index/` | < 1 MB |
| `outputs/` | ~1 MB |

## CSH-specific gotchas

If your shell is `csh` or `tcsh`:

- Use `source .venv/bin/activate.csh` (not `.sh`).
- Multi-line `bash -c '...'` commands may need a wrapper script. See the [Vanama csh notes](../troubleshooting.md#csh-quirks) (well-documented warning sign in this codebase).

## Uninstall

=== "Linux / macOS"

    ```bash
    deactivate
    rm -rf .venv production/.venv
    rm -f hr_enterprise.db attrisense_model.joblib attrisense_synthetic_hr.csv
    rm -rf faiss_hr_index data/multilingual_index outputs/*
    ```

=== "PowerShell"

    ```powershell
    deactivate
    Remove-Item -Recurse -Force .venv, production\.venv
    Remove-Item -Force hr_enterprise.db, attrisense_model.joblib, attrisense_synthetic_hr.csv -ErrorAction SilentlyContinue
    Remove-Item -Recurse -Force faiss_hr_index, data\multilingual_index, outputs\* -ErrorAction SilentlyContinue
    ```

=== "cmd.exe"

    ```cmd
    deactivate
    rmdir /s /q .venv production\.venv
    del /q hr_enterprise.db attrisense_model.joblib attrisense_synthetic_hr.csv
    rmdir /s /q faiss_hr_index data\multilingual_index
    ```

## Common installation errors

| Error | Fix |
|---|---|
| `ERROR: Could not find a version that satisfies langchain` | You're on Python 3.10 or older. Upgrade to 3.11+. |
| `Microsoft Visual C++ 14.0 is required` (Windows) | Install [Visual C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/). |
| `error: Failed building wheel for shap` (M-series Mac) | `brew install libomp` first, then `pip install shap`. |
| `error: legacy-install-failure` for `econml` | Skip it: `pip install -r requirements.txt` without the `[causal]` extra. The dashboard runs without it. |
| `ImportError: numpy.core.multiarray failed to import` | `pip install numpy --upgrade`. |
