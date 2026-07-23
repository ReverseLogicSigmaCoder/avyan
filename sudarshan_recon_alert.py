import os
import sqlite3
import datetime
import requests

# Config
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8627150645:AAFs3xoo0z2odb7cZgw2Em80s8H2gOb-oKE")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "7459821254")
DB_FILE = "sudarshan_audit.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS asset_inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            subdomain TEXT UNIQUE NOT NULL,
            status TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        requests.post(url, data=payload, timeout=10)
    except Exception as e:
        print(f"[-] Telegram Dispatch Error: {e}")

def scan_target_subdomains(target_domain):
    print(f"[+] SUDARSHAN RECON: Scanning assets for {target_domain}...")
    url = f"https://crt.sh/?q=%.{target_domain}&output=json"
    
    new_assets = []
    try:
        res = requests.get(url, timeout=15)
        if res.status_code == 200:
            data = res.json()
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            
            for entry in data:
                subdomain = entry.get('name_value', '').lower()
                if '\n' in subdomain:
                    subdomains = subdomain.split('\n')
                else:
                    subdomains = [subdomain]
                
                for sub in subdomains:
                    sub = sub.strip('* .')
                    if sub and sub.endswith(target_domain):
                        try:
                            cursor.execute('''
                                INSERT INTO asset_inventory (timestamp, subdomain, status)
                                VALUES (?, ?, ?)
                            ''', (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), sub, "NEW_DISCOVERED"))
                            conn.commit()
                            new_assets.append(sub)
                        except sqlite3.IntegrityError:
                            pass # Pehle se DB mein hai
            conn.close()
    except Exception as e:
        print(f"[-] Scan Exception: {e}")
        
    return new_assets

if __name__ == "__main__":
    init_db()
    # Test target domain
    target = "example.com"
    found = scan_target_subdomains(target)
    
    if found:
        msg = f"🎯 *SUDARSHAN ASSET DISCOVERY ALERT* 🎯\n\n"
        msg += f"🌐 *Target:* `{target}`\n"
        msg += f"🆕 *New Subdomains Found:* `{len(found)}`\n\n"
        msg += "📋 *Sample Assets:*\n"
        for item in found[:5]:
            msg += f"• `{item}`\n"
        msg += "\n🔍 *Action Required:* Inspect manually for exposed panels or logic leaks."
        send_telegram_alert(msg)
        print(f"[+] Alert Sent! Found {len(found)} new subdomains.")
    else:
        print("[+] No new assets discovered.")
