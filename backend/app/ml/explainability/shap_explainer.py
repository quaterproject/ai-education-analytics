import os
import shap
import numpy as np
import torch
from typing import Dict, List, Tuple, Any
from app.core.logging import logger

def explain_student_risk(
    predictor: Any,
    X_instance: np.ndarray,
    predicted_risk_level: str
) -> Tuple[Dict[str, float], List[str], List[str]]:
    """
    Calculate SHAP explanation values for a specific student instance.
    Returns:
        - shap_values_dict: Dict mapping feature name -> shap value
        - risk_factors: List of strings detailing high risk contributors
        - protective_factors: List of strings detailing protective elements
    """
    if not predictor.is_loaded:
        return {}, ["Model not loaded"], ["Model not loaded"]
        
    try:
        # Load background dataset to initialize explainer
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        X_train_path = os.path.join(base_dir, "data", "processed", "X_train.npy")
        
        if os.path.exists(X_train_path):
            X_train = np.load(X_train_path)
            # Summarize background data for speed: select 20 representative centroids
            background_data = shap.kmeans(X_train, min(20, X_train.shape[0]))
        else:
            # Fallback to random uniform background if train data is missing
            background_data = np.zeros((10, X_instance.shape[1]))
            
        # Define model probability function for SHAP
        def model_predict_probs(x_np: np.ndarray) -> np.ndarray:
            x_tensor = torch.tensor(x_np, dtype=torch.float32)
            # Ensure model is on the correct device
            device = next(predictor.model.parameters()).device
            x_tensor = x_tensor.to(device)
            with torch.no_grad():
                logits = predictor.model(x_tensor)
                probs = torch.softmax(logits, dim=1).cpu().numpy()
            return probs
            
        # Instantiate KernelExplainer
        explainer = shap.KernelExplainer(model_predict_probs, background_data)
        
        # Calculate SHAP values for the single instance
        # nsamples controls the speed/accuracy tradeoff (100 is fast and accurate enough for 30 features)
        shap_values = explainer.shap_values(X_instance, nsamples=100)
        
        # Get target class index (0: LOW_RISK, 1: MEDIUM_RISK, 2: HIGH_RISK)
        target_class_idx = predictor.label_mapping[predicted_risk_level]
        
        # Extract SHAP values for the target class
        # shap_values is a list of arrays (one per class) or an array of shape (samples, features, classes)
        if isinstance(shap_values, list):
            class_shap = shap_values[target_class_idx][0]
        else:
            # shap 0.45+ output shape could be (samples, features, classes)
            if len(shap_values.shape) == 3:
                class_shap = shap_values[0, :, target_class_idx]
            else:
                class_shap = shap_values[0] # fallback
                
        # Map values back to feature names
        feature_names = predictor.preprocessor.feature_names
        
        # Clean feature names for user-friendly display
        # and create shap dictionary
        shap_dict = {}
        for name, val in zip(feature_names, class_shap):
            shap_dict[name] = float(val)
            
        # Generate user-friendly risk/protective factors based on SHAP signs and magnitudes
        # We sort features by their absolute SHAP values to identify key drivers
        sorted_features = sorted(shap_dict.items(), key=lambda x: abs(x[1]), reverse=True)
        
        risk_factors = []
        protective_factors = []
        
        for name, val in sorted_features:
            # Skip encoded features placeholder if they represent zero influence
            if abs(val) < 1e-4:
                continue
                
            # If the feature pushes prediction TOWARDS the risk level (positive SHAP value)
            # (Note: if predicted_risk_level is LOW_RISK, a positive value means pushing towards LOW risk,
            # which is actually a protective factor. So let's handle LOW_RISK vs HIGH_RISK carefully)
            is_high_or_medium = predicted_risk_level in ["HIGH_RISK", "MEDIUM_RISK"]
            
            if is_high_or_medium:
                if val > 0:
                    risk_factors.append(name)
                else:
                    protective_factors.append(name)
            else: # LOW_RISK
                if val > 0:
                    protective_factors.append(name)
                else:
                    risk_factors.append(name)
                    
        # Map feature names to clean descriptions
        def clean_factor_name(f: str) -> str:
            # Simple translator for feature names to human-readable text
            translations = {
                'failures': 'High previous class failure count',
                'absences': 'High class absence count',
                'studytime': 'Low weekly study time',
                'alc_consumption': 'High weekly alcohol intake',
                'freetime': 'High free time after school',
                'goout': 'Frequent going out with friends',
                'health': 'Poor health status',
                'traveltime': 'Long travel time to school',
                'schoolsup_yes': 'Extra educational support needed',
                'famsup_no': 'Lack of family educational support',
                'internet_no': 'No home internet access',
                'romantic_yes': 'Involved in a romantic relationship',
                'G1': 'Poor performance in first period (G1)',
                'G2': 'Poor performance in second period (G2)',
                'grade_trend': 'Declining intermediate grade trend',
                'study_to_free_ratio': 'Disproportionate free time to study time ratio',
                'parent_edu_sum': 'Lower parental education level'
            }
            # Fallback mapper
            for key, desc in translations.items():
                if f.startswith(key):
                    return desc
            return f.replace("_", " ").title()

        cleaned_risk = [clean_factor_name(f) for f in risk_factors[:5]]
        cleaned_protective = [clean_factor_name(f) for f in protective_factors[:5]]
        
        # Ensure we always return at least some default factors
        if not cleaned_risk:
            cleaned_risk = ["No significant academic risk indicators detected"]
        if not cleaned_protective:
            cleaned_protective = ["Standard support resources available"]

        return shap_dict, cleaned_risk, cleaned_protective
        
    except Exception as e:
        logger.error(f"SHAP explanation computation failed: {e}", exc_info=True)
        return {}, ["SHAP calculation error"], ["SHAP calculation error"]
