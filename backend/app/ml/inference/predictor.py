import os
import torch
import pandas as pd
import numpy as np
import joblib
from typing import Dict, Any, Tuple
from app.ml.models.student_risk_ann import StudentRiskANN
from app.core.config import settings
from app.core.exceptions import ModelNotFoundException
from app.core.logging import logger

class StudentRiskPredictor:
    def __init__(self):
        self.model = None
        self.preprocessor = None
        self.label_mapping = None
        self.reverse_label_mapping = None
        self.is_loaded = False

    def load_model(self) -> bool:
        """
        Load the model state, preprocessor, and label mappings from the artifacts directory.
        """
        if self.is_loaded:
            return True
            
        model_path = settings.MODEL_PATH
        preprocessor_path = settings.PREPROCESSOR_PATH
        label_path = settings.LABEL_ENCODER_PATH
        
        # Check files
        if not (os.path.exists(model_path) and os.path.exists(preprocessor_path) and os.path.exists(label_path)):
            logger.warning(
                f"Model artifacts missing. Expected paths:\n"
                f"- Model: {model_path}\n"
                f"- Preprocessor: {preprocessor_path}\n"
                f"- Label Encoder: {label_path}\n"
                f"Please run download_dataset.py, prepare_dataset.py, and train_model.py first."
            )
            return False
            
        try:
            # 1. Load Preprocessor and Label mappings
            self.preprocessor = joblib.load(preprocessor_path)
            self.label_mapping = joblib.load(label_path)
            # Create reverse mapping (0 -> LOW_RISK, etc.)
            self.reverse_label_mapping = {v: k for k, v in self.label_mapping.items()}
            
            # 2. Get input dimension from the preprocessor features
            # This ensures that the dimension of the ANN input layer matches the preprocessed features dimension
            dummy_df = pd.DataFrame([self._get_dummy_features()])
            preprocessed_dummy = self.preprocessor.transform(dummy_df)
            input_dim = preprocessed_dummy.shape[1]
            
            # 3. Instantiate and load PyTorch model
            num_classes = len(self.label_mapping)
            self.model = StudentRiskANN(input_dim=input_dim, num_classes=num_classes)
            
            # Map storage to CPU if no GPU available
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            state_dict = torch.load(model_path, map_location=device)
            self.model.load_state_dict(state_dict)
            self.model.to(device)
            self.model.eval() # Set to evaluation mode
            
            self.is_loaded = True
            logger.info("StudentRiskANN and preprocessing artifacts loaded successfully!")
            return True
            
        except Exception as e:
            logger.error(f"Error loading model artifacts: {e}", exc_info=True)
            self.is_loaded = False
            return False

    def predict(self, student_features: Dict[str, Any]) -> Tuple[str, float, Dict[str, float], np.ndarray]:
        """
        Run risk prediction on a student's features.
        Returns:
            Tuple of:
                - risk_level (str)
                - confidence (float)
                - class_probabilities (Dict[str, float])
                - preprocessed_features (np.ndarray)
        """
        if not self.is_loaded:
            success = self.load_model()
            if not success:
                raise ModelNotFoundException()
                
        try:
            # 1. Convert dictionary features to pandas DataFrame
            df = pd.DataFrame([student_features])
            
            # 2. Preprocess features
            X_preprocessed = self.preprocessor.transform(df)
            X_tensor = torch.tensor(X_preprocessed, dtype=torch.float32)
            
            # 3. Predict using PyTorch
            with torch.no_grad():
                logits = self.model(X_tensor)
                probs = torch.softmax(logits, dim=1).squeeze(0).numpy()
                
            # 4. Map outputs
            predicted_class_idx = int(np.argmax(probs))
            predicted_risk_level = self.reverse_label_mapping[predicted_class_idx]
            confidence = float(probs[predicted_class_idx])
            
            class_probabilities = {
                self.reverse_label_mapping[idx]: float(prob)
                for idx, prob in enumerate(probs)
            }
            
            return predicted_risk_level, confidence, class_probabilities, X_preprocessed
            
        except Exception as e:
            logger.error(f"Prediction failed: {e}", exc_info=True)
            raise ModelNotFoundException(f"Error executing model inference: {str(e)}")

    def _get_dummy_features(self) -> Dict[str, Any]:
        """Return basic features to initialize columns and dimension tracking."""
        return {
            'school': 'GP', 'sex': 'F', 'age': 15, 'address': 'U', 'famsize': 'GT3',
            'Pstatus': 'T', 'Medu': 4, 'Fedu': 4, 'Mjob': 'other', 'fjob': 'other',
            'reason': 'course', 'guardian': 'mother', 'traveltime': 1, 'studytime': 2,
            'failures': 0, 'schoolsup': 'no', 'famsup': 'no', 'paid': 'no',
            'activities': 'no', 'nursery': 'no', 'higher': 'yes', 'internet': 'yes',
            'romantic': 'no', 'famrel': 4, 'freetime': 3, 'goout': 3, 'Dalc': 1,
            'Walc': 1, 'health': 3, 'absences': 0, 'G1': 10, 'G2': 10
        }

# Global predictor singleton
predictor = StudentRiskPredictor()
