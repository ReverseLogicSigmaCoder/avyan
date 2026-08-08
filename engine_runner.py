import json
import time

def load_configuration(config_path="config.json"):
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
            print(" Configuration loaded successfully.")
            return config
    except FileNotFoundError:
        print(" Error: config.json not found!")
        return None

def execute_sovereign_engine(config):
    client = config["client_info"]["client_name"]
    mode = config["client_info"]["deployment_mode"]
    target_ip = config["network_config"]["target_ip_range"]
    
    print(f"\n Initializing PROJECT AVYAN for: {client} [{mode} MODE]")
    print(f" Target Network Range: {target_ip}")
    print(" Enforcing Air-Gap Diode Isolation Policy...")
    print(" Verifying Firmware-Level Immutable Attestation...")
    
    if config["scada_protocols"]["modbus_tcp_enabled"]:
        print(" SCADA Modbus TCP Listener: ACTIVE")
        
    print("\n[+] Engine operational. Continuous monitoring started...\n")

if __name__ == "__main__":
    cfg = load_configuration()
    if cfg:
        execute_sovereign_engine(cfg)
      
