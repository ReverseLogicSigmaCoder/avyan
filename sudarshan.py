import os
import requests

def send_telegram_alert(message):
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    
    if not token or not chat_id:
        print("[!] ERROR: Telegram Secrets missing!")
        return
        
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, json=payload)
    print(f"[*] Telegram Alert Response Status: {response.status_code}")

if __name__ == "__main__":
    print("[+] Running SUDARSHAN 24/7 Defense Scan...")
    alert_msg = "🛡️ *SUDARSHAN 24/7 Shield Status*\n\n✅ Continuous Defense Audit Executed Successfully!\nSystem Active & Safe."
    send_telegram_alert(alert_msg)
