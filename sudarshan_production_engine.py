import os
import socket
import requests
import json

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

def send_telegram_alert(message: str) -> bool:
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("[SECURE_LOG] Telegram credentials not configured in environment.")
        return False
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        response = requests.post(url, json=payload, timeout=10)
        return response.status_code == 200
    except requests.RequestException as e:
        print(f"[ALERT_ERROR] {e}")
        return False

def check_security_headers(target_url: str) -> dict:
    results = {}
    mandatory_headers = ["Strict-Transport-Security", "X-Frame-Options", "X-Content-Type-Options", "Content-Security-Policy"]
    try:
        if not target_url.startswith(("http://", "https://")):
            target_url = "https://" + target_url
        resp = requests.get(target_url, allow_redirects=False, timeout=10)
        for h in mandatory_headers:
            results[h] = "PASS" if h in resp.headers else "FAIL"
    except Exception as err:
        results["error"] = str(err)
    return results

def probe_scada_ports(host: str) -> dict:
    ports = {"Modbus_TCP": 502, "DNP3": 20000, "IEC_104": 2404}
    status = {}
    for proto, port in ports.items():
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2.0)
        res = sock.connect_ex((host, port))
        status[proto] = "OPEN/EXPOSED" if res == 0 else "CLOSED/SECURE"
        sock.close()
    return status

if __name__ == "__main__":
    print("[+] Sudarshan Production Engine is active and clean.")
