import os
import requests
import json
from datetime import datetime

def load_targets():
    if os.path.exists("targets.txt"):
        with open("targets.txt", "r") as f:
            return [line.strip() for line in f if line.strip() and not line.startswith("#")]
    return ["https://httpbin.org/get"]

def deep_security_audit(target_url):
    findings = []
    
    # Common High-Risk Paths to Check for Exposure
    sensitive_paths = [
        "/.env",
        "/.git/HEAD",
        "/config.json",
        "/actuator/env",
        "/api/v1/debug"
    ]
    
    base_url = target_url.rsplit('/', 1)[0] if target_url.endswith('/get') else target_url
    
    # 1. Critical Endpoint Leakage Check
    for path in sensitive_paths:
        test_url = f"{base_url.rstrip('/')}{path}"
        try:
            res = requests.get(test_url, timeout=5, allow_redirects=False)
            if res.status_code == 200 and len(res.text) > 0:
                findings.append(f"🔥 **HIGH SEVERITY**: Sensitive Endpoint Exposed! `{path}` (HTTP 200)")
        except Exception:
            pass
            
    # 2. CORS Misconfiguration Check (Data Leak Risk)
    headers_cors = {'Origin': 'https://evil-attacker.com'}
    try:
        res_cors = requests.get(target_url, headers=headers_cors, timeout=5)
        allow_origin = res_cors.headers.get('Access-Control-Allow-Origin')
        allow_credentials = res_cors.headers.get('Access-Control-Allow-Credentials')
        
        if allow_origin == 'https://evil-attacker.com' or (allow_origin == '*' and allow_credentials == 'true'):
            findings.append("⚡ **MEDIUM/HIGH**: Critical CORS Misconfiguration (Arbitrary Origin Allowed)")
    except Exception:
        pass

    return findings

def send_telegram_alert(target_results):
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    
    if not token or not chat_id:
        print("[!] ERROR: Telegram Secrets missing!")
        return
        
    msg = f"🛡️ *SUDARSHAN - Advanced Threat & Bounty Scanner*\n"
    msg += f"📅 *Time:* `{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}`\n"
    msg += f"-----------------------------------\n\n"
    
    high_impact_found = False
    for res in target_results:
        msg += f"🌐 *Target:* `{res['target']}`\n"
        if res['issues']:
            high_impact_found = True
            for issue in res['issues']:
                msg += f"  {issue}\n"
        else:
            msg += "  ✅ Clean / No Critical Endpoints Exposed.\n"
        msg += "\n"
        
    if high_impact_found:
        msg += "🎯 *ACTION REQUIRED:* High-impact findings identified! Ready for validation & VDP submission."
    else:
        msg += "🔍 *Status:* No high-severity exposures found on current targets."

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": msg,
        "parse_mode": "Markdown"
    }
    requests.post(url, json=payload)

if __name__ == "__main__":
    print("[+] Executing SUDARSHAN Deep Impact Vulnerability Audit...")
    targets = load_targets()
    results = []
    
    for t in targets:
        issues = deep_security_audit(t)
        results.append({"target": t, "issues": issues})
        
    send_telegram_alert(results)
