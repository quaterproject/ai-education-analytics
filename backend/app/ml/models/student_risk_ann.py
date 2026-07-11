import torch
import torch.nn as nn

class StudentRiskANN(nn.Module):
    def __init__(self, input_dim: int, num_classes: int = 3, dropout_rate: float = 0.3):
        super(StudentRiskANN, self).__init__()
        
        # Layer 1: Input -> 128 neurons
        self.fc1 = nn.Linear(input_dim, 128)
        self.bn1 = nn.BatchNorm1d(128)
        self.relu1 = nn.ReLU()
        self.dropout1 = nn.Dropout(p=dropout_rate)
        
        # Layer 2: 128 -> 64 neurons
        self.fc2 = nn.Linear(128, 64)
        self.bn2 = nn.BatchNorm1d(64)
        self.relu2 = nn.ReLU()
        self.dropout2 = nn.Dropout(p=dropout_rate)
        
        # Layer 3: 64 -> 32 neurons
        self.fc3 = nn.Linear(64, 32)
        self.bn3 = nn.BatchNorm1d(32)
        self.relu3 = nn.ReLU()
        self.dropout3 = nn.Dropout(p=dropout_rate * 0.6) # slightly lower dropout at the end
        
        # Output Layer: 32 -> num_classes logits
        self.out = nn.Linear(32, num_classes)
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # Check if 1D input is passed (e.g. single sample) and unsqueeze to 2D
        if len(x.shape) == 1:
            x = x.unsqueeze(0)
            
        x = self.fc1(x)
        # BatchNorm1d requires batch size > 1 during training. In evaluation mode, it works for batch size 1.
        if x.size(0) > 1 or not self.training:
            x = self.bn1(x)
        x = self.relu1(x)
        x = self.dropout1(x)
        
        x = self.fc2(x)
        if x.size(0) > 1 or not self.training:
            x = self.bn2(x)
        x = self.relu2(x)
        x = self.dropout2(x)
        
        x = self.fc3(x)
        if x.size(0) > 1 or not self.training:
            x = self.bn3(x)
        x = self.relu3(x)
        x = self.dropout3(x)
        
        logits = self.out(x)
        return logits
