import uuid
from datetime import datetime
from sqlalchemy import String, Integer, DateTime, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class Recommendation(Base):
    __tablename__ = "recommendations"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    prediction_id: Mapped[str] = mapped_column(String, ForeignKey("predictions.id", ondelete="CASCADE"), nullable=False)
    
    title: Mapped[str] = mapped_column(String, nullable=False)
    priority: Mapped[str] = mapped_column(String, nullable=False) # 'LOW', 'MEDIUM', 'HIGH'
    summary: Mapped[str] = mapped_column(String, nullable=False)
    recommended_actions: Mapped[list] = mapped_column(JSON, nullable=False) # list of strings
    monitoring_plan: Mapped[list] = mapped_column(JSON, nullable=False) # list of strings
    success_indicators: Mapped[list] = mapped_column(JSON, nullable=False) # list of strings
    review_period_days: Mapped[int] = mapped_column(Integer, default=14)
    llm_model: Mapped[str] = mapped_column(String, nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    prediction = relationship("Prediction", back_populates="recommendation")
    human_review = relationship("HumanReview", back_populates="recommendation", uselist=False, cascade="all, delete-orphan")
