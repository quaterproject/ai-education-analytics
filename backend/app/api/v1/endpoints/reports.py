import os
import glob
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import get_db
from app.services.report_service import ReportService
from app.schemas.report import ReportGenerateResponse
from app.core.config import settings

router = APIRouter()

@router.post("/students/{student_id}/reports/pdf", response_model=ReportGenerateResponse, status_code=status.HTTP_201_CREATED)
async def generate_pdf_report(
    student_id: str,
    db: AsyncSession = Depends(get_db)
):
    try:
        return await ReportService.generate_student_report(db, student_id, "pdf")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate PDF report: {str(e)}"
        )

@router.post("/students/{student_id}/reports/docx", response_model=ReportGenerateResponse, status_code=status.HTTP_201_CREATED)
async def generate_docx_report(
    student_id: str,
    db: AsyncSession = Depends(get_db)
):
    try:
        return await ReportService.generate_student_report(db, student_id, "docx")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate DOCX report: {str(e)}"
        )

@router.get("/reports/{report_id}/download")
async def download_report(report_id: str):
    # Search for files with the report_id inside the report directory
    search_path = os.path.join(settings.REPORT_DIR, f"*_risk_report_{report_id}.*")
    matching_files = glob.glob(search_path)
    
    if not matching_files:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Report file with ID '{report_id}' was not found on disk."
        )
        
    file_path = matching_files[0]
    filename = os.path.basename(file_path)
    
    # Determine media type
    media_type = "application/octet-stream"
    if filename.endswith(".pdf"):
        media_type = "application/pdf"
    elif filename.endswith(".docx"):
        media_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        
    return FileResponse(
        path=file_path,
        media_type=media_type,
        filename=filename
    )
