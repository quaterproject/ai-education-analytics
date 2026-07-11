from typing import Optional, Sequence
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.human_review import HumanReview
from app.models.recommendation import Recommendation
from app.models.prediction import Prediction
from app.core.constants import PENDING_REVIEW

class ReviewRepository:
    @staticmethod
    async def create_human_review(db: AsyncSession, review_data: dict) -> HumanReview:
        review = HumanReview(**review_data)
        db.add(review)
        await db.flush()
        return review

    @staticmethod
    async def get_human_review(db: AsyncSession, review_id: str) -> Optional[HumanReview]:
        stmt = select(HumanReview).where(HumanReview.id == review_id).options(
            selectinload(HumanReview.recommendation).selectinload(Recommendation.prediction).selectinload(Prediction.student)
        )
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_recommendation_review(db: AsyncSession, rec_id: str) -> Optional[HumanReview]:
        stmt = select(HumanReview).where(HumanReview.recommendation_id == rec_id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_pending_reviews(db: AsyncSession) -> Sequence[HumanReview]:
        stmt = (
            select(HumanReview)
            .where(HumanReview.status == PENDING_REVIEW)
            .options(
                selectinload(HumanReview.recommendation)
                .selectinload(Recommendation.prediction)
                .selectinload(Prediction.student)
            )
            .order_by(HumanReview.created_at.desc())
        )
        result = await db.execute(stmt)
        return result.scalars().all()

    @staticmethod
    async def update_human_review(
        db: AsyncSession,
        review_id: str,
        update_data: dict
    ) -> Optional[HumanReview]:
        stmt = (
            update(HumanReview)
            .where(HumanReview.id == review_id)
            .values(**update_data)
            .execution_options(synchronize_session="fetch")
        )
        await db.execute(stmt)
        return await ReviewRepository.get_human_review(db, review_id)
