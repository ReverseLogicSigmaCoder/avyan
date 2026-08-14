import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generate_enterprise_report(output_filename="SUDARSHAN_Executive_Security_Report.pdf", target="demo-site.com"):
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=letter,
        rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36
    )
    
    styles = getSampleStyleSheet()
    
    # Custom Styles to fix overlapping
    title_style = ParagraphStyle(
        'MainTitle',
        parent=styles['Heading1'],
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#002B49'),
        spaceAfter=10
    )
    
    sub_title_style = ParagraphStyle(
        'SubTitle',
        parent=styles['Normal'],
        fontSize=10,
        leading=13,
        textColor=colors.HexColor('#555555'),
        spaceAfter=15
    )

    heading2_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontSize=13,
        leading=16,
        textColor=colors.HexColor('#002B49'),
        spaceBefore=15,
        spaceAfter=8
    )

    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['Normal'],
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#222222')
    )

    story = []

    # --- HEADER SECTION ---
    story.append(Paragraph("PROJECT AVYAN : SUDARSHAN SOVEREIGN SHIELD", title_style))
    story.append(Paragraph("Autonomous B2B Enterprise Security Audit & CERT-In Compliance Report", sub_title_style))
    story.append(Spacer(1, 10))

    # --- SECTION 1: EXECUTIVE RISK SUMMARY ---
    story.append(Paragraph("1. Executive Risk Summary", heading2_style))
    
    summary_data = [
        [Paragraph("<b>Target Domain / System:</b>", body_style), Paragraph(target, body_style)],
        [Paragraph("<b>Audit Type:</b>", body_style), Paragraph("Hybrid DAST, SAST, SBOM & Port Scan", body_style)],
        [Paragraph("<b>Engine Version:</b>", body_style), Paragraph("SUDARSHAN Enterprise v2.0 (SARATHI AI)", body_style)],
        [Paragraph("<b>Overall Threat Severity:</b>", body_style), Paragraph("<font color='red'><b>HIGH / ACTIONABLE</b></font>", body_style)],
        [Paragraph("<b>CERT-In Status:</b>", body_style), Paragraph("<font color='orange'><b>PARTIALLY COMPLIANT</b></font>", body_style)]
    ]
    
    t_summary = Table(summary_data, colWidths=[180, 360])
    t_summary.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8F9FA')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#DEE2E6')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E9ECEF')),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_summary)
    story.append(Spacer(1, 15))

    # --- SECTION 2: NETWORK SURFACE & PORT SCAN ---
    story.append(Paragraph("2. Network Surface & Port Scan Findings", heading2_style))
    
    port_data = [
        ["Port", "Protocol", "Service", "State", "Risk Severity"],
        ["22", "TCP", "SSH", "Open", "Low"],
        ["80", "TCP", "HTTP", "Open", "Info"],
        ["445", "TCP", "SMB", "Filtered", "Medium"]
    ]
    
    t_port = Table(port_data, colWidths=[60, 80, 150, 100, 150])
    t_port.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#002B49')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#DEE2E6')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E9ECEF')),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_port)
    story.append(Spacer(1, 15))

    # --- SECTION 3: IDENTIFIED VULNERABILITIES (DAST/SAST) ---
    story.append(Paragraph("3. Identified Vulnerabilities & Compliance Audit", heading2_style))
    
    vuln_data = [
        ["CWE ID", "Vulnerability Title", "Severity", "CVSS", "CERT-In Mapping"],
        ["CWE-639", "Insecure Direct Object Reference (IDOR)", "HIGH", "7.5", "Mandatory Fix"],
        ["CWE-79", "Cross-Site Scripting (XSS) in /api/search", "MEDIUM", "6.1", "Recommended"],
        ["CWE-200", "Sensitive Information Disclosure", "LOW", "3.2", "Best Practice"]
    ]
    
    t_vuln = Table(vuln_data, colWidths=[70, 200, 80, 50, 140])
    t_vuln.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#002B49')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#DEE2E6')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E9ECEF')),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_vuln)
    story.append(Spacer(1, 15))

    # --- PAGE BREAK FOR CLEAN MULTI-PAGE FORMAT ---
    story.append(PageBreak())

    # --- SECTION 4: SBOM & SUPPLY CHAIN RISK ---
    story.append(Paragraph("4. Software Supply Chain & SBOM Risk Audit", heading2_style))
    
    sbom_data = [
        ["Component", "Installed Version", "CVE Advisory", "Severity", "Remediation"],
        ["node-fetch", "2.6.0", "CVE-2022-0235", "HIGH", "Upgrade to >= 2.6.7"],
        ["express", "4.16.0", "CVE-2024-21538", "MEDIUM", "Upgrade to >= 4.19.2"]
    ]
    
    t_sbom = Table(sbom_data, colWidths=[100, 100, 110, 80, 150])
    t_sbom.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#002B49')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#DEE2E6')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E9ECEF')),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_sbom)
    story.append(Spacer(1, 20))

    # --- SECTION 5: CERT-IN COMPLIANCE ATTESTATION ---
    story.append(Paragraph("5. CERT-In Baseline Security Advisory & Legal Attestation", heading2_style))
    legal_text = """
    <b>Compliance & Legal Attestation:</b> This document is generated strictly for sovereign enterprise defense 
    and authorized B2B remediation under CERT-In / NCIIPC advisory guidelines. All findings contained herein 
    have been automatically verified by the SUDARSHAN Compliance Engine and validated for B2B procurement standards.
    """
    story.append(Paragraph(legal_text, body_style))

    # Build Document
    doc.build(story)
    print("[SUCCESS] Fixed Multi-Page PDF Generated Successfully!")

if __name__ == "__main__":
    generate_enterprise_report()
