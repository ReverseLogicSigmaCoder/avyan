import os

files_content = {
    "sudarshan_production_engine.py": '''import os
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
        resp = requests.get(target_url, timeout=10)
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
    print("[+] Engine operational.")
''',

    "sample_app.py": '''import shlex
import subprocess
from urllib.parse import urlparse

def run_diagnostic_ping(target_domain: str) -> str:
    cleaned = target_domain.strip().lower()
    if "://" in cleaned:
        cleaned = urlparse(cleaned).netloc
    safe_target = shlex.quote(cleaned)
    try:
        result = subprocess.run(["ping", "-c", "1", safe_target], capture_output=True, text=True, timeout=5, check=False)
        return result.stdout if result.returncode == 0 else "Host unreachable."
    except Exception as e:
        return f"Error: {e}"
''',

    "sudarshan_executor.py": '''import sys
from urllib.parse import urlparse
import requests

def sanitize_and_validate_target(raw_input: str) -> str:
    cleaned = raw_input.strip()
    if not cleaned.startswith(("http://", "https://")):
        cleaned = "https://" + cleaned
    parsed = urlparse(cleaned)
    if not parsed.netloc or parsed.scheme not in ["http", "https"]:
        raise ValueError("Invalid target domain or URL scheme.")
    return f"{parsed.scheme}://{parsed.netloc}"

def execute_live_probe(target_endpoint: str):
    try:
        sanitized_url = sanitize_and_validate_target(target_endpoint)
        res = requests.get(sanitized_url, timeout=10)
        print(f"[+] Scan status: {res.status_code}")
    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "digitalindia.gov.in"
    execute_live_probe(target)
''',

    "otx_threat_feed.py": '''import os
import requests

OTX_API_KEY = os.getenv("OTX_API_KEY", "")

def fetch_threat_indicators():
    if not OTX_API_KEY:
        print("[SECURE_LOG] OTX API key not configured.")
        return []
    url = "https://otx.alienvault.com/api/v1/pulses/subscribed"
    headers = {"X-OTX-API-KEY": OTX_API_KEY}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        return res.json().get("results", []) if res.status_code == 200 else []
    except Exception as e:
        print(f"[ERROR] {e}")
        return []
'''
}

for fname, code in files_content.items():
    with open(fname, "w") as f:
        f.write(code)
    print(f"[UPDATED] {fname}")

# Workflow persist-credentials fix
wf_path = ".github/workflows"
if os.path.exists(wf_path):
    for yml_file in os.listdir(wf_path):
        if yml_file.endswith(".yml"):
            full_p = os.path.join(wf_path, yml_file)
            with open(full_p, "r") as f:
                content = f.read()
            if "uses: actions/checkout@" in content and "persist-credentials:" not in content:
                content = content.replace("uses: actions/checkout@v4", "uses: actions/checkout@v4\n        with:\n          persist-credentials: false")
                content = content.replace("uses: actions/checkout@v3", "uses: actions/checkout@v4\n        with:\n          persist-credentials: false")
                with open(full_p, "w") as f:
                    f.write(content)
                print(f"[SECURED WORKFLOW] {yml_file}")
