import json
from typing import Dict, Any
from app.ai.providers.openai_service import OpenAIService
from app.ai.prompts.document_prompts import DOCUMENT_STRUCTURE_PROMPT, TEACHER_NOTES_PROMPT
from app.core.logging import logger

async def run_document_analysis_chain(extracted_text: str) -> Dict[str, Any]:
    """
    Transform unstructured PDF or document text into academic structured data.
    """
    llm = OpenAIService.get_model(temperature=0.0) # deterministic
    
    prompt_value = DOCUMENT_STRUCTURE_PROMPT.format_messages(
        extracted_text=extracted_text
    )
    
    try:
        response = await llm.ainvoke(prompt_value)
        content = response.content.strip()
        
        if content.startswith("```json"):
            content = content[7:]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()
        
        return json.loads(content)
    except Exception as e:
        logger.error(f"Document analysis chain failed: {e}", exc_info=True)
        return {
            "student_name": None,
            "student_id": None,
            "subjects": [],
            "grades": [],
            "attendance": None,
            "teacher_comments": [],
            "academic_concerns": ["Error parsing report content"]
        }

async def run_notes_analysis_chain(notes: str) -> Dict[str, Any]:
    """
    Analyze text notes from educators and extract structured concern flags.
    """
    llm = OpenAIService.get_model(temperature=0.1)
    
    prompt_value = TEACHER_NOTES_PROMPT.format_messages(notes=notes)
    
    try:
        response = await llm.ainvoke(prompt_value)
        content = response.content.strip()
        
        if content.startswith("```json"):
            content = content[7:]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()
        
        return json.loads(content)
    except Exception as e:
        logger.error(f"Teacher notes analysis chain failed: {e}", exc_info=True)
        return {
            "attendance_concern": False,
            "engagement_concern": False,
            "assignment_concern": False,
            "behavioral_concern": False,
            "summary": "Teacher note processing encountered an error."
        }
