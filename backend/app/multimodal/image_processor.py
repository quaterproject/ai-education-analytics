from app.ai.providers.cohere_document_service import CohereDocumentService
from app.core.exceptions import DocumentProcessingException
from app.core.logging import logger

class ImageProcessor:
    def __init__(self):
        self.cohere_service = CohereDocumentService()

    async def extract_text_from_image(self, file_path: str) -> str:
        """
        Extract text from an image using the Cohere vision service.
        """
        try:
            # Call cohere adapter
            text = await self.cohere_service.analyze_document_image(file_path)
            if not text:
                raise DocumentProcessingException("No text could be extracted from the document image.")
            return text
        except Exception as e:
            logger.error(f"Image text extraction failed: {e}", exc_info=True)
            raise DocumentProcessingException(f"Failed to process document image: {str(e)}")
