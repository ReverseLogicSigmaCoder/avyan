import urllib.request
import json
from datetime import datetime, timezone

def fetch_crtsh_subdomains(domain):
    """
    100% Passive Subdomain Enumeration using Public Certificate Transparency Logs (crt.sh).
    Does NOT send any traffic to the target domain server.
    """
    clean_domain = domain.replace("https://", "").replace("http://", "").split("/")[0]
    crt_url = f"https://crt.sh/?q=%.{clean_domain}&output=json"
    
    subdomains = set()
    print(f"[+] [PASSIVE OSINT] Fetching Public CT Logs for domain: {clean_domain}...")
    
    try:
        req = urllib.request.Request(crt_url, headers={'User-Agent': 'Mozilla/5.0 (SUDARSHAN-Passive-Recon)'})
        with urllib.request.urlopen(req, timeout=10, timeout=10, timeout=10) as response:
            if response.status == 200:
                data = json.loads(response.read().decode('utf-8'))
                for entry in data:
                    name_value = entry.get('name_value', '')
                    for sub in name_value.split('\n'):
                        if clean_domain in sub and not sub.startswith('*'):
                            subdomains.add(sub.strip())
    except Exception as e:
        print(f"[!] CT Log Fetch Exception (Passive): {e}")
        
    return sorted(list(subdomains))

def run_passive_osint_audit(domain):
    discovered = fetch_crtsh_subdomains(domain)
    return {
        "engine": "SUDARSHAN OSINT Passive Subdomain Engine",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "target_domain": domain,
        "total_subdomains_found": len(discovered),
        "subdomains": discovered[:50]  # Limit output preview to top 50
    }

if __name__ == "__main__":
    # Safe test on authorized public scope
    test_domain = "example.com"
    results = run_passive_osint_audit(test_domain)
    print("\n=== PASSIVE OSINT AUDIT RESULTS ===")
    print(json.dumps(results, indent=2))
