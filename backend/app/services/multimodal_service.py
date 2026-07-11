from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.document_repository import DocumentRepository
from app.multimodal.pdf_processor import PDFProcessor
from app.multimodal.image_processor import ImageProcessor
from app.ai.providers.cohere_document_service import CohereDocumentService
from app.models.document import Document
from app.core.exceptions import DocumentProcessingException
from app.core.logging import logger

class MultimodalService:
    def __init__(self):
        self.cohere_service = CohereDocumentService()
        self.image_processor = ImageProcessor()

    async def process_and_save_document(
        self,
        db: AsyncSession,
        student_id: str,
        file_path: str,
        filename: str,
        file_type: str
    ) -> Document:
        """
        Extract text, parse structured data from the document, and persist in the database.
        """
        logger.info(f"Processing uploaded document: {filename} of type {file_type} for student {student_id}")
        
        # 1. Create a pending document record
        doc_data = {
            "student_id": student_id,
            "filename": filename,
            "file_type": file_type,
            "file_path": file_path,
            "processing_status": "PROCESSING",
            "extracted_text": None,
            "structured_data": None
        }
        document = await DocumentRepository.create_document(db, doc_data)
        await db.commit()
        
        try:
            extracted_text = ""
            
            # 2. Extract raw text depending on file type
            if file_type.lower() == "pdf":
                extracted_text = PDFProcessor.extract_text(file_path)
            elif file_type.lower() in ["png", "jpg", "jpeg", "webp"]:
                extracted_text = await self.image_processor.extract_text_from_image(file_path)
            else:
                raise DocumentProcessingException(f"Unsupported file type: {file_type}")
                
            # 3. Structure extracted text semantically
            structured_data = await self.cohere_service.structure_document_text(extracted_text)
            
            # 4. Update and complete document record
            update_data = {
                "processing_status": "COMPLETED",
                "extracted_text": extracted_text,
                "structured_data": structured_data
            }
            updated_doc = await DocumentRepository.update_document(db, document.id, update_data)
            await db.commit()
            return updated_doc
            
        except Exception as e:
            logger.error(f"Failed to process uploaded file {filename}: {e}", exc_info=True)
            # Update status to failed
            update_data = {
                "processing_status": "FAILED",
                "extracted_text": f"Error: {str(e)}",
                "structured_data": None
            }
            await DocumentRepository.update_document(db, document.id, update_data)
            await db.commit()
            raise DocumentProcessingException(f"Document processing failed: {str(e)}")

    async def get_document(self, db: AsyncSession, doc_id: str) -> Document:
        doc = await DocumentRepository.get_document(db, doc_id)
        if not doc:
            raise DocumentProcessingException(f"Document with ID '{doc_id}' not found.")
        return doc

    async def get_student_documents(self, db: AsyncSession, student_id: str) -> list[Document]:
        return list(await DocumentRepository.get_student_documents(db, student_id))
