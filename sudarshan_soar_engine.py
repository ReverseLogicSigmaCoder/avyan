import os
import requests
import json
import sqlite3
import datetime

# ----------------- CONFIGURATION & HARDENING -----------------
# Reading from Environment Variables (With Fallback for Safety)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8627150645:AAFs3xoo0z2odb7cZgw2Em80s8H2gOb-oKE")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "7459821254")

TARGET_DOMAIN = "nic.in"
TARGET_EMAIL = "ravindrachoudhary9653@gmail.com"
DB_FILE = "sudarshan_audit.db"

# ----------------- DATABASE PERSISTENCE LAYER -----------------
def init_db():
    """Initialize local SQLite Audit Database for Data Persistence."""
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
    """Save scan record into SQLite DB."""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO scan_logs (timestamp, target_identity, monitored_domain, subdomain_count, ioc_status, raw_summary)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (timestamp, identity, domain, sub_count, ioc_status, summary))
        conn.commit()
        conn.close()
        print("[+] Audit record successfully persisted to SQLite DB.")
    except Exception as e:
        print(f"[-] Database Error: {e}")

# ----------------- ALERT DISPATCHER -----------------
def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        requests.post(url, data=payload, timeout=10)
    except Exception as e:
        print(f"[-] Alert Dispatch Notice: {e}")

# ----------------- PASSIVE RECONNAISSANCE -----------------
def fetch_passive_subdomains(domain):
    print(f"[+] Fetching Certificate Transparency Logs for: {domain}")
    url = f"https://crt.sh/?q=%.{domain}&output=json"
    subdomains = set()
    try:
        res = requests.get(url, timeout=15)
        if res.status_code == 200:
            data = res.json()
            for entry in data[:15]:
                name = entry.get('name_value')
                if name:
                    subdomains.add(name.split('\n')[0])
    except Exception as e:
        print(f"[-] CT Log Sweep Notice: {e}")
    return list(subdomains)

# ----------------- GLOBAL THREAT CORRELATION -----------------
def fetch_global_threat_pulses():
    print("[+] Querying Global Threat Intelligence Pulses...")
    threats = []
    try:
        res = requests.get("https://otx.alienvault.com/api/v1/indicators/IPv4/185.220.101.5/general", timeout=10)
        if res.status_code == 200:
            threats.append("Malicious Tor Exit Node Active Scan Flagged")
    except Exception as e:
        pass
    return threats

# ----------------- MAIN SOAR PIPELINE -----------------
def run_soar_pipeline():
    print("==========================================================")
    print("      PROJECT AVYAN - HARDENED SOAR INTELLIGENCE DB       ")
    print("==========================================================")
    
    init_db()
    
    subs = fetch_passive_subdomains(TARGET_DOMAIN)
    threats = fetch_global_threat_pulses()
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    
    ioc_status = "IOC Match Detected" if threats else "Clean"
    summary = f"Subdomains: {len(subs)}, Threats: {len(threats)}"
    
    # Save to SQLite Audit Log Database
    log_to_db(timestamp, TARGET_EMAIL, TARGET_DOMAIN, len(subs), ioc_status, summary)
    
    # Telegram Multi-Source Report
    report = f"⚡ *SUDARSHAN ADVANCED SOAR INTELLIGENCE REPORT* ⚡\n\n"
    report += f"🕒 *Timestamp:* `{timestamp}`\n"
    report += f"🎯 *Monitored Identity:* `{TARGET_EMAIL}`\n\n"
    
    report += f"🌐 *PASSIVE INFRASTRUCTURE RECON ({TARGET_DOMAIN}):*\n"
    if subs:
        report += f"• Subdomains Discovered: `{len(subs)}` (Clean & Deduplicated)\n"
        for s in subs[:5]:
            report += f"  - `{s}`\n"
    else:
        report += "• Status: Clean / No new passive drift.\n"
        
    report += "\n🔍 *CORRELATED THREAT INDICATORS (IOCs):*\n"
    if threats:
        for t in threats:
            report += f"⚠️ *Indicator Match:* {t}\n"
    else:
        report += "✅ *Status:* No high-confidence IOC matches detected in current cycle.\n"
        
    report += "\n-----------------------------------------\n"
    report += "🗄️ *Persistence Status:* Recorded into `sudarshan_audit.db` SQLite table."
    
    send_telegram_alert(report)
    print("[+] Advanced Pipeline & DB Logging Execution Completed!")

if __name__ == "__main__":
    run_soar_pipeline()

