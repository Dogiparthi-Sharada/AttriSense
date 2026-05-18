<!--
AttriSense — docs/troubleshooting.md
Author : Sharada Dogiparthi <dogiparthi.sharada@gmail.com>
Version: 1.0.0
Date   : 2026-05-07
License: MIT — see LICENSE in repo root.
Copyright (c) 2026 Sharada Dogiparthi. All rights reserved.
-->

# Troubleshooting

> Every error we've personally hit while building AttriSense, with the fix.

## Dashboard won't start

### `ModuleNotFoundError: No module named 'streamlit'`

Virtual environment isn't active.

=== "PowerShell"

    ```powershell
    .\.venv\Scripts\Activate.ps1
    ```

=== "cmd.exe"

    ```cmd
    .venv\Scripts\activate.bat
    ```

=== "bash / zsh"

    ```bash
    source .venv/bin/activate
    ```

=== "csh / tcsh"

    ```csh
    source .venv/bin/activate.csh
    ```

If `.venv` doesn't exist, see [Installation](operations/installation.md#path-a--local-python-recommended-for-development).

### `OperationalError: no such table: workforce_predictions`

The SQLite DB hasn't been built.

```bash
python train_retention_risk_model.py
```

This creates `hr_enterprise.db` with all four tables in ~12 seconds.

### `Address already in use` / port conflict

Streamlit's default port (8503) is taken.

```bash
streamlit run streamlit_app.py --server.port 8502
# OR for v2
make -C production run     # auto-picks a free port
```

## OpenAI / AI Assistant errors

### `openai.APIConnectionError: Connection error.` {#openai-connection-error}

You're behind a corporate firewall that blocks `api.openai.com`. **The dashboard handles this automatically** — the multilingual RAG falls back to local hashing embeddings, and the AI Assistant falls back to the TF-IDF gold-question ranker.

If you saw the error as a Streamlit traceback, you're on an older version. Pull the latest `production/src/attrisense/multilingual_rag.py` — the fix added a reachability probe + per-provider index dirs + mid-query fallback.

Verify:

```bash
.venv/bin/python -c "
from attrisense.multilingual_rag import search
results = search('compensation issues', top_k=3)
print('provider:', results[0]['provider'])
"
```

Expected output: `provider: hashing` (when firewall is in the way) or `provider: openai` (when reachable).

### `OPENAI_API_KEY is not set` (but I have a `.env` file)

The dashboard wasn't loading `.env` because Streamlit's working directory differs from where you ran the launch command.

**Fix is in place** in `production/streamlit_app.py`:

```python
load_dotenv(dotenv_path=_REPO_ROOT / ".env", override=False)
```

Verify the key is loaded:

```bash
cd /path/to/AttriSense
.venv/bin/python -c "
from dotenv import load_dotenv
import os
load_dotenv()
print('Set:', bool(os.getenv('OPENAI_API_KEY')))
"
```

Should print `Set: True`. If `False`:
- File exists? `ls -la .env`
- Format is `OPENAI_API_KEY=sk-...` (no spaces, no quotes)?
- File permissions allow reading? `chmod 600 .env`

### `AuthenticationError: Incorrect API key`

The key is malformed or revoked.

1. Generate a new one in the OpenAI dashboard.
2. Update `.env`.
3. **Revoke the old key** immediately.

Don't paste a key into Slack, email, or any chat (including this one). If you ever do, rotate.

## SHAP / Compare tab errors

### `KeyError: True` on Compare tab

You're on an old version. The fix:

```python
# Wrong (SQLite stores booleans as ints):
explained = df[df["SHAP_Explained"]]
# Right:
explained = df[df["SHAP_Explained"].astype(bool)]
```

