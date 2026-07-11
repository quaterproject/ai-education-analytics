from datetime import datetime
from typing import Dict, List, Any
from pydantic import BaseModel, Field

class PredictionBase(BaseModel):
    risk_level: str = Field(..., description="Predicted risk category (LOW_RISK, MEDIUM_RISK, HIGH_RISK)")
    confidence: float = Field(..., description="Model confidence score (0.0 to 1.0)")
    class_probabilities: Dict[str, float] = Field(..., description="Probability distribution across risk classes")
    model_version: str

class PredictionCreate(PredictionBase):
    student_id: str
    feature_values: Dict[str, Any]
    shap_values: Dict[str, float]
    risk_factors: List[str]
    protective_factors: List[str]

class PredictionOut(PredictionBase):
    id: str
    student_id: str
    feature_values: Dict[str, Any]
    shap_values: Dict[str, float]
    risk_factors: List[str]
    protective_factors: List[str]
    created_at: datetime

    class Config:
        from_attributes = True
