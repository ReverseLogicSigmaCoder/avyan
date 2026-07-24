import requests

# Direct Test Credentials (Only inside this script)
BOT_TOKEN = "8627150645:AAEX2lahyNOtfbQtQKYw9kXp3E9nIK4kC8c"
CHAT_ID = "7459821254"

def send_test_alert(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("\n[+] Telegram Alert Sent Successfully! Check your phone.")
        else:
            print(f"\n[-] Failed to send: {response.text}")
    except Exception as e:
        print(f"\n[-] Error: {e}")

if __name__ == "__main__":
    send_test_alert("🚨 [SUDARSHAN ALERT]: Live Notification Test Successful!")
