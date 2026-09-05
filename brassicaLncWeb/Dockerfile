FROM python:3.10-slim

ARG APP_UID=1000
ARG APP_GID=1000

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential gcc libpq-dev ncbi-blast+ \
    && rm -rf /var/lib/apt/lists/*

COPY requirements /app/requirements
COPY blast_rest /app/blast_rest

RUN python -m pip install --upgrade pip \
    && pip install -r /app/requirements

COPY brassicaLncWeb /app/brassicaLncWeb

COPY brassicaLncWeb/docker-entrypoint.sh /app/brassicaLncWeb/docker-entrypoint.sh

RUN groupadd --gid "$APP_GID" appuser \
    && useradd --create-home --uid "$APP_UID" --gid "$APP_GID" --shell /bin/sh appuser \
    && chown -R appuser:appuser /app \
    && mkdir -p /app/brassicaLncWeb/staticfiles /app/brassicaLncWeb/media \
    && chmod -R 0777 /app/brassicaLncWeb/staticfiles /app/brassicaLncWeb/media

WORKDIR /app/brassicaLncWeb

EXPOSE 8000

USER appuser

ENTRYPOINT ["/bin/sh", "/app/brassicaLncWeb/docker-entrypoint.sh"]
CMD ["gunicorn", "brassicaLncWeb.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "120"]