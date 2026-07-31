import json
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generate_pdf_report(json_file):
    if not os.path.exists(json_file):
        print(f"[-] File not found: {json_file}")
        return

    with open(json_file, 'r') as f:
        data = json.load(f)

    pdf_filename = f"CERT_In_Master_Audit_Report_{data['target'].replace('.', '_')}.pdf"
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle('TStyle', parent=styles['Heading1'], fontSize=16, textColor=colors.HexColor('#003366'), spaceAfter=10)
    h2_style = ParagraphStyle('H2Style', parent=styles['Heading2'], fontSize=11, textColor=colors.HexColor('#111111'), spaceAfter=6)

    # Document Header
    story.append(Paragraph("PROJECT AVYAN | SCANNING ENGINE: SUDARSHAN MASTER", title_style))
    story.append(Paragraph("<b>CERT-In & NCIIPC Compliance Audit Report (DAST + SBOM)</b>", h2_style))
    story.append(Spacer(1, 10))

    # Meta Table
    meta = [
        ["Target Domain / IP:", data.get("target", "N/A")],
        ["Audit Engine:", data.get("engine", "SUDARSHAN MASTER v2.0")],
        ["Compliance Standard:", data.get("compliance_framework", "CERT-In Guidelines")],
        ["Timestamp:", data.get("timestamp", "N/A")]
    ]
    t = Table(meta, colWidths=[140, 310])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F2F4F7')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#D0D5DD')),
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t)
    story.append(Spacer(1, 14))

    # Section 1: Surface
    story.append(Paragraph("<b>1. Network Surface Assessment</b>", h2_style))
    raw_scan = data.get("findings", {}).get("surface_ports", "N/A")
    story.append(Paragraph(raw_scan.replace('\n', '<br/>'), styles['Code']))
    story.append(Spacer(1, 12))

    # Section 2: DAST
    story.append(Paragraph("<b>2. Dynamic Application Security Testing (DAST / Nuclei)</b>", h2_style))
    dast_items = data.get("findings", {}).get("dast_vulnerabilities", [])
    if dast_items:
        for vuln in dast_items:
            v_text = f"• <b>[{vuln.get('severity', 'HIGH').upper()}]</b> {vuln.get('template_id', 'Vulnerability')} - {vuln.get('info', {}).get('name', 'Details logged')}"
            story.append(Paragraph(v_text, styles['Normal']))
    else:
        story.append(Paragraph("No critical DAST vulnerabilities detected.", styles['Normal']))
    story.append(Spacer(1, 12))

    # Section 3: SBOM
    story.append(Paragraph("<b>3. Software Supply Chain & SBOM Audit (Trivy/CycloneDX)</b>", h2_style))
    sbom = data.get("findings", {}).get("sbom_audit", {})
    sbom_text = f"Format: {sbom.get('format')} | Components Scanned: {sbom.get('components_scanned')}"
    story.append(Paragraph(sbom_text, styles['Normal']))
    
    for vul in sbom.get("vulnerabilities", []):
        s_text = f"• <b>[{vul.get('severity')}]</b> {vul.get('cve_id')} in {vul.get('package')} (Fix: {vul.get('fix_version')})"
        story.append(Paragraph(s_text, styles['Normal']))

    doc.build(story)
    print(f"\n[SUCCESS] Master PDF Generated: {pdf_filename}")

if __name__ == "__main__":
    generate_pdf_report("sudarshan_master_audit_scanme_nmap_org.json")
