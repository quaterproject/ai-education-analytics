from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.prediction_repository import PredictionRepository
from app.services.student_service import StudentService
from app.ml.inference.predictor import predictor
from app.ml.explainability.shap_explainer import explain_student_risk
from app.models.prediction import Prediction
from app.core.exceptions import InvalidAcademicDataException

class PredictionService:
    @staticmethod
    async def predict_student_risk(
        db: AsyncSession, 
        student_id: str,
        model_type: str = "LATE_STAGE"
    ) -> Prediction:
        """
        Execute student risk prediction using tabular records.
        """
        # 1. Fetch student and check records
        student = await StudentService.get_student(db, student_id)
        if not student.academic_records:
            raise InvalidAcademicDataException(
                f"Student '{student_id}' has no academic performance records. Prediction requires at least one tabular record."
            )
            
        # Get latest academic record
        latest_record = sorted(student.academic_records, key=lambda r: r.created_at, reverse=True)[0]
        
        # 2. Map academic record and student profile to feature dictionary
        features = {
            'school': student.school,
            'sex': student.gender,
            'age': student.age,
            'address': 'U', # default or can be extended
            'famsize': 'GT3',
            'Pstatus': 'T',
            'Medu': 3, # defaults
            'Fedu': 3,
            'Mjob': 'other',
            'Fjob': 'other',
            'reason': 'course',
            'guardian': 'mother',
            'traveltime': 1,
            'studytime': latest_record.study_time,
            'failures': latest_record.failures,
            'schoolsup': latest_record.school_support,
            'famsup': latest_record.family_support,
            'paid': 'no',
            'activities': 'no',
            'nursery': 'yes',
            'higher': 'yes',
            'internet': latest_record.internet_access,
            'romantic': 'no',
            'famrel': 4,
            'freetime': 3,
            'goout': 3,
            'Dalc': 1,
            'Walc': 1,
            'health': latest_record.health,
            'absences': latest_record.absences,
            'G1': latest_record.g1,
            'G2': latest_record.g2
        }
        
        # Adjust features if EARLY_WARNING is selected (G1/G2 dropped during preprocessor transformation)
        # Note: predictor automatically handles G1/G2 dropping inside transform if model_type == "EARLY_WARNING"
        predictor.model_type = model_type
        if predictor.preprocessor:
            predictor.preprocessor.model_type = model_type
            
        # 3. Execute prediction
        risk_level, confidence, class_probabilities, X_preprocessed = predictor.predict(features)
        
        # 4. Compute SHAP explanations
        shap_values, risk_factors, protective_factors = explain_student_risk(
            predictor, X_preprocessed, risk_level
        )
        
        # 5. Build schema for saving
        # Create prediction metadata and log
        pred_data = {
            "student_id": student_id,
            "risk_level": risk_level,
            "confidence": confidence,
            "class_probabilities": class_probabilities,
            "model_version": f"StudentRiskANN-{model_type}-1.0",
            "feature_values": features,
            "shap_values": shap_values,
            "risk_factors": risk_factors,
            "protective_factors": protective_factors
        }
        
        prediction = await PredictionRepository.create_prediction(db, pred_data)
        return prediction

    @staticmethod
    async def get_prediction(db: AsyncSession, prediction_id: str) -> Prediction:
        pred = await PredictionRepository.get_prediction(db, prediction_id)
        if not pred:
            raise InvalidAcademicDataException(f"Prediction with ID '{prediction_id}' was not found.")
        return pred

    @staticmethod
    async def get_student_predictions(db: AsyncSession, student_id: str) -> Sequence[Prediction]:
        await StudentService.get_student(db, student_id)
        return await PredictionRepository.get_student_predictions(db, student_id)
