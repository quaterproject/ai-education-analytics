from app.core.database import Base
from app.models.student import Student
from app.models.academic_record import AcademicRecord
from app.models.document import Document
from app.models.prediction import Prediction
from app.models.recommendation import Recommendation
from app.models.human_review import HumanReview

__all__ = [
    "Base",
    "Student",
    "AcademicRecord",
    "Document",
    "Prediction",
    "Recommendation",
    "HumanReview",
]
