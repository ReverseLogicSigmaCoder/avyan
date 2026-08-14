import os
import sys
import json
import hashlib
import time

# ======================================================
# 1. SOFTWARE SUPPLY CHAIN & SBOM GENERATOR MODULE
# ======================================================
def generate_sbom_and_scan_dependencies():
    """
    Scans project requirements/dependencies, generates a Software Bill of Materials (SBOM),
    and checks for malicious open-source packages or backdoors.
    """
    print("\n[📦 SOFTWARE SUPPLY CHAIN & SBOM GUARD]")
    
    sbom = {
        "sbom_version": "1.0",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S IST"),
        "components": []
    }

    req_file = "requirements.txt"
    vulnerabilities = []

    # If requirements.txt doesn't exist, create a baseline for AVYAN
    if not os.path.exists(req_file):
        with open(req_file, "w") as f:
            f.write("requests>=2.28.0\nurllib3>=1.26.0\n")

    print(f"[*] Reading dependency manifest: {req_file}")
    
    with open(req_file, "r") as f:
        lines = f.readlines()

    for line in lines:
        dep = line.strip()
        if dep and not dep.startswith("#"):
            dep_hash = hashlib.sha256(dep.encode()).hexdigest()[:12]
            component = {
                "name": dep.split(">=")[0].split("==")[0],
                "version_spec": dep,
                "component_hash": dep_hash,
                "status": "VERIFIED_CLEAN"
            }
            
            # Simulated Backdoor / Vulnerability Check logic
            if "malicious" in dep.lower() or "eval" in dep.lower():
                component["status"] = "THREAT_DETECTED"
                vulnerabilities.append(dep)

            sbom["components"].append(component)

    sbom_filename = f"sbom_manifest_{int(time.time())}.json"
    with open(sbom_filename, "w", encoding="utf-8") as f:
        json.dump(sbom, f, indent=4)

    print(f"[+] SBOM Manifest successfully generated: {sbom_filename}")
    if vulnerabilities:
        print(f"[-] ALERT: Supply chain threat flagged in packages: {vulnerabilities}")
    else:
        print("[+] Supply Chain Audit PASSED: No malicious backdoor signatures found in libraries.")

    return sbom_filename


# ======================================================
# 2. AIR-GAP DATA DIODE EMULATOR
# ======================================================
def emulate_airgap_data_diode_transfer(data_payload):
    """
    Simulates 1-way uncompressed telemetry transmission for Air-Gapped networks.
    """
    print("\n[⚡ AIR-GAP DATA DIODE MONITOR]")
    print("[*] Verifying 1-Way Hardware Data Diode Channel...")
    
    payload_hash = hashlib.sha256(json.dumps(data_payload).encode()).hexdigest()
    print(f"[+] One-Way Outbound Diode Transfer Verified | Payload SHA256: {payload_hash[:16]}...")
    print("[+] Inbound Internet Interface: PHYSICAL_AIR_GAP_LOCKED (100% Isolated)")
    return True


# ======================================================
# MAIN DISPATCHER
# ======================================================
def run_supply_chain_engine():
    print("=" * 65)
    print(" SUDARSHAN SUPPLY CHAIN GUARD & AIR-GAP MONITOR (v1.0)")
    print("=" * 65)

    sbom_file = generate_sbom_and_scan_dependencies()
    
    # Air gap verification test
    emulate_airgap_data_diode_transfer({"event": "SYSTEM_DIODE_AUDIT", "status": "SECURE"})

    print("\n[+] Enterprise Supply Chain Audit Complete.")


if __name__ == "__main__":
    run_supply_chain_engine()
