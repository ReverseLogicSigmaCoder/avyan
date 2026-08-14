import urllib.request
import json
import sys
import os
from datetime import datetime, timezone

# Target Government Domains List for Passive Reconnaissance
GOV_TARGET_DOMAINS = [
    "digitalindia.gov.in",
    "mygov.in",
    "mca.gov.in",
    "ncs.gov.in"
]

def fetch_crtsh_subdomains(domain):
    """Fetches public Certificate Transparency logs via crt.sh (Purely Passive)."""
    subdomains = set()
    url = f"https://crt.sh/?q=%.{domain}&output=json"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (SUDARSHAN-Passive-Engine)'})
        with urllib.request.urlopen(req, timeout=10, timeout=10, timeout=12) as response:
            if response.status == 200:
                data = json.loads(response.read().decode('utf-8'))
                for entry in data:
                    name_val = entry.get('name_value', '')
                    for sub in name_val.split('\n'):
                        clean_sub = sub.strip().lower()
                        if domain in clean_sub and not clean_sub.startswith('*'):
                            subdomains.add(clean_sub)
    except Exception as e:
        print(f"[!] Warning fetching CT logs for {domain}: {e}")
    return sorted(list(subdomains))

def run_full_passive_recon():
    print("="*60)
    print("   SUDARSHAN PASSIVE OSINT ENGINE - GOV DOMAIN RECON    ")
    print("="*60)
    
    master_results = {
        "engine": "SUDARSHAN Passive OSINT Engine",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "targets_scanned": len(GOV_TARGET_DOMAINS),
        "recon_data": {}
    }

    for target in GOV_TARGET_DOMAINS:
        print(f"\n[+] Querying Public CT Logs for: {target}...")
        discovered_subs = fetch_crtsh_subdomains(target)
        master_results["recon_data"][target] = {
            "total_subdomains": len(discovered_subs),
            "subdomains_sample": discovered_subs[:30] # Limit sample size
        }
        print(f"[SUCCESS] Discovered {len(discovered_subs)} public subdomains for {target}.")

    # Save output to JSON
    output_filename = "passive_recon_results.json"
    with open(output_filename, "w") as f:
        json.dump(master_results, f, indent=4)
    print(f"\n[+] Master Passive Recon Report saved to: {output_filename}")

if __name__ == "__main__":
    run_full_passive_recon()
