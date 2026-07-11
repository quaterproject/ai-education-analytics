import json
from typing import Dict, Any, List, Optional
from app.ai.providers.openai_service import OpenAIService
from app.ai.prompts.recommendation_prompts import RECOMMENDATION_PROMPT
from app.core.logging import logger

async def run_recommendation_chain(
    risk_level: str,
    confidence: float,
    risk_factors: List[str],
    protective_factors: List[str],
    student_context: Dict[str, Any],
    document_context: Optional[str] = None,
    teacher_notes: Optional[str] = None
) -> Dict[str, Any]:
    """
    Run LangChain recommendation chain to generate a student intervention plan.
    """
    llm = OpenAIService.get_model(temperature=0.3)
    
    prompt_value = RECOMMENDATION_PROMPT.format_messages(
        risk_level=risk_level,
        confidence=confidence,
        risk_factors=risk_factors,
        protective_factors=protective_factors,
        student_context=student_context,
        document_context=document_context or "No additional document context uploaded.",
        teacher_notes=teacher_notes or "No educator notes submitted."
    )
    
    try:
        response = await llm.ainvoke(prompt_value)
        content = response.content.strip()
        
        if content.startswith("```json"):
            content = content[7:]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()
        
        parsed = json.loads(content)
        # Ensure we record which model version generated the recommendation
        parsed["llm_model"] = llm.model_name
        return parsed
        
    except Exception as e:
        logger.error(f"Recommendation chain execution failed: {e}", exc_info=True)
        # Fallback intervention plan
        return {
            "title": f"Academic Success Plan for {student_context.get('student_code', 'Student')}",
            "priority": "HIGH" if risk_level == "HIGH_RISK" else ("MEDIUM" if risk_level == "MEDIUM_RISK" else "LOW"),
            "summary": "Regular monitoring and basic academic support are suggested to secure progress.",
            "recommended_actions": [
                "Schedule a progress check-in meeting with the student's academic advisor.",
                "Review attendance weekly and establish contact with parents/guardians.",
                "Promote structured study times and suggest peer tutoring groups."
            ],
            "monitoring_plan": [
                "Track class attendance and check weekly for missing assignments."
            ],
            "success_indicators": [
                "No further absences registered during the review cycle.",
                "Completed algebra and class homework exercises."
            ],
            "review_period_days": 14,
            "llm_model": llm.model_name
        }
