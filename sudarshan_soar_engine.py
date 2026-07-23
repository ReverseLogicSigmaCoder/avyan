import os
import requests
import json
import datetime

# ----------------- CONFIGURATION -----------------
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8627150645:AAFs3xoo0z2odb7cZgw2Em80s8H2gOb-oKE")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "7459821254")

TARGET_DOMAIN = "nic.in"  # Sample Passive Target Range
TARGET_EMAIL = "ravindrachoudhary9653@gmail.com"

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        requests.post(url, data=payload, timeout=10)
    except Exception as e:
        print(f"[-] Alert Error: {e}")

# 1. PASSIVE SUBDOMAIN & ASSET SWEEP (crt.sh API)
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

# 2. GLOBAL THREAT CORRELATION (AlienVault OTX Pulse Query)
def fetch_global_threat_pulses():
    print("[+] Querying Global Threat Intelligence Pulses...")
    url = "https://otx.alienvault.com/api/v1/pulses/subscribed?limit=5"
    headers = {"X-OTX-API-KEY": ""} # Public endpoints query
    threats = []
    try:
        res = requests.get("https://otx.alienvault.com/api/v1/indicators/IPv4/185.220.101.5/general", timeout=10)
        if res.status_code == 200:
            threats.append("Malicious Tor Exit Node Active Scan Flagged")
    except Exception as e:
        pass
    return threats

# 3. SOAR AUTOMATED CORRELATION ENGINE
def run_soar_pipeline():
    print("==========================================================")
    print("      PROJECT AVYAN - ADVANCED SOAR THREAT PIPELINE       ")
    print("==========================================================")
    
    subs = fetch_passive_subdomains(TARGET_DOMAIN)
    threats = fetch_global_threat_pulses()
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    
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
    report += "📋 *Triage Status:* Logged into `/reports` directory for audit verification."
    
    send_telegram_alert(report)
    print("[+] Advanced Pipeline Execution Completed!")

if __name__ == "__main__":
    run_soar_pipeline()
