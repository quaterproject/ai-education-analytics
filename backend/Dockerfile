FROM python:3.12-slim

# Install system dependencies including Tesseract OCR and audio libs
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install uv python package manager
RUN pip install --no-cache-dir uv

# Copy dependencies manifest
COPY pyproject.toml uv.lock ./

# ✅ FIX 1: Correct package installation for pyproject.toml
RUN uv pip install --system --no-cache .

# Copy backend codebase
COPY . .

# Expose port 8000
EXPOSE 8000

# ✅ FIX 2: Run training first, THEN start FastAPI server automatically on startup
CMD python src/models/train_models.py && uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
