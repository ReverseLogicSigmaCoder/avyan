import socket
import json
from datetime import datetime, timezone

def verify_target_sockets():
    """
    Day 86: Core Logging, Dynamic Input & Socket Verification Engine.
    Scans essential ports with robust exception handling and logs structured telemetry.
    """
    print("[*] Initializing SUDARSHAN Day 86 Socket Verification Engine...")
    
    target_host = "127.0.0.1" # Default local secure loopback target
    ports_to_check = [21, 22, 80, 443, 3306]
    scan_results = {}

    for port in ports_to_check:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2.0)
            result = sock.connect_ex((target_host, port))
            if result == 0:
                scan_results[port] = "OPEN [✅]"
            else:
                scan_results[port] = "CLOSED [❌]"
            sock.close()
        except Exception as e:
            scan_results[port] = f"ERROR: {str(e)}"

    report_data = {
        "engine": "SUDARSHAN Day 86 Socket Engine",
        "target": target_host,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "port_status": scan_results
    }

    log_filename = "day86_socket_audit.json"
    with open(log_filename, "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=4)

    print(f"[+] Day 86 Socket Audit completed successfully. Saved to {log_filename}")
    return report_data

if __name__ == "__main__":
    verify_target_sockets()
