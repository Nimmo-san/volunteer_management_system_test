# Build stage
FROM python:3.12-slim AS builder

RUN mkdir /app

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy project metadata and install dependencies
COPY backend/pyproject.toml ./

# If using setup.cfg / setup.py
# COPY setup.cfg setup.py ./

RUN pip install --upgrade pip && pip install .

# Prod stage
FROM python:3.12-slim

RUN useradd -m -r appuser && \
    mkdir /app && \
    chown -R appuser /app


COPY --from=builder /usr/local/lib/python3.12/site-packages/ /usr/local/lib/python3.12/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

WORKDIR /app

# Now copy the actual project code
# COPY . .
COPY --chown=appuser:appuser . .

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

# Environment, unsure about this one
ENV DJANGO_SETTINGS_MODULE=config.settings.prod

USER appuser

# Expose gunicorn port
EXPOSE 8000

RUN ["chmod", "+x", "/app/entrypoint.prod.sh"]

CMD ["/app/entrypoint.prod.sh"]
# CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]