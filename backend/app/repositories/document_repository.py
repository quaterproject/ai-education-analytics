from typing import Optional, Sequence
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.document import Document

class DocumentRepository:
    @staticmethod
    async def create_document(db: AsyncSession, doc_data: dict) -> Document:
        doc = Document(**doc_data)
        db.add(doc)
        await db.flush()
        return doc

    @staticmethod
    async def get_document(db: AsyncSession, doc_id: str) -> Optional[Document]:
        stmt = select(Document).where(Document.id == doc_id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_student_documents(db: AsyncSession, student_id: str) -> Sequence[Document]:
        stmt = select(Document).where(Document.student_id == student_id)
        result = await db.execute(stmt)
        return result.scalars().all()

    @staticmethod
    async def update_document(
        db: AsyncSession, 
        doc_id: str, 
        update_data: dict
    ) -> Optional[Document]:
        stmt = (
            update(Document)
            .where(Document.id == doc_id)
            .values(**update_data)
            .execution_options(synchronize_session="fetch")
        )
        await db.execute(stmt)
        return await DocumentRepository.get_document(db, doc_id)
