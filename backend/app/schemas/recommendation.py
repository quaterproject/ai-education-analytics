from datetime import datetime
from typing import List
from pydantic import BaseModel, Field

class RecommendationBase(BaseModel):
    title: str
    priority: str = Field(..., description="HIGH, MEDIUM, or LOW")
    summary: str
    recommended_actions: List[str]
    monitoring_plan: List[str]
    success_indicators: List[str]
    review_period_days: int = Field(default=14)
    llm_model: str

class RecommendationCreate(RecommendationBase):
    prediction_id: str

class RecommendationOut(RecommendationBase):
    id: str
    prediction_id: str
    created_at: datetime

    class Config:
        from_attributes = True
