<!--
AttriSense — docs/operations/docker.md
Author : Sharada Dogiparthi <dogiparthi.sharada@gmail.com>
Version: 1.0.0
Date   : 2026-05-07
License: MIT — see LICENSE in repo root.
Copyright (c) 2026 Sharada Dogiparthi. All rights reserved.
-->

# Docker

> A reproducible container for the production dashboard.

!!! tip "Windows users"
    Install **Docker Desktop for Windows** with the WSL 2 backend. All commands below work in PowerShell, cmd.exe, and Git Bash — only the path-separator and shell-substitution syntax differ.

## Build

=== "Linux / macOS / Git Bash"

    ```bash
    cd production
    make docker-build
    # OR
    docker build -t attrisense:latest -f Dockerfile ..
    ```

=== "PowerShell"

    ```powershell
    cd production
    docker build -t attrisense:latest -f Dockerfile ..
    ```

=== "cmd.exe"

    ```cmd
    cd production
    docker build -t attrisense:latest -f Dockerfile ..
    ```

The build context is the **parent** directory (`..`) so the image can copy in `requirements.txt`, `streamlit_app.py`, the trained model, and the SQLite DB.

Build time: ~3 minutes from clean. Image size: ~720 MB compressed.

## Run

=== "Linux / macOS / Git Bash"

    ```bash
    make docker-run
    # OR
    docker run --rm -p 8501:8501 \
      --env-file ../.env \
      -v $(pwd)/../outputs:/app/outputs \
      attrisense:latest
    ```

=== "PowerShell"

    ```powershell
    docker run --rm -p 8501:8501 `
      --env-file ..\.env `
      -v ${PWD}\..\outputs:/app/outputs `
      attrisense:latest
    ```

=== "cmd.exe"

    ```cmd
    docker run --rm -p 8501:8501 ^
      --env-file ..\.env ^
      -v %cd%\..\outputs:/app/outputs ^
      attrisense:latest
    ```

Browse to `http://localhost:8501`.

## What's in the image

| | |
|---|---|
| Base | `python:3.11-slim` |
| User | non-root `appuser` (UID 1000) |
| Working dir | `/app` |
| Entrypoint | `streamlit run production/streamlit_app.py --server.port 8501 --server.address 0.0.0.0 --server.headless true` |
| Exposed port | 8501 |
| Health check | `curl -fsS http://localhost:8501/_stcore/health` |

## Layers (rough)

| Layer | Size | What |
|---|---|---|
| `python:3.11-slim` | ~120 MB | Base |
| `pip install -r requirements.txt` | ~520 MB | Streamlit, sklearn, SHAP, lifelines, langchain, FAISS, plotly |
| `pip install -e production[causal]` | ~80 MB | EconML + transitive |
| App code + data | ~10 MB | Repo files |

EconML is the dominant non-base size. Drop it (and the Causal Uplift tab) by removing `[causal]` from the install line in the Dockerfile if you need a slimmer image.

## Configuration via env vars

Anything in `.env` works the same way in the container:

```bash
docker run -e OPENAI_API_KEY=$OPENAI_API_KEY \
           -e LANGCHAIN_TRACING_V2=true \
           -p 8501:8501 attrisense
```

Or use `--env-file` (path separators per shell):

=== "Linux / macOS / Git Bash"

    ```bash
    docker run --env-file ../.env -p 8501:8501 attrisense
    ```

=== "PowerShell / cmd"

    ```powershell
    docker run --env-file ..\.env -p 8501:8501 attrisense
    ```

## Volume mounts

To persist `outputs/` (fairness reports, eval reports, screenshots) between runs:

```bash
docker run --rm -p 8501:8501 \
  -v $(pwd)/../outputs:/app/outputs \
  attrisense
```

To persist the FAISS multilingual index:

```bash
-v $(pwd)/../data/multilingual_index:/app/data/multilingual_index
```

## Multi-stage Dockerfile?

Not currently used. The bottleneck is `pip install`, not artifact copying. A multi-stage build would shave ~30 MB off the final image — not worth the complexity for this project.

When that becomes worth it: split into `builder` (full build deps) and `runtime` (just the wheel cache + slim base).

## Production hardening checklist

If you actually deploy this:

- [ ] Pin all dependency versions (`requirements.txt` already does this — keep it that way)
- [ ] Run as non-root (already done)
- [ ] Add Trivy / Grype scanning to CI
- [ ] Sign the image (`cosign sign`)
- [ ] Push to a private registry, not Docker Hub
- [ ] Configure log shipping (the container logs to stdout — pick that up)
- [ ] Add a readiness probe alongside the health probe
- [ ] Set memory limits (`--memory 1.5g`) — RF + SHAP + EconML need ~1 GB peak
- [ ] If exposing publicly: terminate TLS at the load balancer, not in the container

## docker-compose

Not provided. The single-container deployment doesn't need it. If you want one, it's three lines:

```yaml
services:
  attrisense:
    build: { context: ., dockerfile: production/Dockerfile }
    ports: ["8501:8501"]
    env_file: .env
```

## Troubleshooting

| Symptom | Fix |
|---|---|
| Build hangs at `pip install` | Network issue inside Docker. Check proxy settings. |
| `Permission denied` on `outputs/` | Volume mount permissions. Run `chown -R 1000 outputs/` on the host. |
| Health check fails on first run | `model.joblib` or `hr_enterprise.db` missing. Either rebuild image after running `train_retention_risk_model.py`, or mount them in. |
| OOM killed | Increase Docker memory to ≥2 GB. EconML + SHAP are memory-hungry. |
