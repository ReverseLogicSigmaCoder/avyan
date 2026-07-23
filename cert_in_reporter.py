import json
import datetime
import os

def generate_certin_report(target, threat_type, details, severity="HIGH"):
    """Generates a standardized CERT-In compliant Incident Report."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    report_id = f"AVYAN-CERTIN-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    report_data = {
        "report_header": {
            "platform": "PROJECT AVYAN - SUDARSHAN Security Engine",
            "report_id": report_id,
            "timestamp": timestamp,
            "compliance_standard": "CERT-In Cyber Security Incident Reporting Directives"
        },
        "incident_details": {
            "target_asset": target,
            "threat_category": threat_type,
            "severity_level": severity,
            "evidence_logs": details
        },
        "recommended_actions": [
            "Block malicious IP/Domain at perimeter firewall/DNS sinkhole.",
            "Enforce immediate credential reset and MFA on affected endpoints.",
            "Submit IOC details to national threat sharing databases."
        ]
    }
    
    # Save Report as JSON file for official evidence submission
    os.makedirs("reports", exist_ok=True)
    filename = f"reports/{report_id}.json"
    with open(filename, "w") as f:
        json.dump(report_data, f, indent=4)
        
    print(f"[+] CERT-In Compliant Report Generated: {filename}")
    return report_data, filename

if __name__ == "__main__":
    # Test run
    sample_details = "Detected active malicious scanner node flagged in global threat intel feeds."
    generate_certin_report("185.220.101.5", "Vulnerability/Threat Indicator", sample_details)
