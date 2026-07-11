import uuid
from datetime import datetime
from sqlalchemy import String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class AcademicRecord(Base):
    __tablename__ = "academic_records"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    student_id: Mapped[str] = mapped_column(String, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    
    study_time: Mapped[int] = mapped_column(Integer, nullable=False) # hours per week (1: <2h, 2: 2-5h, 3: 5-10h, 4: >10h)
    failures: Mapped[int] = mapped_column(Integer, nullable=False) # number of past class failures (n if 1<=n<3, else 4)
    absences: Mapped[int] = mapped_column(Integer, nullable=False) # number of school absences (0 to 93)
    
    family_support: Mapped[str] = mapped_column(String, nullable=False) # 'yes' or 'no'
    school_support: Mapped[str] = mapped_column(String, nullable=False) # 'yes' or 'no'
    internet_access: Mapped[str] = mapped_column(String, nullable=False) # 'yes' or 'no'
    health: Mapped[int] = mapped_column(Integer, nullable=False) # current health status (1: very bad to 5: very good)
    
    g1: Mapped[float] = mapped_column(Float, nullable=False) # first period grade (0 to 20)
    g2: Mapped[float] = mapped_column(Float, nullable=False) # second period grade (0 to 20)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    student = relationship("Student", back_populates="academic_records")
