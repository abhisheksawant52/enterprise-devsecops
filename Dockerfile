# syntax=docker/dockerfile:1

FROM python:3.12-slim AS builder

WORKDIR /build

COPY pyproject.toml requirements.txt ./
COPY src ./src
COPY README.md ./

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir --prefix=/install .

FROM python:3.12-slim AS runtime

LABEL org.opencontainers.image.title="enterprise-devsecops" \
      org.opencontainers.image.description="Enterprise DevSecOps platform service" \
      org.opencontainers.image.licenses="MIT" \
      org.opencontainers.image.source="https://github.com/abhisheksawant52/enterprise-devsecops"

RUN addgroup --system edsec && adduser --system --ingroup edsec --home /app edsec

WORKDIR /app

COPY --from=builder /install /usr/local
COPY policies ./policies

USER edsec

ENV EDSEC_HOST=0.0.0.0 \
    EDSEC_PORT=8080 \
    PYTHONUNBUFFERED=1

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8080/health', timeout=3)" || exit 1

ENTRYPOINT ["uvicorn", "enterprise_devsecops.service:app", "--host", "0.0.0.0", "--port", "8080"]
