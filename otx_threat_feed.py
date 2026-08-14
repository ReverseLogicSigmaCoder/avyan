import os
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
