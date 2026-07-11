from datetime import datetime
from pydantic import BaseModel, Field

class AcademicRecordBase(BaseModel):
    study_time: int = Field(..., ge=1, le=4, description="Weekly study time (1: <2h, 2: 2-5h, 3: 5-10h, 4: >10h)")
    failures: int = Field(..., ge=0, le=4, description="Number of past class failures (0-4)")
    absences: int = Field(..., ge=0, le=93, description="Number of school absences (0-93)")
    family_support: str = Field(..., pattern="^(yes|no)$", description="Family educational support ('yes' or 'no')")
    school_support: str = Field(..., pattern="^(yes|no)$", description="School educational support ('yes' or 'no')")
    internet_access: str = Field(..., pattern="^(yes|no)$", description="Internet access at home ('yes' or 'no')")
    health: int = Field(..., ge=1, le=5, description="Current health status (1: very bad to 5: very good)")
    g1: float = Field(..., ge=0.0, le=20.0, description="First period grade (0 to 20)")
    g2: float = Field(..., ge=0.0, le=20.0, description="Second period grade (0 to 20)")

class AcademicRecordCreate(AcademicRecordBase):
    pass

class AcademicRecordOut(AcademicRecordBase):
    id: str
    student_id: str
    created_at: datetime

    class Config:
        from_attributes = True
