from typing import Optional, Sequence
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.student import Student
from app.models.academic_record import AcademicRecord

class StudentRepository:
    @staticmethod
    async def get_student(db: AsyncSession, student_id: str) -> Optional[Student]:
        stmt = select(Student).where(Student.id == student_id).options(
            selectinload(Student.academic_records),
            selectinload(Student.documents),
            selectinload(Student.predictions)
        )
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_student_by_code(db: AsyncSession, student_code: str) -> Optional[Student]:
        stmt = select(Student).where(Student.student_code == student_code).options(
            selectinload(Student.academic_records)
        )
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_students(db: AsyncSession, skip: int = 0, limit: int = 100) -> Sequence[Student]:
        stmt = select(Student).options(
            selectinload(Student.academic_records)
        ).offset(skip).limit(limit)
        result = await db.execute(stmt)
        return result.scalars().all()

    @staticmethod
    async def create_student(db: AsyncSession, student_data: dict) -> Student:
        student = Student(**student_data)
        db.add(student)
        await db.flush()
        return student

    @staticmethod
    async def update_student(db: AsyncSession, student_id: str, student_data: dict) -> Optional[Student]:
        stmt = (
            update(Student)
            .where(Student.id == student_id)
            .values(**student_data)
            .execution_options(synchronize_session="fetch")
        )
        await db.execute(stmt)
        return await StudentRepository.get_student(db, student_id)

    @staticmethod
    async def delete_student(db: AsyncSession, student_id: str) -> bool:
        stmt = delete(Student).where(Student.id == student_id)
        result = await db.execute(stmt)
        return result.rowcount > 0

    @staticmethod
    async def add_academic_record(db: AsyncSession, student_id: str, record_data: dict) -> AcademicRecord:
        record = AcademicRecord(student_id=student_id, **record_data)
        db.add(record)
        await db.flush()
        return record

    @staticmethod
    async def get_academic_records(db: AsyncSession, student_id: str) -> Sequence[AcademicRecord]:
        stmt = select(AcademicRecord).where(AcademicRecord.student_id == student_id)
        result = await db.execute(stmt)
        return result.scalars().all()
