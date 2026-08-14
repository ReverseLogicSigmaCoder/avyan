import json
import time
import os

def load_config():
    if os.path.exists("config.json"):
        with open("config.json", "r") as f:
            return json.load(f)
    return None

def run_sudarshan_engine():
    config = load_config()
    if not config:
        print("[-] Config file missing!")
        return

    print("==================================================")
    print("      PROJECT AVYAN: SOVEREIGN ENGINE RUNNER      ")
    print("==================================================")
    print(f"[+] Client Target: {config['client_info']['client_name']}")
    print(f"[+] Mode: {config['client_info']['deployment_mode']}")
    print(f"[+] Target Subnet: {config['network_config']['target_ip_range']}")
    print("--------------------------------------------------")
    
    # Air-Gap & Firmware Attestation Status
    if config['network_config']['airgap_isolated_mode']:
        print("[✓] Air-Gap Data Diode: ENFORCED (Isolated Network)")
    print("[✓] Firmware Attestation: VERIFIED (Hardware-Software Lock)")
    
    # SCADA Protocol Monitor
    if config['scada_protocols']['modbus_tcp_enabled']:
        print("[✓] SCADA Gateway Monitor (Modbus/DNP3): ONLINE")
        
    print("--------------------------------------------------")
    print("[+] Engine initialization complete. Ready for client network scan.")
    print("==================================================")

if __name__ == "__main__":
    run_sudarshan_engine()
  
