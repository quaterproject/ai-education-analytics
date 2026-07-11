from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from typing import Dict, Any

class PDFReportGenerator:
    @staticmethod
    def generate(file_path: str, data: Dict[str, Any]):
        """
        Generate a professional PDF student risk assessment report.
        """
        # Load styles
        styles = getSampleStyleSheet()
        
        # Define clean, custom color styles
        primary_color = colors.HexColor("#1A365D")   # Deep Slate Blue
        secondary_color = colors.HexColor("#2B6CB0") # Medium Blue
        accent_color = colors.HexColor("#C53030")    # Soft Red (Risk)
        neutral_dark = colors.HexColor("#2D3748")    # Charcoal
        neutral_light = colors.HexColor("#EDF2F7")   # Light Grey
        
        # Modify existing styles or create new ones
        title_style = ParagraphStyle(
            'ReportTitle',
            parent=styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=22,
            textColor=primary_color,
            spaceAfter=15
        )
        
        h1_style = ParagraphStyle(
            'SectionHeader',
            parent=styles['Heading2'],
            fontName='Helvetica-Bold',
            fontSize=14,
            textColor=secondary_color,
            spaceBefore=15,
            spaceAfter=8,
            keepWithNext=True
        )
        
        h2_style = ParagraphStyle(
            'SubsectionHeader',
            parent=styles['Heading3'],
            fontName='Helvetica-Bold',
            fontSize=11,
            textColor=neutral_dark,
            spaceBefore=8,
            spaceAfter=4,
            keepWithNext=True
        )
        
        body_style = ParagraphStyle(
            'ReportBody',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=10,
            textColor=neutral_dark,
            leading=14,
            spaceAfter=8
        )
        
        bold_body_style = ParagraphStyle(
            'ReportBodyBold',
            parent=body_style,
            fontName='Helvetica-Bold'
        )

        disclaimer_style = ParagraphStyle(
            'ReportDisclaimer',
            parent=styles['Italic'],
            fontName='Helvetica-Oblique',
            fontSize=8,
            textColor=colors.HexColor("#718096"),
            leading=11
        )
        
        # Setup document template
        doc = SimpleDocTemplate(
            file_path,
            pagesize=letter,
            rightMargin=54, leftMargin=54,
            topMargin=54, bottomMargin=54
        )
        
        story = []
        
        student = data["student"]
        prediction = data["prediction"]
        recommendation = data["recommendation"]
        review = data["review"]
        narrative = data["narrative"]
        
        # --- Header ---
        story.append(Paragraph("EduPilot AI Student Risk Assessment", title_style))
        story.append(Paragraph(f"Generated on {data['generated_at'].strftime('%Y-%m-%d %H:%M:%S')}", disclaimer_style))
        story.append(Spacer(1, 15))
        
        # --- Student Information Section ---
        story.append(Paragraph("1. Student Information", h1_style))
        student_table_data = [
            [
                Paragraph("<b>Name:</b>", body_style), Paragraph(f"{student.first_name} {student.last_name}", body_style),
                Paragraph("<b>Student Code:</b>", body_style), Paragraph(student.student_code, body_style)
            ],
            [
                Paragraph("<b>Age:</b>", body_style), Paragraph(str(student.age), body_style),
                Paragraph("<b>Gender:</b>", body_style), Paragraph(student.gender, body_style)
            ],
            [
                Paragraph("<b>School:</b>", body_style), Paragraph("Gabriel Pereira (GP)" if student.school == "GP" else "Mousinho da Silveira (MS)", body_style),
                Paragraph("<b>Assessment ID:</b>", body_style), Paragraph(prediction.id[:8].upper(), body_style)
            ]
        ]
        
        student_table = Table(student_table_data, colWidths=[80, 170, 90, 160])
        student_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), neutral_light),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('PADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ]))
        story.append(student_table)
        story.append(Spacer(1, 10))
        
        # --- Predictive Model Assessment Section ---
        story.append(Paragraph("2. Predictive Model Assessment", h1_style))
        
        risk_color = accent_color if prediction.risk_level == "HIGH_RISK" else (colors.HexColor("#DD6B20") if prediction.risk_level == "MEDIUM_RISK" else colors.HexColor("#38A169"))
        risk_label_style = ParagraphStyle(
            'RiskLabel',
            parent=bold_body_style,
            textColor=risk_color,
            fontSize=11
        )
        
        pred_table_data = [
            [Paragraph("<b>Risk Classification:</b>", body_style), Paragraph(prediction.risk_level, risk_label_style)],
            [Paragraph("<b>Model Confidence:</b>", body_style), Paragraph(f"{prediction.confidence:.1%}", body_style)],
            [Paragraph("<b>Class Probabilities:</b>", body_style), Paragraph(f"LOW_RISK: {prediction.class_probabilities.get('LOW_RISK', 0.0):.1%} | MEDIUM_RISK: {prediction.class_probabilities.get('MEDIUM_RISK', 0.0):.1%} | HIGH_RISK: {prediction.class_probabilities.get('HIGH_RISK', 0.0):.1%}", body_style)],
            [Paragraph("<b>Model Version:</b>", body_style), Paragraph(prediction.model_version, body_style)],
        ]
        pred_table = Table(pred_table_data, colWidths=[150, 350])
        pred_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('LINEBELOW', (0,0), (-1,-1), 0.5, neutral_light),
        ]))
        story.append(pred_table)
        story.append(Paragraph("<i>Prediction generated by the EduPilot ANN risk classification model.</i>", disclaimer_style))
        story.append(Spacer(1, 10))
        
        # --- Explainable AI (SHAP) Section ---
        story.append(Paragraph("3. Explainable AI (SHAP) Analysis", h1_style))
        story.append(Paragraph("<b>Primary Risk Contributing Factors:</b>", h2_style))
        for factor in prediction.risk_factors:
            story.append(Paragraph(f"• {factor}", body_style))
            
        story.append(Paragraph("<b>Primary Protective Elements:</b>", h2_style))
        for factor in prediction.protective_factors:
            story.append(Paragraph(f"• {factor}", body_style))
            
        story.append(Spacer(1, 10))
        
        # --- Multimodal Evidence Section ---
        story.append(Paragraph("4. Multimodal Evidence Synthesis", h1_style))
        story.append(Paragraph("<b>AI Executive Analysis:</b>", h2_style))
        story.append(Paragraph(narrative.get("executive_summary", ""), body_style))
        story.append(Paragraph(narrative.get("evidence_synthesis", ""), body_style))
        story.append(Spacer(1, 10))
        
        # --- Intervention Plan Section ---
        story.append(Paragraph("5. AI Co-Pilot Recommendation", h1_style))
        story.append(Paragraph(f"<b>Proposed Plan: {recommendation.get('title', 'N/A')}</b> (Priority: {recommendation.get('priority', 'N/A')})", h2_style))
        story.append(Paragraph(f"<b>Plan Summary:</b> {recommendation.get('summary', 'N/A')}", body_style))
        
        story.append(Paragraph("<b>Recommended Intervention Actions:</b>", h2_style))
        for action in recommendation.get("recommended_actions", []):
            story.append(Paragraph(f"- {action}", body_style))
            
        story.append(Paragraph("<b>Monitoring and Milestones:</b>", h2_style))
        for plan in recommendation.get("monitoring_plan", []):
            story.append(Paragraph(f"- {plan}", body_style))
            
        story.append(Paragraph(f"<b>Review Period:</b> {recommendation.get('review_period_days', 14)} days", body_style))
        story.append(Spacer(1, 10))
        
        # --- Human Review Section ---
        story.append(Paragraph("6. Human Educator Review", h1_style))
        status_color = colors.HexColor("#38A169") if review["status"] == "APPROVED" else (colors.HexColor("#C53030") if review["status"] == "REJECTED" else colors.HexColor("#DD6B20"))
        status_style = ParagraphStyle(
            'ReviewStatusLabel',
            parent=bold_body_style,
            textColor=status_color
        )
        
        review_table_data = [
            [Paragraph("<b>Educator Review Status:</b>", body_style), Paragraph(review["status"], status_style)],
            [Paragraph("<b>Reviewed By:</b>", body_style), Paragraph(review["reviewed_by"], body_style)],
            [Paragraph("<b>Decision Date:</b>", body_style), Paragraph(review["reviewed_at"], body_style)],
            [Paragraph("<b>Educator Comments:</b>", body_style), Paragraph(review["educator_comment"], body_style)],
        ]
        
        if review["status"] == "REJECTED":
            review_table_data.append([Paragraph("<b>Rejection Reason:</b>", body_style), Paragraph(review["rejection_reason"], body_style)])
            
        if review["status"] == "MODIFIED":
            mod_details = review["modified_recommendation"]
            mod_summary = f"Title: {mod_details.get('title')}\nSummary: {mod_details.get('summary')}"
            review_table_data.append([Paragraph("<b>Modification Details:</b>", body_style), Paragraph(mod_summary, body_style)])
            
        review_table = Table(review_table_data, colWidths=[150, 350])
        review_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BACKGROUND', (0,0), (-1,-1), neutral_light),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ]))
        story.append(review_table)
        story.append(Spacer(1, 20))
        
        # --- Disclaimer ---
        story.append(Paragraph("<b>Disclaimer:</b>", ParagraphStyle('DiscTitle', parent=disclaimer_style, fontName='Helvetica-Bold')))
        story.append(Paragraph("EduPilot AI is a decision-support system. Predictions and AI-generated recommendations are intended to assist qualified educators and academic advisors. Final academic intervention decisions remain the responsibility of the educational institution and authorized personnel.", disclaimer_style))
        
        # Build Document
        doc.build(story)
