import os
import re
import json
import logging
import urllib.request
import urllib.error
from datetime import datetime, timezone

logging.basicConfig(
    filename="sudarshan_audit_trail.log",
    level=logging.INFO,
    format="%(asctime)s UTC - [AUDIT] - %(message)s"
)

def log_audit_event(event_type: str, details: str):
    timestamp = datetime.now(timezone.utc).isoformat()
    log_message = f"[{event_type.upper()}] {details}"
    logging.info(log_message)
    print(f"[{timestamp}] {log_message}")

# ---------------------------------------------------------
# PASSIVE HEADER AUDIT ENGINE
# ---------------------------------------------------------
RECOMMENDED_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options"
]

def analyze_target(domain: str) -> dict:
    url = f"https://{domain}"
    log_audit_event("PASSIVE_SCAN_START", f"Auditing {url}")
    missing_headers = []
    
    try:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req, timeout=10, timeout=10, timeout=10) as response:
            resp_headers = response.info()
            for sec_h in RECOMMENDED_HEADERS:
                if sec_h.lower() not in [h.lower() for h in resp_headers.keys()]:
                    missing_headers.append(sec_h)
            return {"status": "SUCCESS", "domain": domain, "missing": missing_headers}
    except Exception as e:
        log_audit_event("SCAN_ERROR", f"Failed for {domain}: {str(e)}")
        return {"status": "ERROR", "domain": domain, "reason": str(e)}

# ---------------------------------------------------------
# TELEGRAM NOTIFIER
# ---------------------------------------------------------
def send_telegram_report(summary_text: str):
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    
    if not bot_token or not chat_id:
        print("[!] Telegram credentials missing in GitHub Secrets.")
        return

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = json.dumps({
        "chat_id": chat_id,
        "text": summary_text,
        "parse_mode": "Markdown"
    }).encode("utf-8")

    try:
        req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=10, timeout=10, timeout=10) as resp:
            print("[+] Consolidated Telegram report sent successfully!")
    except Exception as e:
        print(f"[-] Telegram dispatch error: {str(e)}")

# ---------------------------------------------------------
# MAIN MULTI-TARGET EXECUTION
# ---------------------------------------------------------
if __name__ == "__main__":
    # Central Target Scope List inside AVYAN Repo
    TARGET_SCOPE = [
        "digitalindia.gov.in",
        "mygov.in",
        "ncs.gov.in",
        "mca.gov.in"
    ]
    
    results_summary = []
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    
    for target in TARGET_SCOPE:
        res = analyze_target(target)
        if res["status"] == "SUCCESS":
            if res["missing"]:
                results_summary.append(f"⚠️ `{target}`: Missing Headers -> {', '.join(res['missing'])}")
            else:
                results_summary.append(f"✅ `{target}`: Fully Compliant")
        else:
            results_summary.append(f"❌ `{target}`: Unreachable ({res['reason']})")
            
    report_msg = f"🛡️ *SUDARSHAN SOVEREIGN SHIELD REPORT*\n⏱️ *Time:* `{timestamp}`\n\n" + "\n".join(results_summary)
    send_telegram_report(report_msg)
