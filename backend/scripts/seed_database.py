import asyncio
from sqlalchemy import delete
from app.core.database import AsyncSessionLocal
from app.models.student import Student
from app.models.academic_record import AcademicRecord
from app.models.document import Document
from app.models.prediction import Prediction
from app.models.recommendation import Recommendation
from app.models.human_review import HumanReview
from app.services.prediction_service import PredictionService
from app.services.recommendation_service import RecommendationService
from app.services.human_review_service import HumanReviewService
from app.schemas.review import ReviewModifyRequest, RecommendationModificationFields

async def seed_data():
    print("Connecting to database for seeding...")
    
    async with AsyncSessionLocal() as db:
        # Clear tables
        print("Clearing existing tables...")
        await db.execute(delete(HumanReview))
        await db.execute(delete(Recommendation))
        await db.execute(delete(Prediction))
        await db.execute(delete(Document))
        await db.execute(delete(AcademicRecord))
        await db.execute(delete(Student))
        await db.commit()
        
        students_data = [
            {
                "student_code": "GP-001",
                "first_name": "Alexander",
                "last_name": "Wright",
                "age": 17,
                "gender": "M",
                "school": "GP",
                "records": [
                    {
                        "study_time": 1,
                        "failures": 2,
                        "absences": 18,
                        "family_support": "no",
                        "school_support": "yes",
                        "internet_access": "no",
                        "health": 3,
                        "g1": 8.0,
                        "g2": 7.0
                    }
                ]
            },
            {
                "student_code": "GP-002",
                "first_name": "Sophia",
                "last_name": "Martinez",
                "age": 16,
                "gender": "F",
                "school": "GP",
                "records": [
                    {
                        "study_time": 3,
                        "failures": 0,
                        "absences": 2,
                        "family_support": "yes",
                        "school_support": "no",
                        "internet_access": "yes",
                        "health": 5,
                        "g1": 16.0,
                        "g2": 17.0
                    }
                ]
            },
            {
                "student_code": "MS-001",
                "first_name": "Liam",
                "last_name": "O'Connor",
                "age": 18,
                "gender": "M",
                "school": "MS",
                "records": [
                    {
                        "study_time": 2,
                        "failures": 1,
                        "absences": 11,
                        "family_support": "yes",
                        "school_support": "no",
                        "internet_access": "yes",
                        "health": 4,
                        "g1": 11.0,
                        "g2": 10.0
                    }
                ]
            },
            {
                "student_code": "GP-003",
                "first_name": "Emily",
                "last_name": "Chen",
                "age": 15,
                "gender": "F",
                "school": "GP",
                "records": [
                    {
                        "study_time": 4,
                        "failures": 0,
                        "absences": 0,
                        "family_support": "yes",
                        "school_support": "yes",
                        "internet_access": "yes",
                        "health": 4,
                        "g1": 18.0,
                        "g2": 19.0
                    }
                ]
            },
            {
                "student_code": "MS-002",
                "first_name": "Noah",
                "last_name": "Silva",
                "age": 17,
                "gender": "M",
                "school": "MS",
                "records": [
                    {
                        "study_time": 1,
                        "failures": 3,
                        "absences": 22,
                        "family_support": "no",
                        "school_support": "no",
                        "internet_access": "yes",
                        "health": 2,
                        "g1": 6.0,
                        "g2": 5.0
                    }
                ]
            }
        ]
        
        seeded_students = []
        
        # Insert students and records
        for s_info in students_data:
            print(f"Seeding student {s_info['first_name']} {s_info['last_name']}...")
            student = Student(
                student_code=s_info["student_code"],
                first_name=s_info["first_name"],
                last_name=s_info["last_name"],
                age=s_info["age"],
                gender=s_info["gender"],
                school=s_info["school"]
            )
            db.add(student)
            await db.flush()
            
            for r_info in s_info["records"]:
                record = AcademicRecord(
                    student_id=student.id,
                    study_time=r_info["study_time"],
                    failures=r_info["failures"],
                    absences=r_info["absences"],
                    family_support=r_info["family_support"],
                    school_support=r_info["school_support"],
                    internet_access=r_info["internet_access"],
                    health=r_info["health"],
                    g1=r_info["g1"],
                    g2=r_info["g2"]
                )
                db.add(record)
            
            seeded_students.append(student)
            
        await db.commit()
        print("Student and academic record seeding complete.")

        # Ensure the ML model predictor is loaded for generating predictions
        from app.ml.inference.predictor import predictor
        predictor.load_model()
        
        # If model is loaded, generate predictions and recommendations for some students
        if predictor.is_loaded:
            print("Generating initial predictions, recommendations, and reviews...")
            # 1. Alexander Wright (High Risk) -> Pending Review Recommendation
            p1 = await PredictionService.predict_student_risk(db, seeded_students[0].id)
            await RecommendationService.generate_recommendation(
                db, p1.id, 
                teacher_notes="Alexander has been skipping class frequently. His algebra grades have dropped significantly and he doesn't do homework."
            )
            
            # 2. Sophia Martinez (Low Risk) -> Approved Recommendation
            p2 = await PredictionService.predict_student_risk(db, seeded_students[1].id)
            r2 = await RecommendationService.generate_recommendation(
                db, p2.id,
                teacher_notes="Sophia is performing exceptionally well. Excellent student, no concerns."
            )
            # Approve it
            from app.schemas.review import ReviewApproveRequest
            await HumanReviewService.approve_recommendation(
                db, r2.id, 
                ReviewApproveRequest(reviewed_by="Principal Skinner", educator_comment="Highly deserved. Keep up the encouragement.")
            )
            
            # 3. Liam O'Connor (Medium Risk) -> Modified Recommendation
            p3 = await PredictionService.predict_student_risk(db, seeded_students[2].id)
            r3 = await RecommendationService.generate_recommendation(
                db, p3.id,
                teacher_notes="Liam is borderline. He needs some math tutoring support."
            )
            # Modify it
            mod_req = ReviewModifyRequest(
                reviewed_by="Adviser Crabapple",
                educator_comment="Adding custom math tutoring details.",
                modified_recommendation=RecommendationModificationFields(
                    title="Custom Math Intervention Plan for Liam",
                    priority="MEDIUM",
                    summary="Intervention centered around mathematics peer tutoring.",
                    recommended_actions=[
                        "Enroll Liam in the Wednesday Peer Tutoring group.",
                        "Meet with Liam's parents to discuss weekly goals."
                    ],
                    monitoring_plan=["Advisor check-in every Friday morning."],
                    success_indicators=["Obtains a score of at least 12 in the next calculus quiz."],
                    review_period_days=10
                )
            )
            await HumanReviewService.modify_recommendation(db, r3.id, mod_req)
            
            # 4. Noah Silva (High Risk) -> Rejected Recommendation
            p5 = await PredictionService.predict_student_risk(db, seeded_students[4].id)
            r5 = await RecommendationService.generate_recommendation(
                db, p5.id,
                teacher_notes="Noah has severe attendance and grade deficits."
            )
            from app.schemas.review import ReviewRejectRequest
            await HumanReviewService.reject_recommendation(
                db, r5.id,
                ReviewRejectRequest(reviewed_by="Principal Skinner", rejection_reason="Student has already transferred schools.")
            )
            
            print("Successfully generated predictions, recommendations, and reviews.")
        else:
            print("Skipped prediction seeding because the ML model is not trained yet.")

if __name__ == "__main__":
    asyncio.run(seed_data())
