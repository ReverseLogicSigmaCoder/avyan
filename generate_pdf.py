import json
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generate_pdf_report(json_file):
    if not os.path.exists(json_file):
        print(f"[-] Error: File {json_file} not found!")
        return

    with open(json_file, 'r') as f:
        data = json.load(f)

    pdf_filename = f"CERT_In_Audit_Report_{data['target'].replace('.', '_')}.pdf"
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
    story = []

    styles = getSampleStyleSheet()
    
    # Custom Styles
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#003366'),
        spaceAfter=12
    )
    
    header_style = ParagraphStyle(
        'HeaderStyle',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=colors.HexColor('#222222'),
        spaceAfter=6
    )

    # Document Header
    story.append(Paragraph("PROJECT AVYAN | SCANNING ENGINE: SUDARSHAN", title_style))
    story.append(Paragraph("<b>CERT-In Baseline Compliance & Security Audit Report</b>", header_style))
    story.append(Spacer(1, 12))

    # Meta Table
    meta_data = [
        ["Target Domain / IP:", data.get("target", "N/A")],
        ["Audit Engine:", data.get("engine", "SUDARSHAN v1.0")],
        ["Framework:", data.get("compliance_framework", "CERT-In Guidelines")],
        ["Timestamp:", data.get("timestamp", "N/A")]
    ]
    
    t = Table(meta_data, colWidths=[150, 300])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F2F4F7')),
        ('TEXTCOLOR', (0,0), (-1,-1), colors.black),
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#D0D5DD')),
    ]))
    story.append(t)
    story.append(Spacer(1, 18))

    # Findings Section
    story.append(Paragraph("<b>1. Network Surface & Port Scan Findings</b>", header_style))
    
    raw_scan = data.get("findings", {}).get("surface_ports", "No scan data available.")
    
    # Clean text formatting for report
    scan_p = Paragraph(raw_scan.replace('\n', '<br/>'), styles['Code'])
    story.append(scan_p)

    doc.build(story)
    print(f"\n[SUCCESS] PDF Report Generated: {pdf_filename}")

if __name__ == "__main__":
    json_path = "sudarshan_audit_scanme_nmap_org.json"
    generate_pdf_report(json_path)
