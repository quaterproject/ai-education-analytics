from datetime import datetime
from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.review_repository import ReviewRepository
from app.models.human_review import HumanReview
from app.schemas.review import ReviewApproveRequest, ReviewRejectRequest, ReviewModifyRequest
from app.core.exceptions import HumanReviewException
from app.core.constants import APPROVED, REJECTED, MODIFIED

class HumanReviewService:
    @staticmethod
    async def approve_recommendation(
        db: AsyncSession,
        recommendation_id: str,
        approve_in: ReviewApproveRequest
    ) -> HumanReview:
        """
        Approve the recommendation, recording the reviewer details and optional comments.
        """
        # Find review record by recommendation_id
        review = await ReviewRepository.get_recommendation_review(db, recommendation_id)
        if not review:
            raise HumanReviewException(f"No review record found for recommendation ID '{recommendation_id}'")
            
        if review.status != "PENDING_REVIEW":
            raise HumanReviewException(f"Review has already been processed (Current status: '{review.status}')")
            
        update_data = {
            "status": APPROVED,
            "reviewed_by": approve_in.reviewed_by,
            "educator_comment": approve_in.educator_comment,
            "reviewed_at": datetime.utcnow()
        }
        
        updated = await ReviewRepository.update_human_review(db, review.id, update_data)
        await db.commit()
        return updated

    @staticmethod
    async def reject_recommendation(
        db: AsyncSession,
        recommendation_id: str,
        reject_in: ReviewRejectRequest
    ) -> HumanReview:
        """
        Reject the recommendation, recording the reviewer details and the required rejection reason.
        """
        # Find review record by recommendation_id
        review = await ReviewRepository.get_recommendation_review(db, recommendation_id)
        if not review:
            raise HumanReviewException(f"No review record found for recommendation ID '{recommendation_id}'")
            
        if review.status != "PENDING_REVIEW":
            raise HumanReviewException(f"Review has already been processed (Current status: '{review.status}')")
            
        if not reject_in.rejection_reason.strip():
            raise HumanReviewException("Rejection reason is required to reject a recommendation.")
            
        update_data = {
            "status": REJECTED,
            "reviewed_by": reject_in.reviewed_by,
            "rejection_reason": reject_in.rejection_reason,
            "reviewed_at": datetime.utcnow()
        }
        
        updated = await ReviewRepository.update_human_review(db, review.id, update_data)
        await db.commit()
        return updated

    @staticmethod
    async def modify_recommendation(
        db: AsyncSession,
        recommendation_id: str,
        modify_in: ReviewModifyRequest
    ) -> HumanReview:
        """
        Modify the recommendation, storing the new values separate from the original.
        """
        # Find review record by recommendation_id
        review = await ReviewRepository.get_recommendation_review(db, recommendation_id)
        if not review:
            raise HumanReviewException(f"No review record found for recommendation ID '{recommendation_id}'")
            
        if review.status != "PENDING_REVIEW":
            raise HumanReviewException(f"Review has already been processed (Current status: '{review.status}')")
            
        # Compile modified fields
        mod_dict = modify_in.modified_recommendation.model_dump()
        
        # Inject model key from original to keep track of model
        mod_dict["llm_model"] = review.original_recommendation.get("llm_model", "unknown")
        
        update_data = {
            "status": MODIFIED,
            "reviewed_by": modify_in.reviewed_by,
            "educator_comment": modify_in.educator_comment,
            "modified_recommendation": mod_dict,
            "reviewed_at": datetime.utcnow()
        }
        
        updated = await ReviewRepository.update_human_review(db, review.id, update_data)
        await db.commit()
        return updated

    @staticmethod
    async def get_pending_reviews(db: AsyncSession) -> Sequence[HumanReview]:
        return await ReviewRepository.get_pending_reviews(db)

    @staticmethod
    async def get_review_by_id(db: AsyncSession, review_id: str) -> HumanReview:
        review = await ReviewRepository.get_human_review(db, review_id)
        if not review:
            raise HumanReviewException(f"Review with ID '{review_id}' not found.")
        return review
