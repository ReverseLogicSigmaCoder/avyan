import os
import json
import sqlite3
import datetime
import requests

# ----------------- CONFIGURATION -----------------
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8627150645:AAFs3xoo0z2odb7cZgw2Em80s8H2gOb-oKE")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "7459821254")

DB_FILE = "sudarshan_audit.db"
MONITORED_ASSET = "example.com"  # Generic reference asset

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AVYAN-Sudarshan-ThreatIntel/1.0"
}

# ----------------- DATABASE SETUP -----------------
def init_threat_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS threat_incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            source TEXT NOT NULL,
            threat_type TEXT NOT NULL,
            severity TEXT NOT NULL,
            details TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def log_incident(timestamp, source, threat_type, severity, details):
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO threat_incidents (timestamp, source, threat_type, severity, details)
            VALUES (?, ?, ?, ?, ?)
        ''', (timestamp, source, threat_type, severity, details))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[-] DB Logging Error: {e}")

# ----------------- THREAT INTEL AGGREGATOR -----------------
def fetch_public_threat_advisories():
    print("[+] Fetching Global Public Threat Feeds & Bulletins...")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    
    # Generic public vulnerability/threat source example (CISA / NVD feed structure)
    feed_url = "https://cve.circl.lu/api/last"
    
    incidents_found = []
    try:
        res = requests.get(feed_url, headers=HEADERS, timeout=10)
        if res.status_code == 200:
            data = res.json()
            # Analyze top recent published vulnerabilities
            for item in data[:3]:
                cve_id = item.get('id', 'N/A')
                summary = item.get('summary', 'No summary provided.')[:120]
                incidents_found.append({
                    "cve_id": cve_id,
                    "summary": summary
                })
                log_incident(timestamp, "CIRCL CVE Feed", "Vulnerability Advisory", "Medium", f"{cve_id}: {summary}")
            print(f"[+] Successfully aggregated {len(incidents_found)} public advisories.")
    except Exception as e:
        print(f"[-] Threat Feed Notice: {e}")
        
    return incidents_found

# ----------------- CERT-In ADVISORY GENERATOR -----------------
def generate_certin_threat_advisory(incidents):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    advisory_file = f"certin_threat_advisory_{timestamp}.json"
    
    advisory_data = {
        "metadata": {
            "title": "CERT-In Compliant Cyber Threat Intelligence Advisory",
            "generated_by": "AVYAN - SUDARSHAN SOAR Engine",
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC"),
            "compliance_standard": "CERT-In Incident Handling & CVD Standards"
        },
        "monitored_scope": {
            "target_sector": "Strategic & Government Enterprises Baseline",
            "primary_asset": MONITORED_ASSET
        },
        "threat_summary": {
            "total_incidents_logged": len(incidents),
            "threat_classification": "Threat Intelligence Feed Sync"
        },
        "actionable_advisories": incidents
    }
    
    with open(advisory_file, "w") as f:
        json.dump(advisory_data, f, indent=4)
        
    print(f"[+] CERT-In Threat Advisory generated: {advisory_file}")
    return advisory_file

# ----------------- TELEGRAM DISPATCHER -----------------
def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        requests.post(url, data=payload, timeout=10)
    except Exception as e:
        print(f"[-] Telegram Dispatch Notice: {e}")

# ----------------- MAIN PIPELINE -----------------
def run_threat_pipeline():
    print("==========================================================")
    print("   PROJECT AVYAN - THREAT INTEL & INCIDENT ENGINE         ")
    print("==========================================================")
    
    init_threat_db()
    incidents = fetch_public_threat_advisories()
    advisory_file = generate_certin_threat_advisory(incidents)
    
    alert_msg = f"🛡️ *SUDARSHAN THREAT INTEL ALERT* 🛡️\n\n"
    alert_msg += f"🕒 *Time:* `{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}`\n"
    alert_msg += f"📊 *Threat Feeds Processed:* `{len(incidents)}`\n"
    alert_msg += f"📄 *Advisory File:* `{advisory_file}`\n\n"
    alert_msg += "✅ Threat Intelligence Pipeline executed successfully!"
    
    send_telegram_alert(alert_msg)
    print("[+] Pipeline Execution Completed!")

if __name__ == "__main__":
    run_threat_pipeline()
