import os
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from app.ml.preprocessing.preprocessor import StudentDataPreprocessor
from app.core.constants import LOW_RISK, MEDIUM_RISK, HIGH_RISK

# Define paths
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
PREPROCESSORS_DIR = os.path.join(BASE_DIR, "artifacts", "preprocessors")

def prepare_dataset(model_type: str = "LATE_STAGE"):
    print(f"Preparing dataset for model type: {model_type}...")
    
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    os.makedirs(PREPROCESSORS_DIR, exist_ok=True)
    
    # Load raw datasets
    mat_path = os.path.join(RAW_DIR, "student-mat.csv")
    por_path = os.path.join(RAW_DIR, "student-por.csv")
    
    if not os.path.exists(mat_path) or not os.path.exists(por_path):
        raise FileNotFoundError(
            "Raw CSV files not found. Please run download_dataset.py first."
        )
        
    df_mat = pd.read_csv(mat_path, sep=";")
    df_por = pd.read_csv(por_path, sep=";")
    
    # Add a course source column
    df_mat['course'] = 'math'
    df_por['course'] = 'portuguese'
    
    # Combine datasets
    df = pd.concat([df_mat, df_por], ignore_index=True)
    
    # Drop duplicates if student exists in both datasets (UCI has some overlap)
    # The overlap can be identified by student variables:
    overlap_cols = [
        "school", "sex", "age", "address", "famsize", "Pstatus", "Medu", "Fedu",
        "Mjob", "Fjob", "reason", "guardian", "traveltime", "studytime", "failures",
        "schoolsup", "famsup", "paid", "activities", "nursery", "higher", "internet", "romantic"
    ]
    df = df.drop_duplicates(subset=overlap_cols, keep='first')
    
    # Create Risk Label (Target Variable) based on G3
    # G3 >= 14: LOW_RISK
    # G3 >= 10 and < 14: MEDIUM_RISK
    # G3 < 10: HIGH_RISK
    def get_risk_label(g3):
        if g3 >= 14:
            return LOW_RISK
        elif g3 >= 10:
            return MEDIUM_RISK
        else:
            return HIGH_RISK
            
    df['risk_level'] = df['G3'].apply(get_risk_label)
    
    # Encode Target Labels
    # LOW_RISK -> 0, MEDIUM_RISK -> 1, HIGH_RISK -> 2
    label_mapping = {LOW_RISK: 0, MEDIUM_RISK: 1, HIGH_RISK: 2}
    df['label'] = df['risk_level'].map(label_mapping)
    
    # Separate features and target
    # Exclude G3 to prevent direct target leakage
    X = df.drop(columns=['G3', 'risk_level', 'label'])
    y = df['label'].values
    
    # Split into train (70%), val (15%), test (15%)
    X_train_raw, X_temp_raw, y_train, y_temp = train_test_split(X, y, test_size=0.30, random_state=42, stratify=y)
    X_val_raw, X_test_raw, y_val, y_test = train_test_split(X_temp_raw, y_temp, test_size=0.50, random_state=42, stratify=y_temp)
    
    # Instantiate and fit preprocessor
    preprocessor = StudentDataPreprocessor(model_type=model_type)
    preprocessor.fit(X_train_raw)
    
    # Transform datasets
    X_train = preprocessor.transform(X_train_raw)
    X_val = preprocessor.transform(X_val_raw)
    X_test = preprocessor.transform(X_test_raw)
    
    # Save datasets
    np.save(os.path.join(PROCESSED_DIR, "X_train.npy"), X_train)
    np.save(os.path.join(PROCESSED_DIR, "y_train.npy"), y_train)
    np.save(os.path.join(PROCESSED_DIR, "X_val.npy"), X_val)
    np.save(os.path.join(PROCESSED_DIR, "y_val.npy"), y_val)
    np.save(os.path.join(PROCESSED_DIR, "X_test.npy"), X_test)
    np.save(os.path.join(PROCESSED_DIR, "y_test.npy"), y_test)
    
    # Save the split raw dataframes for SHAP explanation base reference
    X_train_raw.to_csv(os.path.join(PROCESSED_DIR, "X_train_raw.csv"), index=False)
    X_test_raw.to_csv(os.path.join(PROCESSED_DIR, "X_test_raw.csv"), index=False)
    
    # Save preprocessor and label mappings
    joblib.dump(preprocessor, os.path.join(PREPROCESSORS_DIR, "preprocessor.joblib"))
    joblib.dump(label_mapping, os.path.join(PREPROCESSORS_DIR, "label_encoder.joblib"))
    
    print(f"Data split shapes: Train: {X_train.shape}, Val: {X_val.shape}, Test: {X_test.shape}")
    print("Preprocessor and label encoder saved successfully.")

if __name__ == "__main__":
    prepare_dataset()
