import os
import requests
import json
import sqlite3
import datetime

# ----------------- CONFIGURATION -----------------
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8627150645:AAFs3xoo0z2odb7cZgw2Em80s8H2gOb-oKE")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "7459821254")

# Standard test domain for reliable verification
TARGET_DOMAIN = "example.com"
TARGET_EMAIL = "ravindrachoudhary9653@gmail.com"
DB_FILE = "sudarshan_audit.db"

# Custom User-Agent to avoid standard script blocks
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}

# ----------------- DATABASE PERSISTENCE -----------------
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scan_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            target_identity TEXT NOT NULL,
            monitored_domain TEXT NOT NULL,
            subdomain_count INTEGER NOT NULL,
            ioc_status TEXT NOT NULL,
            raw_summary TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def log_to_db(timestamp, identity, domain, sub_count, ioc_status, summary):
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO scan_logs (timestamp, target_identity, monitored_domain, subdomain_count, ioc_status, raw_summary)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (timestamp, identity, domain, sub_count, ioc_status, summary))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[-] DB Error: {e}")

# ----------------- AUDIT ENGINE -----------------
def audit_target_headers(domain):
    print(f"[+] Performing Non-Intrusive Security Header Audit for: {domain}")
    missing_headers = []
    
    # Prefix www if standard apex fails
    url = f"https://{domain}" if domain.startswith("www.") else f"https://www.{domain}"
    
    try:
        res = requests.get(url, headers=HEADERS, timeout=10, allow_redirects=True)
        headers = res.headers
        
        security_headers = [
            "Strict-Transport-Security",
            "Content-Security-Policy",
            "X-Frame-Options",
            "X-Content-Type-Options"
        ]
        
        for h in security_headers:
            if h not in headers:
                missing_headers.append(h)
                
        print(f"[+] HTTP Request Successful! Status Code: {res.status_code}")
    except Exception as e:
        print(f"[-] Header Audit Notice: {e}")
        
    return missing_headers

def fetch_passive_subdomains(domain):
    print(f"[+] Fetching Certificate Transparency Logs for: {domain}")
    url = f"https://crt.sh/?q=%.{domain}&output=json"
    subdomains = set()
    try:
        res = requests.get(url, headers=HEADERS, timeout=15)
        if res.status_code == 200:
            data = res.json()
            for entry in data[:10]:
                name = entry.get('name_value')
                if name:
                    subdomains.add(name.split('\n')[0])
    except Exception as e:
        print(f"[-] CT Log Notice: {e}")
    return list(subdomains)

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        requests.post(url, data=payload, timeout=10)
    except Exception as e:
        print(f"[-] Telegram Notice: {e}")

def run_soar_pipeline():
    print("==========================================================")
    print("    PROJECT AVYAN - SUDARSHAN CERT-In CVD AUDIT ENGINE    ")
    print("==========================================================")
    
    init_db()
    
    subs = fetch_passive_subdomains(TARGET_DOMAIN)
    missing_hdrs = audit_target_headers(TARGET_DOMAIN)
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    
    ioc_status = "CVD Hardening Flagged" if missing_hdrs else "Clean"
    summary = f"Subdomains: {len(subs)}, Missing Headers: {len(missing_hdrs)}"
    
    log_to_db(timestamp, TARGET_EMAIL, TARGET_DOMAIN, len(subs), ioc_status, summary)
    
    report = f"⚡ *SUDARSHAN CERT-In CVD AUDIT REPORT* ⚡\n\n"
    report += f"🕒 *Timestamp:* `{timestamp}`\n"
    report += f"🎯 *Target Domain:* `{TARGET_DOMAIN}`\n\n"
    report += f"🌐 *Passive Subdomains Found:* `{len(subs)}`\n"
    
    report += "\n🛡️ *MISSING SECURITY HEADERS:*\n"
    if missing_hdrs:
        for mh in missing_hdrs:
            report += f"⚠️ `Missing Header:` {mh}\n"
    else:
        report += "✅ All core security headers present.\n"
        
    report += "\n-----------------------------------------\n"
    report += "📋 *Status:* Ready for CVD Audit Log Export."
    
    send_telegram_alert(report)
    print("[+] Pipeline Execution Completed Successfully!")

if __name__ == "__main__":
    run_soar_pipeline()

import sqlite3
import json
import datetime

DB_FILE = "sudarshan_audit.db"

def generate_certin_report():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM scan_logs ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()

    if not row:
        print("[-] No records found in sudarshan_audit.db")
        return

    report = {
        "report_metadata": {
            "organization_target": row[3],
            "timestamp_utc": row[1],
            "reporter_contact": row[2],
            "standard": "CERT-In Coordinated Vulnerability Disclosure (CVD)"
        },
        "finding_details": {
            "title": "HTTP Security Posture & Header Configuration Audit",
            "monitored_domain": row[3],
            "discovered_subdomains_count": row[4],
            "status": row[5],
            "summary": row[6]
        },
        "remediation_guidelines": [
            "Implement Strict-Transport-Security (HSTS) header.",
            "Define strict Content-Security-Policy (CSP).",
            "Set X-Frame-Options to DENY or SAMEORIGIN."
        ]
    }

    # Export to structured JSON
    filename = f"certin_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, "w") as f:
        json.dump(report, f, indent=4)

    print(f"[+] CERT-In Compliant Report generated: {filename}")

if __name__ == "__main__":
    generate_certin_report()

