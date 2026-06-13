import io
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch
from typing import Dict, Any, List

def generate_pdf_report(kpis: Dict[str, Any], insights: List[str], recommendations: List[Dict[str, str]], notes: Dict[str, str], quality_report: Dict[str, Any]) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(name='Title', fontSize=24, textColor=colors.HexColor('#0F172A'), spaceAfter=20, fontName='Helvetica-Bold')
    heading_style = ParagraphStyle(name='Heading', fontSize=16, textColor=colors.HexColor('#0F172A'), spaceAfter=10, spaceBefore=20, fontName='Helvetica-Bold')
    normal_style = ParagraphStyle(name='Normal', fontSize=11, textColor=colors.HexColor('#334155'), spaceAfter=10, fontName='Helvetica')
    
    elements = [
        Paragraph("Executive Sales KPI Intelligence Report", title_style),
        Spacer(1, 0.2*inch),
        Paragraph("1. Executive Summary", heading_style),
        Paragraph(f"Total Revenue: ${kpis['Total_Revenue']:,.2f} | Total Orders: {kpis['Total_Orders']:,} | MoM Growth: {kpis['MoM_Growth']:+.1f}%", normal_style),
        Spacer(1, 0.2*inch),
        Paragraph("2. Data Quality Score", heading_style),
        Paragraph(f"Overall Score: {quality_report['quality_score']}/100 ({quality_report['rating']}). {quality_report['commentary'][0]}", normal_style),
        Spacer(1, 0.2*inch),
        Paragraph("3. Key Business Insights", heading_style)
    ]
    for insight in insights:
        elements.append(Paragraph(f"• {insight}", normal_style))
        
    elements.extend([Spacer(1, 0.2*inch), Paragraph("4. Executive Recommendations", heading_style)])
    for rec in recommendations:
        elements.append(Paragraph(f"<b>{rec['category']}:</b> {rec['action']}", normal_style))
        
    elements.extend([Spacer(1, 0.2*inch), Paragraph("5. Analyst Notes", heading_style)])
    elements.append(Paragraph(f"<b>Key Findings:</b> {notes['key_findings']}", normal_style))
    elements.append(Paragraph(f"<b>Risks:</b> {notes['risks']}", normal_style))
    elements.append(Paragraph(f"<b>Opportunities:</b> {notes['opportunities']}", normal_style))
    elements.append(Paragraph(f"<b>Actions:</b> {notes['recommended_actions']}", normal_style))

    doc.build(elements)
    return buffer.getvalue()