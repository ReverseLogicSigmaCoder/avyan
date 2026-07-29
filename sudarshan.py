import os
import re
import requests
import json
from datetime import datetime

def load_targets():
    if os.path.exists("targets.txt"):
        with open("targets.txt", "r") as f:
            return [line.strip() for line in f if line.strip() and not line.startswith("#")]
    return ["https://adobe.com"]

def deep_recon_audit(target_url):
    findings = []
    try:
        res = requests.get(target_url, timeout=10)
        html_content = res.text
        
        # 1. Extract JavaScript Files for Secret Crawling
        js_files = re.findall(r'src=["\'](.*?\.js)["\']', html_content)
        if js_files:
            findings.append(f"📦 Found `{len(js_files)}` JS Bundle Files for Secret Analysis.")
            
        # 2. Check for Leaked Cloud Credentials & Sensitive Patterns in HTML/JS
        patterns = {
            "AWS Access Key": r'AKIA[0-9A-Z]{16}',
            "Generic API Key": r'api[_-]?key["\']?\s*[:=]\s*["\']([a-zA-Z0-9_\-]{20,})["\']',
            "Internal JWT Token": r'eyJ[a-zA-Z0-9_-]{10,}\.eyJ[a-zA-Z0-9_-]{10,}'
        }
        
        for key_name, pattern in patterns.items():
            matches = re.findall(pattern, html_content)
            if matches:
                findings.append(f"🔥 **CRITICAL LEAK**: {key_name} Identified in Page Source!")

        # 3. CORS Misconfig Check
        res_cors = requests.get(target_url, headers={'Origin': 'https://evil.com'}, timeout=5)
        if res_cors.headers.get('Access-Control-Allow-Origin') == 'https://evil.com':
            findings.append("⚡ **HIGH SEVERITY**: CORS Wildcard/Arbitrary Origin Misconfiguration!")

    except Exception as e:
        findings.append(f"⚠️ Scan Warning: {str(e)}")
        
    return findings

def send_telegram_alert(target_results):
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    
    if not token or not chat_id:
        print("[!] ERROR: Telegram Secrets missing!")
        return
        
    msg = f"🛡️ *SUDARSHAN - Deep Critical Recon Engine*\n"
    msg += f"📅 *Time:* `{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}`\n"
    msg += f"-----------------------------------\n\n"
    
    for res in target_results:
        msg += f"🌐 *Target:* `{res['target']}`\n"
        if res['issues']:
            for issue in res['issues']:
                msg += f"  • {issue}\n"
        else:
            msg += "  ✅ Clean / No Secrets or Critical Flaws Exposed.\n"
        msg += "\n"

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

if __name__ == "__main__":
    print("[+] Executing SUDARSHAN Critical Recon & Secret Analyzer...")
    targets = load_targets()
    results = []
    for t in targets:
        issues = deep_recon_audit(t)
        results.append({"target": t, "issues": issues})
    send_telegram_alert(results)
