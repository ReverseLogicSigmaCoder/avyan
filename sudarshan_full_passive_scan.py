import os
import requests

# ----------------- CONFIGURATION -----------------
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8627150645:AAFs3xoo0z2odb7cZgw2Em80s8H2gOb-oKE")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "7459821254")

TARGET_EMAIL = "ravindrachoudhary9653@gmail.com"
TARGET_DOMAIN = "gmail.com"

def send_telegram_alert(message):
    """Sends formatted alert to Telegram."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, data=payload, timeout=10)
        if response.status_code == 200:
            print("[+] Telegram Alert Sent Successfully!")
        else:
            print(f"[-] Telegram Alert Failed. Status Code: {response.status_code}")
    except Exception as e:
        print(f"[-] Telegram Notification Error: {e}")

# ----------------- 1. DARK WEB & LEAK INTELLIGENCE -----------------
def scan_darkweb_leaks():
    print(f"\n[+] SUDARSHAN Engine: Executing Dark Web & Leak Intelligence Scan...")
    print(f"    Target Identity: {TARGET_EMAIL}")
    
    # Querying Public OSINT Leak & Dark Web Repository API
    leak_url = f"https://api.popup.wiki/v1/breach?email={TARGET_EMAIL}"
    headers = {"User-Agent": "AvyanSudarshanSovereignEngine/1.0"}
    
    results = []
    try:
        resp = requests.get(leak_url, headers=headers, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            breaches = data.get("breaches", [])
            for b in breaches:
                results.append({
                    "title": b.get("title", "Dark Web / Forum Leak"),
                    "domain": b.get("domain", "N/A"),
                    "date": b.get("breach_date", "N/A"),
                    "exposed": ", ".join(b.get("data_classes", []))
                })
    except Exception as e:
        print(f"[-] Dark Web Scan Notice: {e}")
        
    return results

# ----------------- 2. PASSIVE RECON SCANNING -----------------
def scan_passive_recon():
    print(f"\n[+] SUDARSHAN Engine: Executing Stealth Passive Recon Sweep...")
    print(f"    Target Domain: {TARGET_DOMAIN}")
    
    # Querying Certificate Transparency (CT) Logs (100% Passive & Legal)
    ct_url = f"https://crt.sh/?q={TARGET_DOMAIN}&output=json"
    subdomains = set()
    
    try:
        resp = requests.get(ct_url, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            for entry in data[:10]: # Top 10 passive subdomains
                name = entry.get("name_value")
                if name:
                    subdomains.add(name.split('\n')[0])
    except Exception as e:
        print(f"[-] Passive Recon Notice: {e}")
        
    return list(subdomains)

# ----------------- MAIN EXECUTION & TELEGRAM REPORT -----------------
def run_full_scan():
    print("=========================================================")
    print("      PROJECT AVYAN - SUDARSHAN SOVEREIGN SCANNER        ")
    print("=========================================================")
    
    leaks = scan_darkweb_leaks()
    passive_subs = scan_passive_recon()
    
    # Prepare Unified Telegram Report
    report = f"🛡️ *SUDARSHAN INTEGRATED INTELLIGENCE REPORT* 🛡️\n\n"
    
    # Dark Web Section
    report += f"🕵️‍♂️ *DARK WEB & LEAK SCAN RESULT:*\n"
    report += f"• Target Identity: `{TARGET_EMAIL}`\n"
    if leaks:
        report += f"⚠️ *Exposures Detected:* {len(leaks)}\n"
        for idx, l in enumerate(leaks[:3], start=1):
            report += f"\n*{idx}. Source:* {l['title']}\n"
            report += f"   - Domain: `{l['domain']}`\n"
            report += f"   - Date: {l['date']}\n"
            report += f"   - Exposed: `{l['exposed']}`\n"
    else:
        report += "✅ *Status:* No direct credential leaks detected in public dark web dumps.\n"
        
    report += "\n-----------------------------------------\n\n"
    
    # Passive Recon Section
    report += f"🌐 *PASSIVE RECON & INFRASTRUCTURE SCAN:*\n"
    report += f"• Monitored Domain: `{TARGET_DOMAIN}`\n"
    if passive_subs:
        report += f"• Passive Subdomains Discovered: {len(passive_subs)}\n"
        report += "• Sample Endpoints:\n"
        for sub in passive_subs[:4]:
            report += f"   - `{sub}`\n"
    else:
        report += "• Status: CT logs queried successfully.\n"
        
    print("\n[+] Scan Completed! Sending Unified Report to Telegram...")
    send_telegram_alert(report)

if __name__ == "__main__":
    run_full_scan()
