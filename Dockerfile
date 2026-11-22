# ==============================================================================
# Production Dockerfile for AI Link Analysis API
# Python 3.12-slim base with non-root security execution & healthcheck
# ==============================================================================

FROM python:3.12-slim AS base

# System environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    APP_PORT=4000

# Install runtime security packages & curl for Docker healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Create unprivileged system user and group
RUN groupadd -r appuser && useradd -r -g appuser -d /home/appuser -m -s /bin/bash appuser

# Set workspace directory
WORKDIR /app

# Install Python dependencies first (leveraging Docker layer caching)
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code and configuration
COPY app/ /app/app/
COPY README.md /app/README.md

# Set ownership to unprivileged user
RUN chown -R appuser:appuser /app

# Switch to unprivileged user
USER appuser

# Expose API port
EXPOSE 4000

# Container healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://127.0.0.1:4000/health || exit 1

# Launch production ASGI server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "4000"]
