import torch
from torch.utils.data import Dataset
import numpy as np

class StudentDataset(Dataset):
    def __init__(self, X: np.ndarray, y: np.ndarray):
        """
        X: Preprocessed numerical feature matrix (N, num_features)
        y: Integer encoded risk labels (N,)
        """
        self.X = torch.tensor(X, dtype=torch.float32)
        self.y = torch.tensor(y, dtype=torch.long)

    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx: int):
        return self.X[idx], self.y[idx]
