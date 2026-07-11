from pydantic import BaseModel

class AnalyticsOverview(BaseModel):
    total_students: int
    high_risk_count: int
    medium_risk_count: int
    low_risk_count: int
    pending_reviews_count: int

class RiskDistributionItem(BaseModel):
    risk_level: str
    count: int
    percentage: float

class RiskTrendItem(BaseModel):
    date: str  # YYYY-MM-DD
    high_risk: int
    medium_risk: int
    low_risk: int

class InterventionStatusOverview(BaseModel):
    pending: int
    approved: int
    rejected: int
    modified: int
    approval_rate: float
    modification_rate: float
