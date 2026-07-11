from typing import Dict, Any
from app.ai.chains.document_analysis_chain import run_notes_analysis_chain
from app.core.exceptions import DocumentProcessingException
from app.core.logging import logger

class TextProcessor:
    @staticmethod
    async def process_teacher_notes(notes: str) -> Dict[str, Any]:
        """
        Send teacher notes to LangChain to extract structured concerns.
        """
        if not notes.strip():
            return {
                "attendance_concern": False,
                "engagement_concern": False,
                "assignment_concern": False,
                "behavioral_concern": False,
                "summary": ""
            }
            
        try:
            structured_notes = await run_notes_analysis_chain(notes)
            return structured_notes
        except Exception as e:
            logger.error(f"Text processor notes parsing failed: {e}", exc_info=True)
            raise DocumentProcessingException(f"Failed to process teacher notes: {str(e)}")
