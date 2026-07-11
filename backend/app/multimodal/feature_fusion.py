from typing import Dict, Any, List, Optional
from app.core.logging import logger

class FeatureFusion:
    @staticmethod
    def fuse_features(
        prediction_obj: Any,
        pdf_texts: List[str],
        image_texts: List[str],
        teacher_notes: Optional[str] = None,
        structured_notes: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Synthesize numerical prediction parameters, SHAP explanations,
        unstructured document texts (PDF/Images), and note analyses into a unified context payload.
        """
        logger.info("Executing Multimodal Feature Fusion...")
        
        # 1. Gather prediction context
        ann_risk = prediction_obj.risk_level
        confidence = prediction_obj.confidence
        probabilities = prediction_obj.class_probabilities
        risk_factors = prediction_obj.risk_factors
        protective_factors = prediction_obj.protective_factors
        
        # 2. Compile document evidence
        document_evidence = []
        if pdf_texts:
            document_evidence.append("PDF Documents Extracted:\n" + "\n---\n".join(pdf_texts))
        if image_texts:
            document_evidence.append("Scanned Document Images Extracted:\n" + "\n---\n".join(image_texts))
            
        doc_context_str = "\n\n".join(document_evidence) if document_evidence else "No additional documents uploaded."
        
        # 3. Compile notes context
        notes_str = teacher_notes or "No educator notes provided."
        if structured_notes:
            concern_flags = [
                k for k, v in structured_notes.items() 
                if k.endswith("_concern") and v is True
            ]
            if concern_flags:
                notes_str += f"\n(Extracted Concern Flags: {', '.join(concern_flags)})"
                
        # 4. Synthesize for LLM
        fused_context = {
            "risk_level": ann_risk,
            "confidence": confidence,
            "class_probabilities": probabilities,
            "risk_factors": risk_factors,
            "protective_factors": protective_factors,
            "document_context": doc_context_str,
            "teacher_notes": notes_str
        }
        
        return fused_context
