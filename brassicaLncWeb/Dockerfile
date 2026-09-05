FROM python:3.11-slim-bookworm

ARG APP_UID=1000
ARG APP_GID=1000

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONPATH=/app/brassicaLncWeb:/app

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential gcc libpq-dev ncbi-blast+ \
    && rm -rf /var/lib/apt/lists/*

COPY requirements /app/requirements

RUN python -m pip install --upgrade pip \
    && pip install -r /app/requirements

COPY brassicaLncWeb /app/brassicaLncWeb

COPY brassicaLncWeb/docker-entrypoint.sh /app/brassicaLncWeb/docker-entrypoint.sh

RUN test "$APP_UID" -gt 0 && test "$APP_GID" -gt 0 \
    || { echo 'APP_UID and APP_GID must be positive (use 1000 when deploying as root).' >&2; exit 1; }

RUN groupadd --gid "$APP_GID" appuser \
    && useradd --create-home --uid "$APP_UID" --gid "$APP_GID" --shell /bin/sh appuser \
    && mkdir -p /app/brassicaLncWeb/staticfiles /app/brassicaLncWeb/media \
    && chown -R appuser:appuser /app \
    && chmod 0755 /app/brassicaLncWeb/staticfiles /app/brassicaLncWeb/media

WORKDIR /app/brassicaLncWeb

EXPOSE 8000

USER appuser

ENTRYPOINT ["/bin/sh", "/app/brassicaLncWeb/docker-entrypoint.sh"]
CMD ["gunicorn", "brassicaLncWeb.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "1", "--timeout", "120"]
