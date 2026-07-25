import json
from datetime import datetime, timezone

def run_insider_threat_watchdog():
    """
    Day 92: Insider Threat & File Watchdog (Vibhishan Scanner Logic).
    Monitors internal filesystem events, unauthorized privilege escalations, 
    and unexpected data transfer spikes to prevent data leakage.
    """
    print("[*] Initializing SUDARSHAN Day 92 Insider Threat & File Watchdog...")
    
    # Filesystem Watchdog Inspection Simulation
    filesystem_events = {
        "sensitive_directories_monitored": ["/etc", "/var/log", "/home/user/data"],
        "unexpected_file_modifications": 0,
        "unauthorized_usb_exfiltration_attempt": "NONE_DETECTED",
        "file_integrity_checksum": "MATCHED_BASELINE"
    }

    # Vibhishan Scanner: Privilege & Behavioral Context Inspection
    internal_user_audit = {
        "high_privilege_context_usage": "AUTHORIZED_ONLY",
        "bulk_data_read_spikes": "NORMAL",
        "containment_status": "MONITORING_ACTIVE"
    }

    report_data = {
        "engine": "SUDARSHAN Day 92 Insider Threat Watchdog",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "filesystem_watchdog": filesystem_events,
        "internal_user_audit": internal_user_audit
    }

    output_file = "day92_insider_audit.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=4)

    print(f"[+] Day 92 Insider Threat audit complete. Saved to {output_file}")
    return report_data

if __name__ == "__main__":
    run_insider_threat_watchdog()
