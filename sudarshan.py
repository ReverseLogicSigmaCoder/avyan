import os
import re
import requests
import json
from datetime import datetime

def load_targets():
    if os.path.exists("targets.txt"):
        with open("targets.txt", "r") as f:
            return [line.strip() for line in f if line.strip() and not line.startswith("#")]
    return ["https://creativecloud.adobe.com"]

def deep_recon_audit(target_url):
    findings = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    try:
        res = requests.get(target_url, headers=headers, timeout=10, allow_redirects=True)
        html_content = res.text
        
        # 1. JS Bundle Detection
        js_files = re.findall(r'src=["\'](.*?\.js)["\']', html_content)
        if js_files:
            findings.append(f"📦 Identified `{len(js_files)}` JS Bundles for analysis.")
            
        # 2. Key Leaks Check
        if "AKIA" in html_content:
            findings.append("🔥 **CRITICAL**: AWS Access Key Pattern Detected!")

    except Exception as e:
        findings.append(f"⚠️ Target Unreachable: {str(e)[:30]}")
        
    return findings

def send_telegram_alert(target_results):
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    
    if not token or not chat_id:
        print("[!] ERROR: Telegram Secrets missing!")
        return
        
    msg = f"🛡️ *SUDARSHAN - Deep Subdomain Recon Engine*\n"
    msg += f"📅 *Time:* `{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}`\n"
    msg += f"-----------------------------------\n\n"
    
    for res in target_results:
        msg += f"🌐 *Target:* `{res['target']}`\n"
        if res['issues']:
            for issue in res['issues']:
                msg += f"  • {issue}\n"
        else:
            msg += "  ✅ Clean / No Exposed Leaks Identified.\n"
        msg += "\n"

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

if __name__ == "__main__":
    print("[+] Running SUDARSHAN Subdomain Recon...")
    targets = load_targets()
    results = []
    for t in targets:
        issues = deep_recon_audit(t)
        results.append({"target": t, "issues": issues})
    send_telegram_alert(results)
