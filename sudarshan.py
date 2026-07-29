import os
import requests
import json
from datetime import datetime

# Authorized Targets & Critical Sector Endpoints
TARGET_SECTORS = {
    "Telecom & Transport": "https://example.com",
    "Public Infrastructure": "https://httpbin.org/get"
}

def analyze_vulnerability(url):
    vuln_details = []
    try:
        response = requests.get(url, timeout=10)
        headers = response.headers
        
        # 1. Missing Critical Security Headers (CERT-In Baseline)
        required_headers = {
            'Content-Security-Policy': 'High',
            'Strict-Transport-Security': 'High',
            'X-Frame-Options': 'Medium',
            'X-Content-Type-Options': 'Low'
        }
        
        for header, severity in required_headers.items():
            if header not in headers:
                vuln_details.append({
                    "issue": f"Missing Security Header: {header}",
                    "severity": severity,
                    "cve_type": "CWE-693: Protection Mechanism Failure"
                })
                
        # 2. Server Banner Information Leakage
        if 'Server' in headers:
            vuln_details.append({
                "issue": f"Information Disclosure: Server Header ({headers['Server']})",
                "severity": "Low",
                "cve_type": "CWE-200: Exposure of Sensitive Information"
            })

    except Exception as e:
        vuln_details.append({"issue": f"Connection Error: {str(e)}", "severity": "Info", "cve_type": "N/A"})

    return vuln_details

def generate_certin_json_report(sector, target_url, vulnerabilities):
    report = {
        "report_id": f"AVYAN-CERTIN-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
        "timestamp_utc": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
        "reporting_engine": "AVYAN - SUDARSHAN Security Engine",
        "sector_category": sector,
        "target_url": target_url,
        "compliance_framework": "CERT-In / NCIIPC RVDP Disclosure Standard",
        "vulnerabilities_detected": vulnerabilities
    }
    return report

def send_telegram_alert(report_data):
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    
    if not token or not chat_id:
        print("[!] ERROR: Telegram Secrets missing!")
        return
        
    summary_msg = f"🛡️ *AVYAN Threat Intelligence Report*\n"
    summary_msg += f"📅 *ID:* `{report_data['report_id']}`\n"
    summary_msg += f"🏛️ *Sector:* {report_data['sector_category']}\n"
    summary_msg += f"🎯 *Target:* `{report_data['target_url']}`\n"
    summary_msg += f"-----------------------------------\n"
    
    vulns = report_data['vulnerabilities_detected']
    if vulns:
        for v in vulns:
            summary_msg += f"⚠️ *[{v['severity']}]* {v['issue']}\n"
    else:
        summary_msg += "✅ No Vulnerabilities Identified.\n"
        
    summary_msg += f"\n📄 *CERT-In JSON Payload Generated & Ready for RVDP Submission.*"

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": summary_msg,
        "parse_mode": "Markdown"
    }
    requests.post(url, json=payload)

if __name__ == "__main__":
    print("[+] Running AVYAN CERT-In Compliance Audit...")
    for sector, target in TARGET_SECTORS.items():
        vulns = analyze_vulnerability(target)
        report_json = generate_certin_json_report(sector, target, vulns)
        
        # Save JSON Report locally
        with open("certin_report.json", "w") as f:
            json.dump(report_json, f, indent=4)
            
        send_telegram_alert(report_json)
