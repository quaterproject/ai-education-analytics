import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
import numpy as np
from app.ml.models.student_risk_ann import StudentRiskANN
from app.ml.training.dataset import StudentDataset
from app.core.logging import logger

def train_ann_model(
    X_train: np.ndarray,
    y_train: np.ndarray,
    X_val: np.ndarray,
    y_val: np.ndarray,
    epochs: int = 150,
    batch_size: int = 32,
    lr: float = 0.005,
    weight_decay: float = 1e-4,
    patience: int = 15
) -> tuple[StudentRiskANN, dict]:
    """
    Train the StudentRiskANN model using PyTorch.
    Implements early stopping and learning rate scheduling.
    """
    input_dim = X_train.shape[1]
    num_classes = len(np.unique(y_train))
    
    # Create datasets and dataloaders
    train_dataset = StudentDataset(X_train, y_train)
    val_dataset = StudentDataset(X_val, y_val)
    
    # Drop last to avoid batch size of 1 during training (which causes BatchNorm issues)
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, drop_last=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False, drop_last=False)
    
    # Initialize model
    model = StudentRiskANN(input_dim=input_dim, num_classes=num_classes)
    
    # Loss, Optimizer, Scheduler
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=weight_decay)
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.5, patience=5)
    
    # Tracking training history
    history: dict[str, list[float]] = {
        "train_loss": [],
        "val_loss": [],
        "val_accuracy": [],
        "val_precision": [],
        "val_recall": [],
        "val_f1": []
    }
    
    best_val_loss = float('inf')
    best_model_state = None
    patience_counter = 0
    
    for epoch in range(1, epochs + 1):
        # Training Phase
        model.train()
        epoch_train_losses = []
        
        for batch_x, batch_y in train_loader:
            optimizer.zero_grad()
            outputs = model(batch_x)
            loss = criterion(outputs, batch_y)
            loss.backward()
            optimizer.step()
            epoch_train_losses.append(loss.item())
            
        mean_train_loss = np.mean(epoch_train_losses)
        history["train_loss"].append(float(mean_train_loss))
        
        # Validation Phase
        model.eval()
        epoch_val_losses = []
        all_preds: list[int] = []
        all_targets: list[int] = []
        
        with torch.no_grad():
            for batch_x, batch_y in val_loader:
                outputs = model(batch_x)
                loss = criterion(outputs, batch_y)
                epoch_val_losses.append(loss.item())
                
                preds = torch.argmax(outputs, dim=1).numpy()
                all_preds.extend(preds)
                all_targets.extend(batch_y.numpy())
                
        mean_val_loss = np.mean(epoch_val_losses)
        history["val_loss"].append(float(mean_val_loss))
        
        # Calculate validation metrics
        val_acc = accuracy_score(all_targets, all_preds)
        val_precision, val_recall, val_f1, _ = precision_recall_fscore_support(
            all_targets, all_preds, average='macro', zero_division=0
        )
        
        history["val_accuracy"].append(float(val_acc))
        history["val_precision"].append(float(val_precision))
        history["val_recall"].append(float(val_recall))
        history["val_f1"].append(float(val_f1))
        
        # Step LR Scheduler
        scheduler.step(mean_val_loss)
        
        logger.info(
            f"Epoch {epoch}/{epochs} | Train Loss: {mean_train_loss:.4f} | Val Loss: {mean_val_loss:.4f} | "
            f"Val Acc: {val_acc:.4f} | Val F1: {val_f1:.4f}"
        )
        
        # Early Stopping check
        if mean_val_loss < best_val_loss:
            best_val_loss = mean_val_loss
            best_model_state = model.state_dict().copy()
            patience_counter = 0
        else:
            patience_counter += 1
            if patience_counter >= patience:
                logger.info(f"Early stopping triggered at epoch {epoch}. Restoring best model state.")
                break
                
    # Restore best model state
    if best_model_state is not None:
        model.load_state_dict(best_model_state)
        
    return model, history
