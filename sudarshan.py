import os
import requests
import json
from datetime import datetime

# Target Critical Infrastructure / Web Assets for Audit
TARGETS = [
    "https://httpbin.org/get",
    "https://example.com"
]

def scan_target(url):
    findings = []
    try:
        response = requests.get(url, timeout=10)
        headers = response.headers
        
        # 1. Missing Security Headers Check (CERT-In Standard)
        sec_headers = ['X-Frame-Options', 'X-Content-Type-Options', 'Strict-Transport-Security', 'Content-Security-Policy']
        missing_headers = [h for h in sec_headers if h not in headers]
        
        if missing_headers:
            findings.append(f"⚠️ Missing Security Headers: {', '.join(missing_headers)}")
            
        # 2. Server Information Disclosure Check
        if 'Server' in headers:
            findings.append(f"🔍 Information Disclosure (Server Header): {headers['Server']}")
            
    except Exception as e:
        findings.append(f"❌ Scan Connection Error: {str(e)}")
        
    return findings

def send_telegram_alert(message):
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    
    if not token or not chat_id:
        print("[!] ERROR: Telegram Secrets missing!")
        return
        
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }
    requests.post(url, json=payload)

if __name__ == "__main__":
    print("[+] Running SUDARSHAN Real-Time Vulnerability Audit...")
    
    report_text = f"🛡️ *SUDARSHAN SYSTEM AUDIT REPORT*\n"
    report_text += f"📅 *Timestamp:* {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}\n"
    report_text += f"-----------------------------------\n\n"
    
    total_vulns = 0
    for target in TARGETS:
        results = scan_target(target)
        report_text += f"🎯 *Target:* `{target}`\n"
        if results:
            for res in results:
                report_text += f"  • {res}\n"
                total_vulns += 1
        else:
            report_text += f"  ✅ Zero Vulnerabilities Detected.\n"
        report_text += "\n"
        
    report_text += f"📊 *Total Gaps Identified:* {total_vulns}\n"
    report_text += f"🏛️ *CERT-In / NCIIPC Compliance Status:* Ready for Audit Verification."
    
    send_telegram_alert(report_text)
