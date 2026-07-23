import os
import json
import sqlite3
import datetime
import requests
import sys

# ----------------- CONFIGURATION -----------------
# Reading from environment, with fallbacks to your specific credentials
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8627150645:AAEyQnGuSEsW8j3JmxZMjFLLy7GBYL0C_I0")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "7459821254")
DB_FILE = "sudarshan_audit.db"

# Headers to mimic legitimate browser inspection
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS certin_findings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            target_domain TEXT NOT NULL,
            exposed_endpoint TEXT NOT NULL,
            severity TEXT NOT NULL,
            status TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def send_telegram_alert(message):
    if not BOT_TOKEN or not CHAT_ID:
        print("[-] Error: Telegram Token or Chat ID missing.")
        return
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        res = requests.post(url, data=payload, timeout=10)
        if res.status_code == 200:
            print("[+] Instant Telegram Alert Sent Successfully!")
        else:
            print(f"[-] Telegram API Error: {res.text}")
    except Exception as e:
        print(f"[-] Telegram Dispatch Failure: {e}")

# ----------------- REAL-WORLD CERT-IN LOGIC CHECKER -----------------
def Scan_Real_Target_For_CERTIn(domain_name):
    # Sanitize domain input
    domain = domain_name.strip().lower().replace("https://", "").replace("http://", "").split('/')[0]
    base_url = f"https://{domain}"
    
    print(f"\n[+] SUDARSHAN ENGINE: Initiating Real Target Scan on -> {base_url}")
    
    # Critical Paths for CERT-In Reporting (Data Exposures / Sensitive Leaks)
    critical_paths = [
        "/.env",
        "/.git/config",
        "/backup.sql",
        "/db_backup.sql",
        "/config.json",
        "/api/v1/debug",
        "/phpinfo.php",
        "/actuator/env"
    ]
    
    found_vulnerabilities = []
    
    for path in critical_paths:
        target_endpoint = f"{base_url}{path}"
        print(f"[*] Auditing Path: {path} ...", end="\r")
        try:
            res = requests.get(target_endpoint, headers=HEADERS, timeout=6, allow_redirects=False)
            
            # If server responds with 200 OK and significant content length, flag potential exposure
            if res.status_code == 200 and len(res.text) > 20:
                print(f"\n[🚨 CRITICAL FINDING]: Exposed Path Discovered -> {target_endpoint}")
                finding_info = {
                    "endpoint": target_endpoint,
                    "status_code": res.status_code,
                    "content_length": len(res.text),
                    "severity": "CRITICAL"
                }
                found_vulnerabilities.append(finding_info)
                
                # Save to DB
                conn = sqlite3.connect(DB_FILE)
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO certin_findings (timestamp, target_domain, exposed_endpoint, severity, status) 
                    VALUES (?, ?, ?, ?, ?)
                ''', (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), domain, target_endpoint, "CRITICAL", "UNREPORTED"))
                conn.commit()
                conn.close()
        except Exception:
            pass
            
    print(f"\n[+] Audit Completed for {domain}. Total Leaks Flagged: {len(found_vulnerabilities)}")
    return domain, found_vulnerabilities

# ----------------- MAIN PRODUCTION EXECUTION -----------------
if __name__ == "__main__":
    init_db()
    
    print("==========================================================")
    print("   SUDARSHAN REAL-WORLD ASSET EXPOSURE ENGINE (CERT-In)   ")
    print("==========================================================")
    
    # Ask user for REAL domain input dynamically at runtime
    if len(sys.argv) > 1:
        user_target = sys.argv[1]
    else:
        user_target = input("\n👉 Enter Target Domain to Scan (e.g., targetdomain.in): ").strip()
        
    if not user_target:
        print("[-] Error: No domain provided. Exiting.")
        sys.exit(1)
        
    target, leaks = Scan_Real_Target_For_CERTIn(user_target)
    
    if leaks:
        alert_msg = f"🚨 *CERT-In POTENTIAL FINDING DISCOVERED* 🚨\n\n"
        alert_msg += f"🌐 *Target Domain:* `{target}`\n"
        alert_msg += f"⚠️ *Exposed Endpoints Found:* `{len(leaks)}`\n\n"
        for idx, item in enumerate(leaks, 1):
            alert_msg += f"{idx}. Endpoint: `{item['endpoint']}`\n"
            alert_msg += f"   Status: `{item['status_code']}` | Size: `{item['content_length']} bytes`\n\n"
        alert_msg += "📋 *Next Step:* Verify in browser, capture PoC, and prepare CERT-In CVD Report!"
        
        send_telegram_alert(alert_msg)
    else:
        print("\n[+] No sensitive exposed files (`.env`, `.sql`, etc.) found on standard paths for this domain.")

