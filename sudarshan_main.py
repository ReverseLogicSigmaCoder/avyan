import os
import sys
import argparse
import json
import asyncio
from datetime import datetime, timezone

# Import Advanced SUDARSHAN Sub-Modules safely
try:
    from modules.sarathi_logic_auditor import generate_sarathi_logic_report
    from modules.taint_tracker import run_taint_analysis
    from modules.dast_scanner import run_dast_scan
    from modules.dast_payload_engine import audit_url_parameters
    from modules.enterprise_core import AsynchronousEnterpriseScanner, generate_enterprise_pdf_report
except ImportError as e:
    print(f"[!] Warning: Sub-module import issue: {e}")

def export_advisory_to_file(advisory_dict: dict, filename: str = "sudarshan_master_advisory.json"):
    with open(filename, "w") as f:
        json.dump(advisory_dict, f, indent=4)
    print(f"[+] Master CERT-In Advisory successfully exported to: {filename}")

def execute_sudarshan_master_audit(target_file="sample_app.py", target_url="https://example.com", auth_token=None):
    print("="*60)
    print("   SUDARSHAN SOVEREIGN SHIELD - ENTERPRISE AUDIT CORE       ")
    print("="*60)

    code_content = ""
    if os.path.exists(target_file):
        with open(target_file, "r") as f:
            code_content = f.read()

    # 1. Run LLM AST Logic Auditor (SAST)
    print("\n[+] [1/5] Running SARATHI AST Semantic Logic Auditor...")
    logic_results = generate_sarathi_logic_report(target_file, code_content) if code_content else []

    # 2. Run Source-to-Sink Taint Engine
    print("\n[+] [2/5] Running Source-to-Sink Taint Tracking Engine...")
    taint_results = run_taint_analysis(code_content) if code_content else []

    # 3. Run DAST Live Web Audit
    print("\n[+] [3/5] Running DAST Live Web Audit Engine...")
    dast_results = run_dast_scan(target_url)

    # 4. Run Active Parameter Payload Engine
    print("\n[+] [4/5] Running Active Parameter & Injection Auditor...")
    active_payload_results = audit_url_parameters(target_url)

    # 5. Run Asynchronous High-Speed Enterprise Scanner
    print("\n[+] [5/5] Running High-Speed Concurrent Enterprise Scanner...")
    endpoint_batch = [f"{target_url.rstrip('/')}/api/v1/endpoint_{i}" for i in range(5)]
    async_scanner = AsynchronousEnterpriseScanner(auth_header=auth_token)
    async_results = asyncio.run(async_scanner.scan_concurrent_urls(endpoint_batch))

    # Compile Master Summary
    master_summary = {
        "engine": "SUDARSHAN ENTERPRISE AUTONOMOUS DEFENSIVE ENGINE",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "target_file": target_file if code_content else "N/A",
        "target_url": target_url,
        "auth_enabled": bool(auth_token),
        "logic_audit_summary": logic_results,
        "taint_violations": taint_results,
        "dast_audit_summary": dast_results,
        "active_parameter_findings": active_payload_results,
        "enterprise_async_batch_count": len(async_results)
    }

    # Export Final JSON & PDF Executive Summary
    export_advisory_to_file(master_summary, "sudarshan_master_advisory.json")
    generate_enterprise_pdf_report(master_summary, "SUDARSHAN_Executive_Security_Report.pdf")

    print("\n[SUCCESS] Enterprise Master Scan Complete! PDF Report & JSON Advisory Ready.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SUDARSHAN Sovereign Shield Enterprise Core Engine")
    parser.add_argument("--url", type=str, default="https://example.com", help="Target URL for live DAST scanning")
    parser.add_argument("--file", type=str, default="sample_app.py", help="Target Python source code for SAST scanning")
    parser.add_argument("--auth", type=str, default=None, help="Bearer Token or Session Auth Header for Enterprise scans")
    args = parser.parse_args()

    execute_sudarshan_master_audit(target_file=args.file, target_url=args.url, auth_token=args.auth)

