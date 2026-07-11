import os
import uuid
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.api.dependencies import get_db
from app.services.multimodal_service import MultimodalService
from app.schemas.document import DocumentOut
from app.core.config import settings
from app.core.exceptions import DocumentProcessingException

router = APIRouter()
multimodal_service = MultimodalService()

# Allowed file extensions
ALLOWED_EXTENSIONS = {
    "pdf": "pdf",
    "png": "png",
    "jpg": "jpg",
    "jpeg": "jpeg",
    "webp": "webp"
}

@router.post("/students/{student_id}/documents", response_model=DocumentOut, status_code=status.HTTP_201_CREATED)
async def upload_document(
    student_id: str,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    # 1. Validate file extension
    filename = file.filename or ""
    ext = filename.split(".")[-1].lower() if "." in filename else ""
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Unsupported file format '.{ext}'. Supported formats: PDF, PNG, JPG, JPEG, WEBP."
        )

    # 2. Check directory
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    
    # 3. Create unique filename
    unique_filename = f"{uuid.uuid4()}.{ext}"
    file_path = os.path.join(settings.UPLOAD_DIR, unique_filename)
    
    # 4. Save file to disk
    try:
        # Check size constraints
        size = 0
        with open(file_path, "wb") as buffer:
            while chunk := await file.read(1024 * 1024): # read in chunks of 1MB
                size += len(chunk)
                if size > settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024:
                    # Clean up
                    buffer.close()
                    if os.path.exists(file_path):
                        os.remove(file_path)
                    raise HTTPException(
                        status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                        detail=f"File exceeds maximum upload size of {settings.MAX_UPLOAD_SIZE_MB}MB."
                    )
                buffer.write(chunk)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save uploaded file: {str(e)}"
        )
        
    # 5. Extract text and structure it via MultimodalService
    try:
        document = await multimodal_service.process_and_save_document(
            db=db,
            student_id=student_id,
            file_path=file_path,
            filename=file.filename,
            file_type=ALLOWED_EXTENSIONS[ext]
        )
        return document
    except DocumentProcessingException as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.message
        )

@router.get("/students/{student_id}/documents", response_model=List[DocumentOut])
async def list_student_documents(
    student_id: str,
    db: AsyncSession = Depends(get_db)
):
    return await multimodal_service.get_student_documents(db, student_id)

@router.get("/documents/{document_id}", response_model=DocumentOut)
async def get_document(
    document_id: str,
    db: AsyncSession = Depends(get_db)
):
    try:
        return await multimodal_service.get_document(db, document_id)
    except DocumentProcessingException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message
        )
