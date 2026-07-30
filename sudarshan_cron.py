import time
import requests
import urllib3
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- TELEGRAM CONFIGURATION ---
TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # Yahan apna Token daalein
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID_HERE"      # Yahan apni Chat ID daalein

def send_telegram_alert(message, pdf_path=None):
    """ Telegram Message and PDF Sender """
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
        requests.post(url, data=payload)

        if pdf_path:
            doc_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument"
            with open(pdf_path, 'rb') as doc:
                requests.post(doc_url, data={"chat_id": TELEGRAM_CHAT_ID}, files={"document": doc})
    except Exception as e:
        print(f"[-] Telegram Alert Error: {e}")

def passive_scan(target_url):
    if not target_url.startswith("http"):
        target_url = "https://" + target_url

    results = {"url": target_url, "vulnerabilities": [], "status": "Safe"}

    try:
        response = requests.get(target_url, timeout=10, verify=False)
        headers = response.headers

        security_headers = ["Strict-Transport-Security", "X-Frame-Options", "X-Content-Type-Options"]
        for header in security_headers:
            if header not in headers:
                results["vulnerabilities"].append({
                    "title": f"Missing Security Header: {header}",
                    "severity": "Low/Medium",
                    "description": f"Header '{header}' missing on domain.",
                    "remediation": f"Configure '{header}' in web server response headers."
                })

        if "Server" in headers:
            results["vulnerabilities"].append({
                "title": "Server Information Disclosure",
                "severity": "Low",
                "description": f"Server exposes backend software: {headers['Server']}",
                "remediation": "Hide Server banner."
            })

        if results["vulnerabilities"]:
            results["status"] = "Actionable Gap Found"

    except Exception as e:
        results["status"] = f"Scan Error: {str(e)}"

    return results

def generate_pdf(scan_data, filename="SUDARSHAN_Report.pdf"):
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = [Paragraph("PROJECT AVYAN - SUDARSHAN SCANNER REPORT", styles['Heading1']), Spacer(1, 12)]
    story.append(Paragraph(f"<b>Target:</b> {scan_data['url']}", styles['Normal']))
    story.append(Spacer(1, 10))

    for idx, vuln in enumerate(scan_data['vulnerabilities'], 1):
        story.append(Paragraph(f"<b>{idx}. {vuln['title']}</b> ({vuln['severity']})", styles['Heading3']))
        story.append(Paragraph(f"{vuln['description']}", styles['Normal']))
        story.append(Spacer(1, 8))

    doc.build(story)

def run_automated_loop():
    # Target domains list (Text file se bhi load kar sakte hain)
    targets = ["india.gov.in", "powermin.gov.in"] 
    
    print("[*] SUDARSHAN 24/7 Passive Engine Running...")
    
    for target in targets:
        scan_res = passive_scan(target)
        if scan_res["vulnerabilities"]:
            pdf_file = f"SUDARSHAN_{target.replace('.','_')}.pdf"
            generate_pdf(scan_res, pdf_file)
            
            alert_text = f"🚨 *SUDARSHAN PASSIVE ALERT*\n\nDomain: `{target}`\nGaps Found: {len(scan_res['vulnerabilities'])}\n\nReport generated and attached below."
            send_telegram_alert(alert_text, pdf_file)
            print(f"[+] Alert sent for {target}")

if __name__ == "__main__":
    run_automated_loop()
