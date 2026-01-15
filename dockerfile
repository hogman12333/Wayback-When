# syntax=docker/dockerfile:1.6

############################
# Builder stage
# Build wheels here so the runtime image stays small and does not ship compilers.
############################
FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /build

# Build only deps, they do not belong in the final image.
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      build-essential \
      gcc \
      g++ \
      libffi-dev \
      libssl-dev \
      ca-certificates \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip wheel --wheel-dir /wheels -r requirements.txt


############################
# Runtime stage
# This is what you run.
############################
FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    CHROME_BIN=/usr/bin/google-chrome \
    MPLCONFIGDIR=/app/.matplotlib \
    XDG_CACHE_HOME=/tmp/.cache \
    WDM_LOCAL=1 \
    WDM_CACHE_DIR=/tmp/.wdm

WORKDIR /app

# Chrome install plus the libraries it needs for headless runs.
RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
      ca-certificates \
      curl \
      gnupg \
      wget \
      fonts-liberation \
      libasound2 \
      libatk-bridge2.0-0 \
      libatk1.0-0 \
      libc6 \
      libcairo2 \
      libcups2 \
      libdbus-1-3 \
      libdrm2 \
      libexpat1 \
      libgbm1 \
      libglib2.0-0 \
      libnspr4 \
      libnss3 \
      libpango-1.0-0 \
      libpangocairo-1.0-0 \
      libx11-6 \
      libx11-xcb1 \
      libxcb1 \
      libxcomposite1 \
      libxdamage1 \
      libxext6 \
      libxfixes3 \
      libxkbcommon0 \
      libxrandr2 \
      libxrender1 \
      libxshmfence1 \
      libxss1 \
      libxtst6 \
      xdg-utils; \
    rm -rf /var/lib/apt/lists/*

# Add the official Chrome repo using a keyring, then install Chrome.
RUN set -eux; \
    mkdir -p /etc/apt/keyrings; \
    wget -qO- https://dl.google.com/linux/linux_signing_key.pub \
      | gpg --dearmor -o /etc/apt/keyrings/google.gpg; \
    echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/google.gpg] http://dl.google.com/linux/chrome/deb/ stable main" \
      > /etc/apt/sources.list.d/google-chrome.list; \
    apt-get update; \
    apt-get install -y --no-install-recommends google-chrome-stable; \
    rm -rf /var/lib/apt/lists/*

# Run as nonroot, and keep webdriver_manager and matplotlib caches writable.
RUN useradd -m -u 10001 appuser \
 && mkdir -p /app /tmp/.cache /tmp/.wdm /app/.matplotlib \
 && chown -R appuser:appuser /app /tmp/.cache /tmp/.wdm

# Install Python deps from wheels built in the builder stage.
COPY --from=builder /wheels /wheels
COPY requirements.txt .
RUN pip install --no-cache-dir --no-index --find-links=/wheels -r requirements.txt \
 && rm -rf /wheels

COPY app.py /app/app.py

USER appuser

CMD ["python", "/app/app.py"]
