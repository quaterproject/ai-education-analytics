#!/bin/sh
set -e

MODEL_DIR="data/models"

if [ ! -d "$MODEL_DIR" ] || [ -z "$(ls -A "$MODEL_DIR" 2>/dev/null)" ]; then
    echo "No trained models found — running training..."
    python src/models/train_models.py
else
    echo "Trained models found — skipping training."
fi

exec uvicorn main:app --host 0.0.0.0 --port "${PORT:-8000}"