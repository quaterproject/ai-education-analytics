from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.api.dependencies import get_db
from app.services.human_review_service import HumanReviewService
from app.schemas.review import (
    ReviewApproveRequest,
    ReviewRejectRequest,
    ReviewModifyRequest,
    HumanReviewOut,
    HumanReviewQueueOut
)
from app.core.exceptions import HumanReviewException

router = APIRouter()

@router.get("/reviews/pending", response_model=List[HumanReviewQueueOut])
async def list_pending_reviews(db: AsyncSession = Depends(get_db)):
    db_reviews = await HumanReviewService.get_pending_reviews(db)
    
    results = []
    for r in db_reviews:
        # Load related models to map to response structure
        rec = r.recommendation
        pred = rec.prediction if rec else None
        student = pred.student if pred else None
        
        results.append(
            HumanReviewQueueOut(
                id=r.id,
                recommendation_id=r.recommendation_id,
                status=r.status,
                reviewed_by=r.reviewed_by,
                educator_comment=r.educator_comment,
                rejection_reason=r.rejection_reason,
                original_recommendation=r.original_recommendation,
                modified_recommendation=r.modified_recommendation,
                reviewed_at=r.reviewed_at,
                created_at=r.created_at,
                recommendation=rec,
                student_name=f"{student.first_name} {student.last_name}" if student else None,
                student_code=student.student_code if student else None,
                student_id=student.id if student else None,
                risk_level=pred.risk_level if pred else None,
                confidence=pred.confidence if pred else None
            )
        )
    return results

@router.post("/recommendations/{recommendation_id}/approve", response_model=HumanReviewOut)
async def approve_recommendation(
    recommendation_id: str,
    payload: ReviewApproveRequest,
    db: AsyncSession = Depends(get_db)
):
    try:
        return await HumanReviewService.approve_recommendation(db, recommendation_id, payload)
    except HumanReviewException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message
        )

@router.post("/recommendations/{recommendation_id}/reject", response_model=HumanReviewOut)
async def reject_recommendation(
    recommendation_id: str,
    payload: ReviewRejectRequest,
    db: AsyncSession = Depends(get_db)
):
    try:
        return await HumanReviewService.reject_recommendation(db, recommendation_id, payload)
    except HumanReviewException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message
        )

@router.post("/recommendations/{recommendation_id}/modify", response_model=HumanReviewOut)
async def modify_recommendation(
    recommendation_id: str,
    payload: ReviewModifyRequest,
    db: AsyncSession = Depends(get_db)
):
    try:
        return await HumanReviewService.modify_recommendation(db, recommendation_id, payload)
    except HumanReviewException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message
        )
