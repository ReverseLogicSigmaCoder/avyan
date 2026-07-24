import os
import re
import json
import logging
import urllib.request
import urllib.error
from datetime import datetime, timezone

# ---------------------------------------------------------
# 1. AUDIT TRAIL & LOGGING
# ---------------------------------------------------------
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


def validate_scope(target_domain: str, authorized_scope: list) -> bool:
    if target_domain in authorized_scope:
        log_audit_event("SCOPE_VALIDATION", f"Target '{target_domain}' is AUTHORIZED.")
        return True
    else:
        log_audit_event("SCOPE_VIOLATION", f"Target '{target_domain}' BLOCKED.")
        return False


# ---------------------------------------------------------
# 2. REAL LIVE PASSIVE HEADER ANALYZER
# ---------------------------------------------------------
RECOMMENDED_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options"
]

def analyze_live_passive_headers(target_domain: str) -> dict:
    url = f"https://{target_domain}"
    log_audit_event("PASSIVE_SCAN_START", f"Fetching public headers for {url}")
    
    missing_headers = []
    headers_received = {}
    
    try:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            response_headers = response.info()
            for header_name in response_headers.keys():
                headers_received[header_name] = response_headers[header_name]

            for sec_header in RECOMMENDED_HEADERS:
                if sec_header.lower() not in [h.lower() for h in response_headers.keys()]:
                    missing_headers.append(sec_header)
                    
    except Exception as e:
        log_audit_event("PASSIVE_SCAN_ERROR", f"Error for {target_domain}: {str(e)}")
        return {"status": "ERROR", "reason": str(e)}

    return {
        "status": "SUCCESS",
        "domain": target_domain,
        "missing_headers": missing_headers,
        "raw_headers": headers_received
    }


# ---------------------------------------------------------
# 3. TELEGRAM ALERT DISPATCHER
# ---------------------------------------------------------
def send_telegram_alert(message_text: str):
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    
    if not bot_token or not chat_id:
        print("[!] Telegram credentials missing in Environment/Secrets. Skipping dispatch.")
        return

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = json.dumps({
        "chat_id": chat_id,
        "text": message_text,
        "parse_mode": "Markdown"
    }).encode("utf-8")

    try:
        req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            print("[+] Telegram Daily Audit Report Dispatched Successfully!")
    except Exception as e:
        print(f"[-] Telegram dispatch failed: {str(e)}")


# ---------------------------------------------------------
# 4. ADVISORY FORMATTER & EXPORTER
# ---------------------------------------------------------
def generate_certin_advisory(target: str, scan_result: dict) -> dict:
    if scan_result.get("status") != "SUCCESS":
        return {"error": "Scan failed"}

    missing = scan_result.get("missing_headers", [])
    
    if len(missing) > 0:
        cvss_score = 5.3
        severity = "MEDIUM"
        findings_summary = f"Missing Headers detected: {', '.join(missing)}"
    else:
        cvss_score = 0.0
        severity = "INFORMATIONAL"
        findings_summary = "All recommended HTTP security headers are present."

    advisory = {
        "generator": "SUDARSHAN Sovereign Shield",
        "timestamp_utc": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
        "target": target,
        "severity": severity,
        "cvss_score": cvss_score,
        "findings": findings_summary
    }
    
    # Format Telegram Message
    tg_message = f"""🛡️ *SUDARSHAN DAILY COMPLIANCE REPORT*
📌 *Target:* `{target}`
⏱️ *Time:* `{advisory['timestamp_utc']}`
📊 *Severity:* `{severity}` (CVSS: {cvss_score})
📝 *Findings:* {findings_summary}
"""
    send_telegram_alert(tg_message)
    return advisory


if __name__ == "__main__":
    ALLOWED_SCOPE = ["digitalindia.gov.in", "mygov.in", "ncs.gov.in", "mca.gov.in"]
    target_domain = "digitalindia.gov.in"
    
    if validate_scope(target_domain, ALLOWED_SCOPE):
        scan_result = analyze_live_passive_headers(target_domain)
        if scan_result.get("status") == "SUCCESS":
            generate_certin_advisory(target_domain, scan_result)
