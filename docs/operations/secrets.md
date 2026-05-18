<!--
AttriSense — docs/operations/secrets.md
Author : Sharada Dogiparthi <dogiparthi.sharada@gmail.com>
Version: 1.0.0
Date   : 2026-05-07
License: MIT — see LICENSE in repo root.
Copyright (c) 2026 Sharada Dogiparthi. All rights reserved.
-->

# Secrets handling

> Treat every key like it's already leaked. Plan for rotation, not perfection.

## The 30-second rule

If a key has been pasted in a Slack channel, an email, a screenshot, a log line, or **any LLM chat box** (including this conversation), **rotate it now**. Don't reason about whether the rotation is necessary. Rotate.

## What AttriSense uses

| Secret | Purpose | Required? |
|---|---|---|
| `OPENAI_API_KEY` | NL→SQL Assistant + multilingual embeddings | Optional — both have fallbacks |
| `LANGCHAIN_API_KEY` | LangSmith tracing | Optional — only if you want chain logs in LangSmith |

The dashboard runs fully without either.

## Where to put the key

### ✅ Right way: `.env` at repo root

```bash
cp .env.example .env
chmod 600 .env       # owner-only read
```

Edit `.env`:

```bash
OPENAI_API_KEY=sk-proj-...
```

The dashboard auto-loads it via `python-dotenv` at startup. The file is git-ignored ([`.gitignore` line 58](https://github.com/Dogiparthi-Sharada/AttriSense/blob/main/.gitignore)) — `git status` will not show it.

### ❌ Wrong ways

- ✗ `export OPENAI_API_KEY=...` in `~/.bashrc` / `~/.cshrc` — leaks to every process you ever run.
- ✗ Hardcoding in any `.py` file — even temporarily.
- ✗ Pasting into the dashboard UI as a "config" field — never built.
- ✗ Committing to a private branch "just to test CI" — git history is forever.

## Verifying it's loaded

```bash
cd /path/to/AttriSense
.venv/bin/python -c "
from dotenv import load_dotenv
import os
load_dotenv()
print('OPENAI_API_KEY set:', bool(os.getenv('OPENAI_API_KEY')))
"
```

Expected: `OPENAI_API_KEY set: True`.

If `False`:
- Check the file exists: `ls -la .env`
- Check the format — no spaces around `=`, no quotes needed.
- Check working directory — you must run from the repo root, OR rely on the auto-load (the production dashboard does explicit `load_dotenv(dotenv_path=_REPO_ROOT / ".env")`).

## Rotation playbook

1. Generate a new key in the OpenAI dashboard.
2. Update `.env` locally.
3. Update Streamlit Community Cloud / Vercel / wherever else.
4. Update CI secrets if any.
5. **Revoke the old key** immediately — don't wait for "next maintenance window".
6. Verify the dashboard still works.

OpenAI's UI lets you scope new keys to specific projects with usage caps — use that.

## Pre-commit hook (optional but recommended)

Block accidental commits of `sk-` patterns:

```bash
# .git/hooks/pre-commit  (chmod +x)
#!/bin/bash
if git diff --cached -U0 | grep -E "sk-[A-Za-z0-9_-]{20,}" > /dev/null; then
  echo "ERROR: looks like an OpenAI key in your staged diff. Aborting."
  exit 1
fi
```

For team-scale, use [`gitleaks`](https://github.com/gitleaks/gitleaks) wired into CI.

## Streamlit Community Cloud

Use the **Secrets** UI in the app settings — never put the key in the repo even on a private fork.

```toml
# Pasted into Streamlit Cloud secrets UI
OPENAI_API_KEY = "sk-proj-..."
```

Streamlit injects them as env vars at runtime; the same `os.getenv("OPENAI_API_KEY")` works.

## Docker

```bash
docker run --env-file .env -p 8503:8503 attrisense
```

Or pass individually:

```bash
docker run -e OPENAI_API_KEY=$OPENAI_API_KEY -p 8503:8503 attrisense
```

Never bake the key into the image — `docker history` exposes layer commands.

## Real production

For a hosted deployment with multiple environments (staging, prod):

| Tool | Use case |
|---|---|
| AWS Secrets Manager | If you're on AWS |
| HashiCorp Vault | If you're not on a single cloud |
| Doppler / Infisical | Lightweight SaaS managers |
| 1Password CLI | Small teams, devs only |

The pattern is the same: secrets manager → env vars at runtime → `os.getenv("OPENAI_API_KEY")`. The application code never changes.

## What about the synthetic data?

`attrisense_synthetic_hr.csv` and `hr_enterprise.db` are **safe to commit** — they're 100% synthetic, generated from `RANDOM_SEED=42`, with no PII.

They're committed to keep the repo clone-and-run. A real deployment would .gitignore them and provide a `make data` target instead.
