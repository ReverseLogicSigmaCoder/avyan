import requests

# Tor SOCKS5 Proxy Configuration
tor_proxy = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}

print("[+] Testing Tor Proxy Connection...")

try:
    # Tor Network ke zariye IP check
    response = requests.get("https://check.torproject.org/api/ip", proxies=tor_proxy, timeout=15)
    print(f"[SUCCESS] Tor Connected IP Data: {response.json()}")
except Exception as e:
    print(f"[-] Connection Error: {e}")

import requests
import re

tor_proxy = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}

def scan_darkweb_leaks(target_domain):
    print(f"[+] SUDARSHAN Scraper Scanning Dark Web Feeds for Domain: {target_domain}...")
    
    # Test Data Feed URL
    url = f"https://httpbin.org/anything?domain={target_domain}"
    
    try:
        response = requests.get(url, proxies=tor_proxy, timeout=15)
        if response.status_code == 200:
            print("[+] Connection Established via Tor SOCKS5 Proxy.")
            
            # Regex Pattern to Extract Leaked Emails / Hashes
            raw_text = response.text
            email_pattern = r'[a-zA-Z0-9._%+-]+@' + re.escape(target_domain)
            leaks_found = re.findall(email_pattern, raw_text)
            
            print(f"[SUCCESS] Scan Complete! Total Matches Extracted: {len(leaks_found)}")
            return leaks_found
    except Exception as e:
        print(f"[-] Dark Web Proxy Error: {e}")

if __name__ == "__main__":
    scan_darkweb_leaks("gov.in")
