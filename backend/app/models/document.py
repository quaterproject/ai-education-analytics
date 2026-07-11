import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class Document(Base):
    __tablename__ = "documents"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    student_id: Mapped[str] = mapped_column(String, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    
    filename: Mapped[str] = mapped_column(String, nullable=False)
    file_type: Mapped[str] = mapped_column(String, nullable=False) # 'pdf', 'png', 'jpg', 'jpeg', 'webp'
    file_path: Mapped[str] = mapped_column(String, nullable=False)
    processing_status: Mapped[str] = mapped_column(String, default="PENDING") # 'PENDING', 'PROCESSING', 'COMPLETED', 'FAILED'
    extracted_text: Mapped[str] = mapped_column(Text, nullable=True)
    structured_data: Mapped[dict] = mapped_column(JSON, nullable=True) # JSON containing structured fields from parsing
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    student = relationship("Student", back_populates="documents")
