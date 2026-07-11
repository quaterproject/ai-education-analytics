from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class StudentBase(BaseModel):
    student_code: str = Field(..., description="Unique alphanumeric identifier for the student")
    first_name: str = Field(..., min_length=1)
    last_name: str = Field(..., min_length=1)
    age: int = Field(..., ge=0, le=100)
    gender: str = Field(..., pattern="^[MF]$", description="M for Male, F for Female")
    school: str = Field(..., pattern="^(GP|MS)$", description="GP for Gabriel Pereira, MS for Mousinho da Silveira")

class StudentCreate(StudentBase):
    pass

class StudentUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1)
    last_name: Optional[str] = Field(None, min_length=1)
    age: Optional[int] = Field(None, ge=0, le=100)
    gender: Optional[str] = Field(None, pattern="^[MF]$")
    school: Optional[str] = Field(None, pattern="^(GP|MS)$")

class StudentOut(StudentBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
