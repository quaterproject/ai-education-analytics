FROM python:3.12-slim

# System deps: Tesseract OCR + audio libs
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    libtesseract-dev \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install uv
RUN pip install --no-cache-dir uv

# Copy dependency manifests first (layer caching)
COPY pyproject.toml uv.lock ./

# Use uv sync so installs match the lockfile exactly (reproducible builds)
RUN uv sync --frozen --no-cache --no-dev

# Make the venv the default python/uvicorn
ENV PATH="/app/.venv/bin:$PATH"
ENV TF_CPP_MIN_LOG_LEVEL=3
ENV OMP_NUM_THREADS=1
ENV TF_ENABLE_ONEDNN_OPTS=0
ENV MALLOC_MMAP_THRESHOLD_=131072

# Copy the rest of the codebase
COPY . .

# Non-root user for security
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

# Only train if model artifacts are missing — don't retrain on every boot
COPY --chown=appuser:appuser entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
