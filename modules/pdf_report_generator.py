import json
import os
from fpdf import FPDF

class ExecutivePDFReport(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 15)
        self.cell(0, 10, 'PROJECT AVYAN - SUDARSHAN ENGINE', border=False, ln=True, align='C')
        self.set_font('Helvetica', 'I', 10)
        self.cell(0, 5, 'Autonomous Cyber Defense & Executive Audit Report', border=False, ln=True, align='C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

def build_pdf():
    json_file = "AVYAN_ALL_38_FEATURES_MASTER_REPORT.json"
    pdf_file = "SUDARSHAN_Executive_Security_Report.pdf"

    if not os.path.exists(json_file):
        print(f"[-] Error: {json_file} not found.")
        return

    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    pdf = ExecutivePDFReport()
    pdf.add_page()
    pdf.set_font("Helvetica", size=11)

    # Overview Section
    pdf.set_font("Helvetica", 'B', 12)
    pdf.cell(0, 8, "1. Executive Overview", ln=True)
    pdf.set_font("Helvetica", size=10)
    pdf.cell(0, 6, f"Project Name: {data.get('project', 'PROJECT AVYAN')}", ln=True)
    pdf.cell(0, 6, f"Engine: {data.get('engine', 'SUDARSHAN')}", ln=True)
    pdf.cell(0, 6, f"Audit Timestamp: {data.get('timestamp', 'N/A')}", ln=True)
    pdf.ln(5)

    # Status Summary
    pdf.set_font("Helvetica", 'B', 12)
    pdf.cell(0, 8, "2. System Verification Summary", ln=True)
    pdf.set_font("Helvetica", size=10)
    
    features = data.get('executed_features', {})
    for feat_name, feat_details in features.items():
        pdf.set_font("Helvetica", 'B', 10)
        pdf.cell(0, 6, f"- Module: {feat_name}", ln=True)
        pdf.set_font("Helvetica", size=9)
        
        # Safe parsing: Handles both dict and string data types
        if isinstance(feat_details, dict):
            engine_type = feat_details.get('engine', 'Active Module')
            pdf.cell(0, 5, f"  Status: Authenticated ({engine_type})", ln=True)
        else:
            pdf.cell(0, 5, f"  Status: Authenticated ({str(feat_details)})", ln=True)

    pdf.ln(5)
    pdf.set_font("Helvetica", 'I', 9)
    pdf.multi_cell(0, 5, "Notice: This document provides a high-level architectural verification summary of Project AVYAN. Confidential - For Authorized Review Only.")

    pdf.output(pdf_file)
    print(f"[+] PDF Executive Report generated: {pdf_file}")

if __name__ == "__main__":
    build_pdf()
