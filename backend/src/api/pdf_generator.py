import os
import re
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def generate_pdf_report(assessment_dict, output_pdf_path):
    """
    Generates a beautifully styled inspection and risk PDF report.
    """
    # Create directory if needed
    os.makedirs(os.path.dirname(output_pdf_path), exist_ok=True)
    
    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )
    
    styles = getSampleStyleSheet()
    
    # Custom Styles for Premium Look
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor('#1A365D'),
        spaceAfter=6
    )
    
    section_style = ParagraphStyle(
        'SectionHeader',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor('#2B6CB0'),
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#2D3748')
    )
    
    body_bold = ParagraphStyle(
        'BodyBold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )
    
    bullet_style = ParagraphStyle(
        'BulletStyle',
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )
    
    story = []
    
    # Header Banner / Logo Placeholder
    story.append(Paragraph("OMNIRISK AI &mdash; MULTIMODAL ASSESSMENT REPORT", ParagraphStyle('SubBanner', fontName='Helvetica-Bold', fontSize=8, leading=10, textColor=colors.HexColor('#718096'))))
    story.append(Spacer(1, 4))
    
    # Title
    story.append(Paragraph(f"Asset Analysis: {assessment_dict['asset_name']}", title_style))
    
    # Metadata Table
    status_text = "APPROVED & REVIEWED" if assessment_dict['is_reviewed'] else "PENDING REVIEW"
    status_color = "#38A169" if assessment_dict['is_reviewed'] else "#E53E3E"
    
    meta_data = [
        [
            Paragraph("<b>Asset ID:</b>", body_style), Paragraph(str(assessment_dict['id']), body_style),
            Paragraph("<b>Assessment Date:</b>", body_style), Paragraph(assessment_dict['created_at'][:10] if assessment_dict['created_at'] else "N/A", body_style)
        ],
        [
            Paragraph("<b>Location:</b>", body_style), Paragraph(assessment_dict['location'], body_style),
            Paragraph("<b>Status:</b>", body_style), Paragraph(f"<font color='{status_color}'><b>{status_text}</b></font>", body_style)
        ]
    ]
    
    meta_table = Table(meta_data, colWidths=[1.2*inch, 2.2*inch, 1.4*inch, 2.2*inch])
    meta_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('LINEBELOW', (0,-1), (-1,-1), 1, colors.HexColor('#E2E8F0')),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 12))
    
    # Section: Executive Summary
    story.append(Paragraph("1. Executive Summary", section_style))
    summary_text = assessment_dict.get('llm_summary') or "No summary available."
    story.append(Paragraph(summary_text, body_style))
    story.append(Spacer(1, 10))
    
    # Section: Diagnostics & Predictions
    story.append(Paragraph("2. Diagnostic Predictions", section_style))
    
    # Map classes
    lstm_map = {0: "Low Risk", 1: "Medium Risk", 2: "High Risk"}
    cnn_map = {0: "Healthy (No visible cracks)", 1: "Damaged (Cracks/Scratches)"}
    ann_map = {0: "Normal Noise", 1: "Anomalous Sound"}
    
    lstm_pred = lstm_map.get(assessment_dict['lstm_prediction_class'], "N/A")
    cnn_pred = cnn_map.get(assessment_dict['cnn_prediction_class'], "N/A")
    ann_pred = ann_map.get(assessment_dict['ann_prediction_class'], "N/A")
    
    # Human adjustments
    final_lstm = lstm_map.get(assessment_dict['override_lstm_class'], lstm_pred) if assessment_dict['override_lstm_class'] is not None else lstm_pred
    final_cnn = cnn_map.get(assessment_dict['override_cnn_class'], cnn_pred) if assessment_dict['override_cnn_class'] is not None else cnn_pred
    final_ann = ann_map.get(assessment_dict['override_ann_class'], ann_pred) if assessment_dict['override_ann_class'] is not None else ann_pred
    
    diag_data = [
        [Paragraph("<b>Diagnostic Module</b>", body_bold), Paragraph("<b>Initial AI Prediction</b>", body_bold), Paragraph("<b>Final Adjusted Status</b>", body_bold)],
        [Paragraph("Tabular Time-Series (LSTM)", body_style), Paragraph(lstm_pred, body_style), Paragraph(final_lstm, body_bold)],
        [Paragraph("Visual Damage (CNN)", body_style), Paragraph(cnn_pred, body_style), Paragraph(final_cnn, body_bold)],
        [Paragraph("Sound Analysis (ANN)", body_style), Paragraph(ann_pred, body_style), Paragraph(final_ann, body_bold)]
    ]
    
    diag_table = Table(diag_data, colWidths=[2.3*inch, 2.35*inch, 2.35*inch])
    diag_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F7FAFC')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E0')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(diag_table)
    story.append(Spacer(1, 10))
    
    # Section: Explainable AI (XAI)
    story.append(Paragraph("3. Explainable AI (XAI) Insights", section_style))
    
    # Feature Importance description
    imp_dict = assessment_dict.get('lstm_feature_importance') or {}
    imp_lines = []
    for k, v in imp_dict.items():
        imp_lines.append(f"<b>{k.capitalize()}:</b> {v*100:.1f}% impact")
    imp_text = " &bull; ".join(imp_lines) if imp_lines else "No feature importance data."
    story.append(Paragraph(f"<b>Time-Series Perturbation Saliency:</b> {imp_text}", body_style))
    story.append(Spacer(1, 8))
    
    # Image side-by-side or stacked
    # Load original image and Grad-CAM image side-by-side if they exist
    orig_img_path = assessment_dict.get('image_path')
    gradcam_path = assessment_dict.get('cnn_gradcam_path')
    
    img_elements = []
    if orig_img_path and os.path.exists(orig_img_path):
        try:
            img_elements.append(Image(orig_img_path, width=2.2*inch, height=2.2*inch))
        except Exception as e:
            print(f"Error loading original image into PDF: {e}")
            
    if gradcam_path and os.path.exists(gradcam_path):
        try:
            img_elements.append(Image(gradcam_path, width=2.2*inch, height=2.2*inch))
        except Exception as e:
            print(f"Error loading Grad-CAM image into PDF: {e}")
            
    if img_elements:
        # Wrap in Table
        table_cells = []
        if len(img_elements) == 2:
            table_cells = [[img_elements[0], img_elements[1]],
                           [Paragraph("<font color='#718096'>Original Image</font>", body_style), Paragraph("<font color='#718096'>Visual Grad-CAM Saliency Highlight</font>", body_style)]]
            img_table = Table(table_cells, colWidths=[3.5*inch, 3.5*inch])
        else:
            table_cells = [[img_elements[0]], [Paragraph("<font color='#718096'>Inspection Image</font>", body_style)]]
            img_table = Table(table_cells, colWidths=[7*inch])
            
        img_table.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ]))
        story.append(KeepTogether([img_table]))
    else:
        story.append(Paragraph("<i>No inspection images uploaded for Grad-CAM display.</i>", body_style))
        
    story.append(Spacer(1, 10))
    
    # Section: LLM Technical Reasoning & Mitigations
    reasoning_section = []
    reasoning_section.append(Paragraph("4. Technical Risk Reasoning", section_style))
    reasoning_text = assessment_dict.get('llm_reasoning') or "No technical reasoning summary available."
    reasoning_section.append(Paragraph(reasoning_text, body_style))
    reasoning_section.append(Spacer(1, 10))
    story.append(KeepTogether(reasoning_section))
    
    mitigation_section = []
    mitigation_section.append(Paragraph("5. Recommended Mitigation & Compliance Steps", section_style))
    mitigation_text = assessment_dict.get('llm_mitigation') or "No mitigation steps generated."
    
    # Split bullet points if it contains newlines/numbers
    lines = [l.strip() for l in mitigation_text.split('\n') if l.strip()]
    for line in lines:
        # Format bullet point
        clean_line = re.sub(r'^(\d+[\.\)]|-|\*)\s*', '', line)
        mitigation_section.append(Paragraph(f"&bull; {clean_line}", bullet_style))
        
    mitigation_section.append(Spacer(1, 10))
    story.append(KeepTogether(mitigation_section))
    
    # Section: Human in the Loop (HITL) Sign-off
    hitl_section = []
    hitl_section.append(Paragraph("6. Human-in-the-Loop Analyst Verification", section_style))
    notes_text = assessment_dict.get('analyst_notes') or "No human analyst notes provided."
    reviewer_name = assessment_dict.get('reviewed_by') or "N/A"
    review_date = assessment_dict.get('reviewed_at')[:10] if assessment_dict.get('reviewed_at') else "N/A"
    
    hitl_section.append(Paragraph(f"<b>Analyst Remarks:</b> {notes_text}", body_style))
    hitl_section.append(Spacer(1, 6))
    
    sign_data = [
        [Paragraph(f"<b>Reviewed By:</b> {reviewer_name}", body_style), Paragraph(f"<b>Review Date:</b> {review_date}", body_style)]
    ]
    sign_table = Table(sign_data, colWidths=[3.5*inch, 3.5*inch])
    sign_table.setStyle(TableStyle([
        ('LINEABOVE', (0,0), (-1,0), 0.5, colors.HexColor('#CBD5E0')),
        ('TOPPADDING', (0,0), (-1,-1), 8),
    ]))
    hitl_section.append(sign_table)
    story.append(KeepTogether(hitl_section))
    
    # Build Document
    doc.build(story)
    return output_pdf_path
