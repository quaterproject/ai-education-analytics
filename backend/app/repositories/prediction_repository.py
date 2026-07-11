from typing import Optional, Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.prediction import Prediction
from app.models.recommendation import Recommendation

class PredictionRepository:
    @staticmethod
    async def create_prediction(db: AsyncSession, prediction_data: dict) -> Prediction:
        prediction = Prediction(**prediction_data)
        db.add(prediction)
        await db.flush()
        return prediction

    @staticmethod
    async def get_prediction(db: AsyncSession, prediction_id: str) -> Optional[Prediction]:
        stmt = select(Prediction).where(Prediction.id == prediction_id).options(
            selectinload(Prediction.student),
            selectinload(Prediction.recommendation).selectinload(Recommendation.human_review)
        )
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_student_predictions(db: AsyncSession, student_id: str) -> Sequence[Prediction]:
        stmt = select(Prediction).where(Prediction.student_id == student_id).options(
            selectinload(Prediction.recommendation).selectinload(Recommendation.human_review)
        ).order_by(Prediction.created_at.desc())
        result = await db.execute(stmt)
        return result.scalars().all()

    @staticmethod
    async def create_recommendation(db: AsyncSession, rec_data: dict) -> Recommendation:
        rec = Recommendation(**rec_data)
        db.add(rec)
        await db.flush()
        return rec

    @staticmethod
    async def get_recommendation(db: AsyncSession, rec_id: str) -> Optional[Recommendation]:
        stmt = select(Recommendation).where(Recommendation.id == rec_id).options(
            selectinload(Recommendation.prediction).selectinload(Prediction.student),
            selectinload(Recommendation.human_review)
        )
        result = await db.execute(stmt)
        return result.scalar_one_or_none()
