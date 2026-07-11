from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.api.dependencies import get_db
from app.services.student_service import StudentService
from app.schemas.student import StudentCreate, StudentUpdate, StudentOut
from app.schemas.academic_record import AcademicRecordCreate, AcademicRecordOut

router = APIRouter()

@router.get("", response_model=List[StudentOut])
async def list_students(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    return await StudentService.get_students(db, skip=skip, limit=limit)

@router.post("", response_model=StudentOut, status_code=status.HTTP_201_CREATED)
async def create_student(
    student_in: StudentCreate,
    db: AsyncSession = Depends(get_db)
):
    return await StudentService.create_student(db, student_in)

@router.get("/{student_id}", response_model=StudentOut)
async def get_student(
    student_id: str,
    db: AsyncSession = Depends(get_db)
):
    return await StudentService.get_student(db, student_id)

@router.put("/{student_id}", response_model=StudentOut)
async def update_student(
    student_id: str,
    student_in: StudentUpdate,
    db: AsyncSession = Depends(get_db)
):
    return await StudentService.update_student(db, student_id, student_in)

@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(
    student_id: str,
    db: AsyncSession = Depends(get_db)
):
    await StudentService.delete_student(db, student_id)
    return None

@router.post("/{student_id}/records", response_model=AcademicRecordOut, status_code=status.HTTP_201_CREATED)
async def add_academic_record(
    student_id: str,
    record_in: AcademicRecordCreate,
    db: AsyncSession = Depends(get_db)
):
    return await StudentService.add_academic_record(db, student_id, record_in)

@router.get("/{student_id}/records", response_model=List[AcademicRecordOut])
async def get_academic_records(
    student_id: str,
    db: AsyncSession = Depends(get_db)
):
    return await StudentService.get_academic_records(db, student_id)
