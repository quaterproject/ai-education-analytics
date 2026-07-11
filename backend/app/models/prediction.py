import uuid
from datetime import datetime
from sqlalchemy import String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class Prediction(Base):
    __tablename__ = "predictions"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    student_id: Mapped[str] = mapped_column(String, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    
    risk_level: Mapped[str] = mapped_column(String, nullable=False) # 'LOW_RISK', 'MEDIUM_RISK', 'HIGH_RISK'
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    class_probabilities: Mapped[dict] = mapped_column(JSON, nullable=False) # {'LOW_RISK': 0.1, ...}
    model_version: Mapped[str] = mapped_column(String, nullable=False)
    
    feature_values: Mapped[dict] = mapped_column(JSON, nullable=False) # raw features sent to preprocessor
    shap_values: Mapped[dict] = mapped_column(JSON, nullable=False) # shap values mapped to features
    risk_factors: Mapped[list] = mapped_column(JSON, nullable=False) # list of string factors
    protective_factors: Mapped[list] = mapped_column(JSON, nullable=False) # list of string protective factors
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    student = relationship("Student", back_populates="predictions")
    recommendation = relationship("Recommendation", back_populates="prediction", uselist=False, cascade="all, delete-orphan")
