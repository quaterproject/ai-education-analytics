from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.prediction_repository import PredictionRepository
from app.repositories.review_repository import ReviewRepository
from app.multimodal.feature_fusion import FeatureFusion
from app.multimodal.text_processor import TextProcessor
from app.ai.chains.recommendation_chain import run_recommendation_chain
from app.services.prediction_service import PredictionService
from app.models.recommendation import Recommendation
from app.core.exceptions import InvalidAcademicDataException
from app.core.constants import PENDING_REVIEW
from app.core.logging import logger

class RecommendationService:
    @staticmethod
    async def generate_recommendation(
        db: AsyncSession,
        prediction_id: str,
        teacher_notes: Optional[str] = None,
        document_id: Optional[str] = None
    ) -> Recommendation:
        """
        Generate academic recommendation by fusing prediction metrics, SHAP explanations,
        teacher notes, and uploaded document records.
        """
        logger.info(f"Generating recommendation plan for prediction: {prediction_id}")
        
        # 1. Fetch prediction
        prediction = await PredictionService.get_prediction(db, prediction_id)
        
        # 2. Get student details for raw metrics
        student = prediction.student
        
        # 3. Handle teacher notes (structured parse)
        structured_notes = None
        if teacher_notes:
            try:
                structured_notes = await TextProcessor.process_teacher_notes(teacher_notes)
            except Exception as e:
                logger.warning(f"Failed to pre-process teacher notes: {e}. Proceeding with raw notes.")

        # 4. Fetch document text
        pdf_texts = []
        image_texts = []
        
        # If document_id is provided, look it up. Otherwise, fetch all student documents
        from app.repositories.document_repository import DocumentRepository
        if document_id:
            doc = await DocumentRepository.get_document(db, document_id)
            if doc and doc.extracted_text and doc.processing_status == "COMPLETED":
                if doc.file_type.lower() == "pdf":
                    pdf_texts.append(doc.extracted_text)
                else:
                    image_texts.append(doc.extracted_text)
        else:
            docs = await DocumentRepository.get_student_documents(db, student.id)
            for doc in docs:
                if doc.extracted_text and doc.processing_status == "COMPLETED":
                    if doc.file_type.lower() == "pdf":
                        pdf_texts.append(doc.extracted_text)
                    else:
                        image_texts.append(doc.extracted_text)

        # 5. Execute Feature Fusion
        fused_context = FeatureFusion.fuse_features(
            prediction_obj=prediction,
            pdf_texts=pdf_texts,
            image_texts=image_texts,
            teacher_notes=teacher_notes,
            structured_notes=structured_notes
        )
        
        # 6. Run LangChain Recommendation Chain
        student_context = {
            "first_name": student.first_name,
            "last_name": student.last_name,
            "student_code": student.student_code,
            "age": student.age,
            "gender": student.gender,
            "school": student.school,
            "features": prediction.feature_values
        }
        
        rec_data = await run_recommendation_chain(
            risk_level=fused_context["risk_level"],
            confidence=fused_context["confidence"],
            risk_factors=fused_context["risk_factors"],
            protective_factors=fused_context["protective_factors"],
            student_context=student_context,
            document_context=fused_context["document_context"],
            teacher_notes=fused_context["teacher_notes"]
        )
        
        # 7. Create Recommendation Model
        rec_payload = {
            "prediction_id": prediction_id,
            "title": rec_data["title"],
            "priority": rec_data["priority"],
            "summary": rec_data["summary"],
            "recommended_actions": rec_data["recommended_actions"],
            "monitoring_plan": rec_data["monitoring_plan"],
            "success_indicators": rec_data["success_indicators"],
            "review_period_days": rec_data.get("review_period_days", 14),
            "llm_model": rec_data["llm_model"]
        }
        
        recommendation = await PredictionRepository.create_recommendation(db, rec_payload)
        await db.commit()
        
        # 8. Create HumanReview record (initialized to PENDING_REVIEW)
        # Store a complete serializable copy of the original recommendation fields
        original_copy = {
            "title": recommendation.title,
            "priority": recommendation.priority,
            "summary": recommendation.summary,
            "recommended_actions": recommendation.recommended_actions,
            "monitoring_plan": recommendation.monitoring_plan,
            "success_indicators": recommendation.success_indicators,
            "review_period_days": recommendation.review_period_days,
            "llm_model": recommendation.llm_model
        }
        
        review_payload = {
            "recommendation_id": recommendation.id,
            "status": PENDING_REVIEW,
            "original_recommendation": original_copy,
            "modified_recommendation": None,
            "reviewed_by": None,
            "educator_comment": None,
            "rejection_reason": None,
            "reviewed_at": None
        }
        
        await ReviewRepository.create_human_review(db, review_payload)
        await db.commit()
        
        return recommendation

    @staticmethod
    async def get_recommendation(db: AsyncSession, rec_id: str) -> Recommendation:
        rec = await PredictionRepository.get_recommendation(db, rec_id)
        if not rec:
            raise InvalidAcademicDataException(f"Recommendation with ID '{rec_id}' not found.")
        return rec
