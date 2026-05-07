# Multi-stage build for the AttriSense v2 dashboard.
# Stage 1: build environment with all wheels.
# Stage 2: slim runtime that only ships the venv + source.

FROM python:3.11-slim AS builder

ENV PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /build

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN python -m venv /opt/venv \
    && /opt/venv/bin/pip install --upgrade pip \
    && /opt/venv/bin/pip install -r requirements.txt \
    && /opt/venv/bin/pip install econml>=0.15

# ---- Runtime stage ----
FROM python:3.11-slim AS runtime

ENV PATH=/opt/venv/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/production/src:/app

WORKDIR /app

# Bring in the prebuilt venv from the builder stage.
COPY --from=builder /opt/venv /opt/venv

# Copy only the runtime payload.
COPY config.py ./
COPY natural_language_sql.py ./
COPY streamlit_app.py ./
COPY launch_streamlit_app.py ./
COPY generate_demo_workforce_data.py ./
COPY train_retention_risk_model.py ./
COPY build_exit_interview_vector_index.py ./
COPY .streamlit ./.streamlit
COPY production ./production

# Generate data + train at build time so the image is self-contained.
RUN python generate_demo_workforce_data.py \
    && python train_retention_risk_model.py

# Drop privileges.
RUN useradd --create-home --uid 10001 attrisense \
    && chown -R attrisense:attrisense /app
USER attrisense

EXPOSE 8501
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD curl --fail --silent http://127.0.0.1:8501/_stcore/health || exit 1

CMD ["streamlit", "run", "production/streamlit_app.py", \
     "--server.address=0.0.0.0", "--server.port=8501", \
     "--server.headless=true", "--browser.gatherUsageStats=false"]
