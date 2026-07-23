import requests

# Public Indicator Feed Endpoint (No API Key Required)
OTX_PUBLIC_API = "https://otx.alienvault.com/api/v1/indicators/IPv4/8.8.8.8/general"

def fetch_threat_intelligence():
    print("[+] SUDARSHAN Engine: Fetching Global Threat Data...")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }
    
    try:
        response = requests.get(OTX_PUBLIC_API, headers=headers, timeout=20)
        
        if response.status_code == 200:
            print("[SUCCESS] OTX Threat Intelligence Feed Connected Successfully!")
            data = response.json()
            pulse_info = data.get('pulse_info', {})
            count = pulse_info.get('count', 0)
            print(f"[+] Total Threat Records Associated: {count}")
            return True
        else:
            print(f"[-] OTX API Returned Status Code: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"[-] Threat Feed Fetch Error: {e}")
        return False

if __name__ == "__main__":
    fetch_threat_intelligence()



import requests

# Test Indicator (Querying an OTX IP endpoint)
TARGET_IP = "185.220.101.5"  # Sample Tor exit node/flagged IP for testing
OTX_PUBLIC_API = f"https://otx.alienvault.com/api/v1/indicators/IPv4/{TARGET_IP}/general"

def fetch_threat_intelligence():
    print(f"[+] SUDARSHAN Engine: Scanning Threat Intelligence for Target IP [{TARGET_IP}]...")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }
    
    try:
        response = requests.get(OTX_PUBLIC_API, headers=headers, timeout=20)
        
        if response.status_code == 200:
            print("[SUCCESS] Threat Feed Data Retrieved!\n")
            data = response.json()
            
            pulse_info = data.get('pulse_info', {})
            pulses = pulse_info.get('pulses', [])
            
            print(f"================ Threat Detection Report ================")
            print(f"Target IP Analyzed : {TARGET_IP}")
            print(f"Total Threat Pulses : {len(pulses)}")
            print(f"========================================================\n")
            
            if len(pulses) == 0:
                print("[SAFE] No malicious threat records detected for this target.")
            else:
                for idx, pulse in enumerate(pulses, start=1):
                    print(f"[{idx}] DETECTED THREAT DETAILS:")
                    print(f"   - Name        : {pulse.get('name')}")
                    print(f"   - Description : {pulse.get('description', 'N/A')[:100]}...")
                    print(f"   - Tags        : {', '.join(pulse.get('tags', []))}")
                    print(f"   - Created On  : {pulse.get('created')}")
                    print("-" * 55)
            return True
        else:
            print(f"[-] OTX API Status Code: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"[-] Fetch Error: {e}")
        return False

if __name__ == "__main__":
    fetch_threat_intelligence()


import requests

# ----------------- TELEGRAM BOT CONFIGURATION -----------------
TELEGRAM_BOT_TOKEN = "8627150645:AAFs3xoo0z2odb7cZgw2Em80s8H2gOb-oKE"
  # Place your Bot Father Token here
TELEGRAM_CHAT_ID = "7459821254"      # Place your Chat ID here

def send_telegram_alert(message):
    """Sends a formatted alert message to the configured Telegram Bot."""
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
            print(f"[-] Failed to send Telegram alert. Status: {response.status_code}")
    except Exception as e:
        print(f"[-] Telegram Notification Error: {e}")

# ----------------- THREAT INTELLIGENCE ENGINE -----------------
TARGET_IP = "185.220.101.5"  # Sample IP for testing threat alerts
OTX_PUBLIC_API = f"https://otx.alienvault.com/api/v1/indicators/IPv4/{TARGET_IP}/general"

def fetch_threat_intelligence():
    print(f"[+] SUDARSHAN Engine: Scanning Threat Intelligence for Target IP [{TARGET_IP}]...")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }
    
    try:
        response = requests.get(OTX_PUBLIC_API, headers=headers, timeout=20)
        
        if response.status_code == 200:
            data = response.json()
            pulse_info = data.get('pulse_info', {})
            pulses = pulse_info.get('pulses', [])
            
            total_pulses = len(pulses)
            print(f"[SUCCESS] Scanned Target. Total Pulses Found: {total_pulses}")
            
            if total_pulses > 0:
                # Construct detailed Markdown report for Telegram
                alert_text = f"🚨 *SUDARSHAN SECURITY ENGINE ALERT* 🚨\n\n"
                alert_text += f"📍 *Target IP Analyzed:* `{TARGET_IP}`\n"
                alert_text += f"⚠️ *Total Threat Pulses:* {total_pulses}\n\n"
                alert_text += "--- *DETAILED THREAT FINDINGS* ---\n"
                
                for idx, pulse in enumerate(pulses[:3], start=1):  # Top 3 threat details
                    name = pulse.get('name', 'N/A')
                    desc = pulse.get('description', 'No description available')[:120]
                    tags = ", ".join(pulse.get('tags', []))
                    created = pulse.get('created', 'N/A')
                    
                    alert_text += f"\n*{idx}. Threat Name:* {name}\n"
                    alert_text += f"   - *Description:* {desc}...\n"
                    alert_text += f"   - *Tags:* `{tags}`\n"
                    alert_text += f"   - *Reported Date:* {created}\n"
                
                # Trigger Telegram Alert
                send_telegram_alert(alert_text)
            else:
                print("[SAFE] No active threat records found.")
            return True
        else:
            print(f"[-] OTX API Status Code: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"[-] Threat Feed Fetch Error: {e}")
        return False

if __name__ == "__main__":
    fetch_threat_intelligence()

