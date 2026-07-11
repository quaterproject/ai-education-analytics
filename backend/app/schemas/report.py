from datetime import datetime
from pydantic import BaseModel

class ReportGenerateResponse(BaseModel):
    report_id: str
    file_type: str  # 'pdf' or 'docx'
    filename: str
    download_url: str
    generated_at: datetime
