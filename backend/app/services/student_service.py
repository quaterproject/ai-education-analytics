from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.student_repository import StudentRepository
from app.models.student import Student
from app.models.academic_record import AcademicRecord
from app.schemas.student import StudentCreate, StudentUpdate
from app.schemas.academic_record import AcademicRecordCreate
from app.core.exceptions import StudentNotFoundException, InvalidAcademicDataException

class StudentService:
    @staticmethod
    async def get_student(db: AsyncSession, student_id: str) -> Student:
        student = await StudentRepository.get_student(db, student_id)
        if not student:
            raise StudentNotFoundException(student_id)
        return student

    @staticmethod
    async def get_students(db: AsyncSession, skip: int = 0, limit: int = 100) -> Sequence[Student]:
        return await StudentRepository.get_students(db, skip, limit)

    @staticmethod
    async def create_student(db: AsyncSession, student_in: StudentCreate) -> Student:
        # Check if student code is already taken
        existing = await StudentRepository.get_student_by_code(db, student_in.student_code)
        if existing:
            raise InvalidAcademicDataException(
                f"Student code '{student_in.student_code}' is already registered."
            )
        return await StudentRepository.create_student(db, student_in.model_dump())

    @staticmethod
    async def update_student(db: AsyncSession, student_id: str, student_in: StudentUpdate) -> Student:
        # Verify student exists
        await StudentService.get_student(db, student_id)
        
        update_dict = student_in.model_dump(exclude_unset=True)
        updated = await StudentRepository.update_student(db, student_id, update_dict)
        if not updated:
            raise StudentNotFoundException(student_id)
        return updated

    @staticmethod
    async def delete_student(db: AsyncSession, student_id: str) -> bool:
        # Verify student exists
        await StudentService.get_student(db, student_id)
        return await StudentRepository.delete_student(db, student_id)

    @staticmethod
    async def add_academic_record(
        db: AsyncSession, 
        student_id: str, 
        record_in: AcademicRecordCreate
    ) -> AcademicRecord:
        # Verify student exists
        await StudentService.get_student(db, student_id)
        return await StudentRepository.add_academic_record(db, student_id, record_in.model_dump())

    @staticmethod
    async def get_academic_records(db: AsyncSession, student_id: str) -> Sequence[AcademicRecord]:
        await StudentService.get_student(db, student_id)
        return await StudentRepository.get_academic_records(db, student_id)
class_name = StudentService
