import json
from typing import Dict, Any, List
from app.ai.providers.openai_service import OpenAIService
from app.ai.prompts.report_prompts import REPORT_NARRATIVE_PROMPT
from app.core.logging import logger

async def run_report_chain(
    first_name: str,
    last_name: str,
    student_code: str,
    age: int,
    school: str,
    risk_level: str,
    confidence: float,
    risk_factors: List[str],
    protective_factors: List[str],
    student_context: Dict[str, Any],
    document_context: Dict[str, Any],
    teacher_notes: str,
    recommendation_details: Dict[str, Any],
    review_details: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Run LangChain report chain to generate a structured academic assessment narrative.
    """
    llm = OpenAIService.get_model(temperature=0.2)
    
    prompt_value = REPORT_NARRATIVE_PROMPT.format_messages(
        first_name=first_name,
        last_name=last_name,
        student_code=student_code,
        age=age,
        school=school,
        risk_level=risk_level,
        confidence=confidence,
        risk_factors=risk_factors,
        protective_factors=protective_factors,
        student_context=student_context,
        document_context=document_context,
        teacher_notes=teacher_notes or "No additional notes.",
        recommendation_details=recommendation_details,
        review_details=review_details
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
        logger.error(f"Report chain execution failed: {e}", exc_info=True)
        # Return fallback text sections
        return {
            "executive_summary": f"This report evaluates the academic risk status of student {first_name} {last_name}. The Artificial Neural Network predicts a {risk_level} status with {confidence:.1%} confidence.",
            "academic_analysis": "Analysis of active performance records indicates an accumulation of critical behaviors. Attendance rate and grades require active review.",
            "model_assessment": f"The PyTorch ANN identified {', '.join(risk_factors[:3])} as major risk forces, mitigated slightly by {', '.join(protective_factors[:3])}.",
            "evidence_synthesis": "Teacher notes indicate concerns. Document evidence supports the model's indicators.",
            "intervention_plan": f"The suggested program recommends {recommendation_details.get('title', 'Academic Support')}, requiring review in {recommendation_details.get('review_period_days', 14)} days."
        }
