from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.api.dependencies import get_db
from app.services.prediction_service import PredictionService
from app.schemas.prediction import PredictionOut

router = APIRouter()

@router.post("/students/{student_id}/predict", response_model=PredictionOut)
async def predict_student_risk(
    student_id: str,
    model_type: str = Query("LATE_STAGE", pattern="^(EARLY_WARNING|LATE_STAGE)$"),
    db: AsyncSession = Depends(get_db)
):
    return await PredictionService.predict_student_risk(db, student_id, model_type)

@router.get("/students/{student_id}/predictions", response_model=List[PredictionOut])
async def get_student_predictions(
    student_id: str,
    db: AsyncSession = Depends(get_db)
):
    return await PredictionService.get_student_predictions(db, student_id)

@router.get("/predictions/{prediction_id}", response_model=PredictionOut)
async def get_prediction(
    prediction_id: str,
    db: AsyncSession = Depends(get_db)
):
    return await PredictionService.get_prediction(db, prediction_id)
