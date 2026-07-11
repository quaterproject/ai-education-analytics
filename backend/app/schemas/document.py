from datetime import datetime
from typing import Optional, Any, Dict
from pydantic import BaseModel

class DocumentBase(BaseModel):
    filename: str
    file_type: str
    processing_status: str

class DocumentCreate(BaseModel):
    filename: str
    file_type: str
    file_path: str

class DocumentOut(DocumentBase):
    id: str
    student_id: str
    extracted_text: Optional[str] = None
    structured_data: Optional[Dict[str, Any]] = None
    created_at: datetime

    class Config:
        from_attributes = True
