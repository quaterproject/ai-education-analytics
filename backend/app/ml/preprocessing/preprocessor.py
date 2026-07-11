import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from app.ml.preprocessing.feature_engineering import engineer_features

class StudentDataPreprocessor:
    def __init__(self, model_type: str = "LATE_STAGE"):
        self.model_type = model_type
        self.pipeline = None
        self.feature_names: list[str] = []
        
        # Base numerical columns (excluding grades)
        self.base_num_cols = [
            'age', 'Medu', 'Fedu', 'traveltime', 'studytime', 
            'failures', 'famrel', 'freetime', 'goout', 'Dalc', 
            'Walc', 'health', 'absences'
        ]
        
        # Base categorical columns
        self.base_cat_cols = [
            'school', 'sex', 'address', 'famsize', 'Pstatus', 
            'Mjob', 'Fjob', 'reason', 'guardian', 'schoolsup', 
            'famsup', 'paid', 'activities', 'nursery', 'higher', 
            'internet', 'romantic'
        ]
        
        # Engineered columns (excluding grade_trend)
        self.engineered_cols = [
            'alc_consumption', 'parent_edu_sum', 'academic_support_score', 'study_to_free_ratio'
        ]

    def _get_columns(self):
        """Get numerical and categorical columns depending on the model configuration."""
        num_cols = self.base_num_cols + self.engineered_cols
        cat_cols = self.base_cat_cols.copy()
        
        if self.model_type == "LATE_STAGE":
            num_cols = num_cols + ['G1', 'G2', 'grade_trend']
            
        return num_cols, cat_cols

    def fit(self, X: pd.DataFrame):
        """Fit the preprocessing pipeline on the input data."""
        # 1. Engineer features first
        X_eng = engineer_features(X, model_type=self.model_type)
        
        num_cols, cat_cols = self._get_columns()
        
        # Ensure all columns exist in X_eng, fill missing with defaults if needed
        for col in num_cols:
            if col not in X_eng.columns:
                X_eng[col] = 0.0
        for col in cat_cols:
            if col not in X_eng.columns:
                X_eng[col] = "no"

        # 2. Setup Transformers
        num_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler())
        ])
        
        cat_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='most_frequent')),
            ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
        ])
        
        self.preprocessor = ColumnTransformer(
            transformers=[
                ('num', num_transformer, num_cols),
                ('cat', cat_transformer, cat_cols)
            ]
        )
        
        # Fit
        self.preprocessor.fit(X_eng[num_cols + cat_cols])
        
        # Cache feature names
        num_features = num_cols
        try:
            cat_features = list(self.preprocessor.named_transformers_['cat'].named_steps['onehot'].get_feature_names_out(cat_cols))
        except Exception:
            cat_features = [f"{col}_encoded" for col in cat_cols] # fallback
            
        self.feature_names = num_features + cat_features
        return self

    def transform(self, X: pd.DataFrame) -> np.ndarray:
        """Transform input data using the fitted pipeline."""
        X_eng = engineer_features(X, model_type=self.model_type)
        num_cols, cat_cols = self._get_columns()
        
        # Ensure all columns exist in X_eng
        for col in num_cols:
            if col not in X_eng.columns:
                X_eng[col] = 0.0
        for col in cat_cols:
            if col not in X_eng.columns:
                X_eng[col] = "no"
                
        return self.preprocessor.transform(X_eng[num_cols + cat_cols])

    def fit_transform(self, X: pd.DataFrame) -> np.ndarray:
        return self.fit(X).transform(X)
