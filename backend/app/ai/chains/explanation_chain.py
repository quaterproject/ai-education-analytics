import json
from typing import Dict, Any, List
from app.ai.providers.openai_service import OpenAIService
from app.ai.prompts.explanation_prompts import EXPLANATION_PROMPT
from app.core.logging import logger

async def run_explanation_chain(
    risk_level: str,
    confidence: float,
    class_probabilities: Dict[str, float],
    risk_factors: List[str],
    protective_factors: List[str],
    student_context: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Run LangChain explanation chain to translate numerical prediction metrics into clear explanations.
    """
    llm = OpenAIService.get_model(temperature=0.2)
    
    # Render prompt
    prompt_value = EXPLANATION_PROMPT.format_messages(
        risk_level=risk_level,
        confidence=confidence,
        class_probabilities=class_probabilities,
        risk_factors=risk_factors,
        protective_factors=protective_factors,
        student_context=student_context
    )
    
    try:
        response = await llm.ainvoke(prompt_value)
        content = response.content.strip()
        
        # Strip code blocks
        if content.startswith("```json"):
            content = content[7:]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()
        
        return json.loads(content)
    except Exception as e:
        logger.error(f"Explanation chain execution failed: {e}", exc_info=True)
        # Fallback explanation response
        return {
            "summary": f"Student is classified as {risk_level} with {confidence:.1%} confidence.",
            "risk_explanation": f"The student shows critical risk patterns related to their academic metrics, family support system, and absences. Primary drivers include: {', '.join(risk_factors[:3])}.",
            "key_concerns": risk_factors[:3],
            "protective_observations": protective_factors[:3]
        }
