import json
import os
from datetime import datetime, timezone

def generate_cert_in_advisory(json_report_path="github_sast_audit_report.json"):
    """
    Reads the SUDARSHAN SAST / DAST audit report and transforms it into 
    a formal CERT-In / NCIIPC compliant vulnerability advisory format.
    """
    if not os.path.exists(json_report_path):
        print(f"[!] Report file {json_report_path} not found. Run a scan first.")
        return None

    try:
        with open(json_report_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"[!] Error reading audit report: {e}")
        return None

    advisory = {
        "advisory_metadata": {
            "issuing_agency": "PROJECT AVYAN - SUDARSHAN Security Engine",
            "compliance_standard": "CERT-In / NCIIPC Vulnerability Disclosure Format",
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "target_inspected": data.get("repository_scanned", "Unknown Target")
        },
        "executive_summary": {
            "total_files_analyzed": data.get("production_files_analyzed", 0),
            "actionable_findings_count": data.get("actionable_vulnerabilities_count", 0),
            "risk_status": "HIGH" if data.get("actionable_vulnerabilities_count", 0) > 0 else "SECURE"
        },
        "vulnerability_details": []
    }

    findings = data.get("repository_findings", [])
    for item in findings:
        file_path = item.get("file")
        
        # Process Logic Findings
        for logic in item.get("logic_findings", []):
            advisory["vulnerability_details"].append({
                "component_path": file_path,
                "vulnerability_type": logic.get("title", "Business Logic Flaw"),
                "cwe_identifier": logic.get("cwe_id", "CWE-639"),
                "severity_level": logic.get("severity", "HIGH"),
                "cvss_score": logic.get("cvss", 7.5),
                "affected_function_or_line": f"Function: {logic.get('function')} at Line {logic.get('line')}",
                "technical_description": logic.get("reasoning", ""),
                "recommended_remediation": "Apply strict authorization checks, decorators, and access control validation before handling object references."
            })

        # Process Taint Findings
        for taint in item.get("taint_findings", []):
            advisory["vulnerability_details"].append({
                "component_path": file_path,
                "vulnerability_type": taint.get("title", "Injection Flaw"),
                "cwe_identifier": taint.get("cwe_id", "CWE-95"),
                "severity_level": taint.get("severity", "CRITICAL"),
                "cvss_score": taint.get("cvss", 9.8),
                "affected_function_or_line": f"Sink: {taint.get('sink_function')} at Line {taint.get('line')}",
                "technical_description": f"Tainted argument '{taint.get('tainted_argument')}' flows directly into unsafe sink without sanitization.",
                "recommended_remediation": taint.get("remediation", "Sanitize and validate all external input.")
            })

    output_file = "cert_in_official_advisory.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(advisory, f, indent=4)

    print(f"[SUCCESS] CERT-In Compliant Advisory generated successfully!")
    print(f"[+] Output saved to: {output_file}")
    return advisory

if __name__ == "__main__":
    generate_cert_in_advisory()
