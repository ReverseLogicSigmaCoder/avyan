import sys
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
