import os
import uuid
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.student_service import StudentService
from app.services.prediction_service import PredictionService
from app.ai.chains.report_chain import run_report_chain
from app.reports.pdf_generator import PDFReportGenerator
from app.reports.docx_generator import DOCXReportGenerator
from app.schemas.report import ReportGenerateResponse
from app.core.config import settings
from app.core.exceptions import ReportGenerationException
from app.core.logging import logger

class ReportService:
    @staticmethod
    async def generate_student_report(
        db: AsyncSession,
        student_id: str,
        file_type: str = "pdf"
    ) -> ReportGenerateResponse:
        """
        Generate a downloadable student success report (PDF or DOCX).
        Aggregates prediction metrics, SHAP factors, and final educator decisions.
        """
        logger.info(f"Generating student success report (Type: {file_type}) for student: {student_id}")
        
        # 1. Fetch student
        student = await StudentService.get_student(db, student_id)
        
        # 2. Get latest prediction
        predictions = await PredictionService.get_student_predictions(db, student_id)
        if not predictions:
            raise ReportGenerationException(
                f"No risk assessments found for student '{student_id}'. Cannot generate report without a prediction."
            )
        latest_pred = predictions[0]
        
        # 3. Get recommendation and human review
        recommendation = latest_pred.recommendation
        review_details = {"status": "PENDING_REVIEW", "decision": "No educator review logged.", "educator_comments": "N/A", "rejection_reason": "N/A", "modification_details": "N/A", "reviewed_at": "N/A"}
        recommendation_details = {"title": "N/A", "priority": "N/A", "summary": "N/A", "recommended_actions": [], "monitoring_plan": [], "success_indicators": [], "review_period_days": 14}
        
        if recommendation:
            recommendation_details = {
                "title": recommendation.title,
                "priority": recommendation.priority,
                "summary": recommendation.summary,
                "recommended_actions": recommendation.recommended_actions,
                "monitoring_plan": recommendation.monitoring_plan,
                "success_indicators": recommendation.success_indicators,
                "review_period_days": recommendation.review_period_days
            }
            
            review = recommendation.human_review
            if review:
                review_details = {
                    "status": review.status,
                    "reviewed_by": review.reviewed_by or "N/A",
                    "educator_comment": review.educator_comment or "N/A",
                    "rejection_reason": review.rejection_reason or "N/A",
                    "modified_recommendation": review.modified_recommendation or {},
                    "reviewed_at": review.reviewed_at.strftime("%Y-%m-%d %H:%M:%S") if review.reviewed_at else "N/A"
                }

        # 4. Extract document context
        doc_details = []
        for doc in student.documents:
            if doc.processing_status == "COMPLETED" and doc.extracted_text:
                doc_details.append(f"Document ({doc.filename}): {doc.extracted_text[:200]}...")
        doc_context = "\n".join(doc_details) if doc_details else "No document uploads recorded."
        
        # 5. Extract latest teacher notes (from prediction features or recommendation inputs)
        teacher_notes = latest_pred.feature_values.get("teacher_notes", "")
        
        # 6. Generate Narrative using ReportChain
        student_context = {
            "G1": latest_pred.feature_values.get("G1", 0.0),
            "G2": latest_pred.feature_values.get("G2", 0.0),
            "absences": latest_pred.feature_values.get("absences", 0.0),
            "study_time": latest_pred.feature_values.get("study_time", 2.0),
            "failures": latest_pred.feature_values.get("failures", 0.0)
        }
        
        narrative = await run_report_chain(
            first_name=student.first_name,
            last_name=student.last_name,
            student_code=student.student_code,
            age=student.age,
            school=student.school,
            risk_level=latest_pred.risk_level,
            confidence=latest_pred.confidence,
            risk_factors=latest_pred.risk_factors,
            protective_factors=latest_pred.protective_factors,
            student_context=student_context,
            document_context={"summary": doc_context},
            teacher_notes=teacher_notes,
            recommendation_details=recommendation_details,
            review_details=review_details
        )
        
        # 7. Write report to disk
        report_id = str(uuid.uuid4())
        os.makedirs(settings.REPORT_DIR, exist_ok=True)
        
        filename = f"{student.student_code}_risk_report_{report_id}.{file_type.lower()}"
        file_path = os.path.join(settings.REPORT_DIR, filename)
        
        report_data = {
            "student": student,
            "prediction": latest_pred,
            "recommendation": recommendation_details,
            "review": review_details,
            "narrative": narrative,
            "generated_at": datetime.utcnow()
        }
        
        try:
            if file_type.lower() == "pdf":
                PDFReportGenerator.generate(file_path, report_data)
            elif file_type.lower() == "docx":
                DOCXReportGenerator.generate(file_path, report_data)
            else:
                raise ReportGenerationException(f"Unsupported export type: {file_type}")
        except Exception as e:
            logger.error(f"Report file generation failed: {e}", exc_info=True)
            raise ReportGenerationException(f"Failed to generate {file_type.upper()} report file: {str(e)}")

        # Clean download url mapping to backend API
        download_url = f"/api/v1/reports/{report_id}/download"
        
        return ReportGenerateResponse(
            report_id=report_id,
            file_type=file_type.lower(),
            filename=filename,
            download_url=download_url,
            generated_at=datetime.utcnow()
        )
