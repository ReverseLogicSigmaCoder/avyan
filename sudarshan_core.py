import json
import os
import subprocess
import time

def print_banner():
    banner = """
    ==================================================
        PROJECT AVYAN | SCANNING ENGINE: SUDARSHAN
      Real-Time CERT-In & DAST Compliance Audit Module
    ==================================================
    """
    print(banner)

def run_port_scan(target):
    print(f"[*] Starting Initial Surface Assessment on: {target}")
    # Nmap JSON / XML simulation wrapper for fast baseline analysis
    cmd = f"nmap -F {target}"
    try:
        result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
        print("[+] Surface Scan Complete!")
        return result.decode('utf-8')
    except Exception as e:
        return f"[-] Scan Error: {str(e)}"

def generate_audit_payload(target, raw_scan):
    # CERT-In Compliance JSON Mapping Format
    audit_data = {
        "engine": "SUDARSHAN v1.0",
        "target": target,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "compliance_framework": "CERT-In Baseline Guidelines",
        "findings": {
            "surface_ports": raw_scan,
            "dast_status": "PENDING_NUCLEI_INTEGRATION",
            "sbom_status": "PENDING_TRIVY_INTEGRATION"
        }
    }
    
    filename = f"sudarshan_audit_{target.replace('.', '_')}.json"
    with open(filename, "w") as f:
        json.dump(audit_data, f, indent=4)
    print(f"[+] Baseline Audit Payload generated: {filename}")

if __name__ == "__main__":
    print_banner()
    target_domain = input("Enter target domain/IP for baseline testing (e.g., scanme.nmap.org): ")
    if target_domain.strip():
        scan_output = run_port_scan(target_domain)
        print("\n--- RAW SCAN OUTPUT ---")
        print(scan_output)
        print("-----------------------")
        generate_audit_payload(target_domain, scan_output)
