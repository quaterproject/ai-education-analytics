import torch
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from app.ml.models.student_risk_ann import StudentRiskANN
from app.core.logging import logger

def evaluate_ann_model(
    model: StudentRiskANN,
    X_test: np.ndarray,
    y_test: np.ndarray,
    target_names: list[str]
) -> dict:
    """
    Evaluate the trained StudentRiskANN model on a test set.
    """
    model.eval()
    
    # Convert test inputs to PyTorch Tensors
    X_tensor = torch.tensor(X_test, dtype=torch.float32)
    
    with torch.no_grad():
        logits = model(X_tensor)
        probabilities = torch.softmax(logits, dim=1).numpy()
        predictions = torch.argmax(logits, dim=1).numpy()
        
    accuracy = accuracy_score(y_test, predictions)
    report = classification_report(y_test, predictions, target_names=target_names, output_dict=True, zero_division=0)
    cm = confusion_matrix(y_test, predictions)
    
    evaluation_results = {
        "accuracy": float(accuracy),
        "classification_report": report,
        "confusion_matrix": cm.tolist(),
        "predictions": predictions.tolist(),
        "probabilities": probabilities.tolist()
    }
    
    logger.info("--- Evaluation Metrics ---")
    logger.info(f"Test Accuracy: {accuracy:.4f}")
    for name in target_names:
        if name in report:
            logger.info(f"Class '{name}' F1-Score: {report[name]['f1-score']:.4f}")
            
    return evaluation_results
