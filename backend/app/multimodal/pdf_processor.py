import os
import pypdf
from app.core.exceptions import DocumentProcessingException
from app.core.logging import logger

class PDFProcessor:
    @staticmethod
    def extract_text(file_path: str) -> str:
        """
        Extract text content from a PDF document.
        Raises DocumentProcessingException if extraction fails.
        """
        if not os.path.exists(file_path):
            raise DocumentProcessingException(f"PDF file not found at path: {file_path}")
            
        try:
            reader = pypdf.PdfReader(file_path)
            extracted_text = []
            
            for page_num, page in enumerate(reader.pages):
                text = page.extract_text()
                if text:
                    extracted_text.append(text)
                    
            full_text = "\n".join(extracted_text).strip()
            
            if not full_text:
                logger.warning(f"No readable text extracted from PDF: {file_path}. Scanned document assumed.")
                raise DocumentProcessingException(
                    "The PDF contains no digital text. It may be a scanned document image. Please process using document vision."
                )
                
            return full_text
            
        except DocumentProcessingException:
            raise
        except Exception as e:
            logger.error(f"Error reading PDF file {file_path}: {e}", exc_info=True)
            raise DocumentProcessingException(f"Failed to parse PDF document: {str(e)}")
