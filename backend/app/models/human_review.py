import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey, JSON, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class HumanReview(Base):
    __tablename__ = "human_reviews"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    recommendation_id: Mapped[str] = mapped_column(String, ForeignKey("recommendations.id", ondelete="CASCADE"), nullable=False)
    
    status: Mapped[str] = mapped_column(String, default="PENDING_REVIEW") # 'PENDING_REVIEW', 'APPROVED', 'REJECTED', 'MODIFIED'
    reviewed_by: Mapped[str] = mapped_column(String, nullable=True) # Educator name/username
    educator_comment: Mapped[str] = mapped_column(Text, nullable=True)
    rejection_reason: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Audit trail: store complete original recommendation state and the modified state
    original_recommendation: Mapped[dict] = mapped_column(JSON, nullable=False) # original json representation
    modified_recommendation: Mapped[dict] = mapped_column(JSON, nullable=True) # modified json representation (if modified)
    
    reviewed_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    recommendation = relationship("Recommendation", back_populates="human_review")
