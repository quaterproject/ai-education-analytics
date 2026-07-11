from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from pydantic import BaseModel
from app.api.dependencies import get_db
from app.services.recommendation_service import RecommendationService
from app.schemas.recommendation import RecommendationOut

router = APIRouter()

class RecommendationGenerateRequest(BaseModel):
    teacher_notes: Optional[str] = None
    document_id: Optional[str] = None

@router.post("/predictions/{prediction_id}/recommendation", response_model=RecommendationOut, status_code=status.HTTP_201_CREATED)
async def generate_recommendation(
    prediction_id: str,
    payload: RecommendationGenerateRequest,
    db: AsyncSession = Depends(get_db)
):
    try:
        return await RecommendationService.generate_recommendation(
            db=db,
            prediction_id=prediction_id,
            teacher_notes=payload.teacher_notes,
            document_id=payload.document_id
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/recommendations/{recommendation_id}", response_model=RecommendationOut)
async def get_recommendation(
    recommendation_id: str,
    db: AsyncSession = Depends(get_db)
):
    try:
        return await RecommendationService.get_recommendation(db, recommendation_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
