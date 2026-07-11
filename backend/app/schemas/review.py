from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from app.schemas.recommendation import RecommendationOut

class RecommendationModificationFields(BaseModel):
    title: str
    priority: str
    summary: str
    recommended_actions: List[str]
    monitoring_plan: List[str]
    success_indicators: List[str]
    review_period_days: int

class ReviewApproveRequest(BaseModel):
    reviewed_by: str = Field(..., description="Name of the educator reviewing this recommendation")
    educator_comment: Optional[str] = Field(None, description="Optional notes or feedback")

class ReviewRejectRequest(BaseModel):
    reviewed_by: str = Field(..., description="Name of the educator reviewing this recommendation")
    rejection_reason: str = Field(..., description="Required explanation for why recommendation is rejected")

class ReviewModifyRequest(BaseModel):
    reviewed_by: str = Field(..., description="Name of the educator reviewing this recommendation")
    educator_comment: Optional[str] = Field(None, description="Optional notes or feedback")
    modified_recommendation: RecommendationModificationFields = Field(..., description="The modified recommendation contents")

class HumanReviewOut(BaseModel):
    id: str
    recommendation_id: str
    status: str
    reviewed_by: Optional[str] = None
    educator_comment: Optional[str] = None
    rejection_reason: Optional[str] = None
    original_recommendation: Dict[str, Any]
    modified_recommendation: Optional[Dict[str, Any]] = None
    reviewed_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True

# Extended schema for queue displays
class HumanReviewQueueOut(HumanReviewOut):
    recommendation: Optional[RecommendationOut] = None
    student_name: Optional[str] = None
    student_code: Optional[str] = None
    student_id: Optional[str] = None
    risk_level: Optional[str] = None
    confidence: Optional[float] = None