The fix is in [`production/src/attrisense/compare.py`](https://github.com/Dogiparthi-Sharada/AttriSense/blob/main/production/src/attrisense/compare.py) and regression-tested by [`test_compare.py`](https://github.com/Dogiparthi-Sharada/AttriSense/blob/main/production/tests/test_compare.py).

### Empty drivers list for an employee

That employee has `SHAP_Explained = 0` — SHAP values weren't stored for them. The dashboard only stores SHAP for high-risk + a sampled subset to keep the DB compact.

To force SHAP for everyone, edit `train_retention_risk_model.py` to remove the sampling and set `SHAP_Explained = 1` for all rows. Expect the DB size to grow ~10×.

## Multilingual RAG errors

### `'HashingEmbeddings' object is not callable`

You're on a version of `multilingual_rag.py` from before the `Embeddings` inheritance fix. Update to the latest — `HashingEmbeddings(Embeddings)` must inherit from `langchain_core.embeddings.Embeddings`.

### `dimension mismatch` from FAISS

The FAISS index on disk was built with one provider (1536-dim OpenAI) and you're now loading it with another (256-dim hashing). The fix is in place — per-provider dirs:

```
data/multilingual_index/
├── openai/    ← 1536-dim
└── hashing/   ← 256-dim
```

If you see this error after a hand-edit, just delete `data/multilingual_index/` and let the dashboard rebuild on next query.

## Windows / PowerShell quirks {#windows-quirks}

| Symptom | Cause | Fix |
|---|---|---|
| `Activate.ps1 cannot be loaded because running scripts is disabled` | Default PowerShell execution policy | `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned` |
| `'make' is not recognized as an internal or external command` | Windows has no `make` | Use direct commands (`streamlit run ...`, `pytest tests/`), or run inside Git Bash, or `choco install make` |
| `'py' is not recognized` | Python launcher not installed | Reinstall Python from python.org with **"py launcher"** checked, or use `python` directly if it's on PATH |
| `Microsoft Visual C++ 14.0 is required` building wheels | Native build deps missing | Install [Visual C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/) |
| Backslash paths break in scripts | Mixing forward/back slashes | In PowerShell prefer `Join-Path`; in Python use `pathlib.Path` |
| `--env-file ../.env` says file not found | Wrong separator on Windows | Use `..\.env` in PowerShell/cmd |
| Line continuation broken | `\` is not a continuation char in PowerShell/cmd | Use backtick `` ` `` in PowerShell, caret `^` in cmd.exe |
| Port 8503 in use | Another Streamlit running | `Get-Process | Where-Object { $_.ProcessName -like 'python*' } | Stop-Process` (PowerShell) or pick a new port `streamlit run ... --server.port 8502` |

## CSH / TCSH quirks {#csh-quirks}

This dev environment may use `csh`, which has multiple quirks vs. bash:

| Symptom | Cause | Fix |
|---|---|---|
| `Ambiguous output redirect` | csh can't do `2>/dev/null` | Use `>& /dev/null` or wrap in `bash -c '...'` |
| `Variable name must contain alphanumeric characters` | csh can't do `$()` substitution inline | Wrap in bash script |
| `Unmatched '"'` from multi-line command | csh tokenises line-by-line | Write to `/tmp/foo.sh`, run with `bash /tmp/foo.sh` |
| Backtick fails in `set` | csh limitations | Use bash |

The pattern that always works: write your script to `/tmp/foo.sh`, then run `bash /tmp/foo.sh`. Never put multi-line `bash -c '...'` directly in a csh prompt.

## Theme / palette issues

### "Background is too white"

You're seeing the original `streamlit_app.py` (Streamlit default theme) instead of v2. Run the production dashboard:

```bash
make -C production run
```

The production theme lives in [`production/src/attrisense/theme.py`](https://github.com/Dogiparthi-Sharada/AttriSense/blob/main/production/src/attrisense/theme.py) — deep slate canvas + cyan/indigo accent.

### Charts have white backgrounds inside the dark theme

A chart was created without `apply_plotly_defaults(fig)`. Wrap it:

```python
from attrisense.theme import apply_plotly_defaults
fig = px.bar(...)
fig = apply_plotly_defaults(fig)
st.plotly_chart(fig)
```

## Test failures

### `pytest` collects 0 tests

You're in the wrong directory. Tests live under `production/tests/`:

```bash
cd production
pytest tests/ -v
```

### Specific test fails after a code change

Run only that test for a faster loop:

```bash
pytest production/tests/test_compare.py::test_headline_drivers_returns_top_n -vv
```

Add `-vv` for full assertion diffs. Add `--pdb` to drop into the debugger on failure.

## Streamlit cache stuck

If the dashboard shows old data after retraining:

```python
# Click the hamburger menu → "Clear cache"
# OR press 'C' on the dashboard
# OR restart streamlit
```

For aggressive clear:

```bash
rm -rf .streamlit/.cache
# restart streamlit
```

## I retrained the model but the dashboard is showing old numbers

`@st.cache_data` retains the DataFrame for the session. Press `R` in the browser to rerun, or click "Clear cache" from the hamburger menu.

## Docker container won't start

### `port already allocated`

Another container already on 8503.

```bash
docker ps
docker stop <other_container>
# OR map to a different host port
docker run -p 8502:8503 attrisense
```

### Health check fails on first run

The DB or model file is missing inside the container. Either:

- Rebuild the image after generating these files.
- Mount them in: `-v $(pwd)/hr_enterprise.db:/app/hr_enterprise.db -v $(pwd)/attrisense_model.joblib:/app/attrisense_model.joblib`.

## Still stuck?

- File an issue on the [GitHub repo](https://github.com/Dogiparthi-Sharada/AttriSense/issues).
- Include: OS, Python version, the exact command you ran, full traceback, and `pip freeze` output.
- Search existing issues first — somebody else may have hit it.
