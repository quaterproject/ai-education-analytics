import os
import json
import numpy as np
import torch
import joblib
from app.ml.training.train import train_ann_model
from app.ml.training.evaluate import evaluate_ann_model

# Define paths
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
MODELS_DIR = os.path.join(BASE_DIR, "artifacts", "models")
PREPROCESSORS_DIR = os.path.join(BASE_DIR, "artifacts", "preprocessors")

def run_training():
    print("Loading processed datasets...")
    X_train = np.load(os.path.join(PROCESSED_DIR, "X_train.npy"))
    y_train = np.load(os.path.join(PROCESSED_DIR, "y_train.npy"))
    X_val = np.load(os.path.join(PROCESSED_DIR, "X_val.npy"))
    y_val = np.load(os.path.join(PROCESSED_DIR, "y_val.npy"))
    X_test = np.load(os.path.join(PROCESSED_DIR, "X_test.npy"))
    y_test = np.load(os.path.join(PROCESSED_DIR, "y_test.npy"))
    
    # Load labels mapping to map classes
    label_path = os.path.join(PREPROCESSORS_DIR, "label_encoder.joblib")
    if not os.path.exists(label_path):
        raise FileNotFoundError("Label mapping file not found. Run prepare_dataset.py first.")
    label_mapping = joblib.load(label_path)
    # Target names in order (0: LOW_RISK, 1: MEDIUM_RISK, 2: HIGH_RISK)
    target_names = [k for k, v in sorted(label_mapping.items(), key=lambda item: item[1])]

    print("Dataset summary:")
    print(f"X_train shape: {X_train.shape} | X_val shape: {X_val.shape} | X_test shape: {X_test.shape}")
    print(f"Target names: {target_names}")
    
    # Train model
    model, history = train_ann_model(
        X_train, y_train, X_val, y_val,
        epochs=150, batch_size=32, lr=0.005, weight_decay=1e-4, patience=15
    )
    
    # Evaluate model
    eval_results = evaluate_ann_model(model, X_test, y_test, target_names)
    
    # Ensure directories exist
    os.makedirs(MODELS_DIR, exist_ok=True)
    
    # Save PyTorch Model
    model_save_path = os.path.join(MODELS_DIR, "student_risk_ann.pt")
    torch.save(model.state_dict(), model_save_path)
    print(f"Model state dictionary saved to {model_save_path}")
    
    # Save Metadata & Metrics
    metadata = {
        "model_name": "StudentRiskANN",
        "input_dim": X_train.shape[1],
        "num_classes": len(target_names),
        "target_names": target_names,
        "metrics": {
            "test_accuracy": eval_results["accuracy"],
            "classification_report": eval_results["classification_report"],
            "confusion_matrix": eval_results["confusion_matrix"]
        },
        "history": history
    }
    
    metadata_save_path = os.path.join(MODELS_DIR, "model_metadata.json")
    with open(metadata_save_path, "w") as f:
        json.dump(metadata, f, indent=4)
    print(f"Model metadata and metrics saved to {metadata_save_path}")

if __name__ == "__main__":
    run_training()
