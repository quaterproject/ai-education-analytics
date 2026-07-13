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

# Install python dependencies system-wide inside the container
RUN uv pip install --system --no-cache -r pyproject.toml

# Copy backend codebase
COPY . .

# Run the model training script at build time to pre-bake the saved models into the image
RUN python src/models/train_models.py

# Expose port 8000
EXPOSE 8000

# Start FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
