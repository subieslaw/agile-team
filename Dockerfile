# ── Stage 1: builder ──────────────────────────────────────────────────────────
FROM python:3.13-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:0.5 /uv /usr/local/bin/uv

ENV UV_NO_PROGRESS=1 \
    UV_SYSTEM_PYTHON=0 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /build

# Install runtime dependencies first (cached layer — only invalidated when lock changes)
COPY pyproject.toml uv.lock ./
RUN uv venv /opt/venv && \
    uv sync \
        --frozen \
        --no-dev \
        --no-install-project \
        --python /opt/venv/bin/python

# Install the application package itself
COPY src/ ./src/
COPY migrations/ ./migrations/
COPY alembic.ini ./
RUN uv pip install \
        --python /opt/venv/bin/python \
        --no-deps \
        .


# ── Stage 2: final ────────────────────────────────────────────────────────────
FROM python:3.13-slim AS final

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

RUN groupadd --gid 1001 appgroup && \
    useradd  --uid 1001 --gid appgroup --no-create-home --shell /sbin/nologin appuser

COPY --from=builder --chown=appuser:appgroup /opt/venv      /opt/venv
COPY --from=builder --chown=appuser:appgroup /build/alembic.ini /app/alembic.ini
COPY --from=builder --chown=appuser:appgroup /build/migrations  /app/migrations

COPY --chown=appuser:appgroup entrypoint.sh /entrypoint.sh

WORKDIR /app
USER appuser

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
