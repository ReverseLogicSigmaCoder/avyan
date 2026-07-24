import os
import sys
import argparse
import json
from datetime import datetime, timezone

# Import Advanced SUDARSHAN Sub-Modules safely
try:
    from modules.sarathi_logic_auditor import generate_sarathi_logic_report
    from modules.taint_tracker import run_taint_analysis
    from modules.ai_fuzzer import AIGuidedFuzzer
    from modules.dast_scanner import run_dast_scan
    from modules.dast_payload_engine import audit_url_parameters
except ImportError as e:
    print(f"[!] Warning: Sub-module import issue: {e}")

def export_advisory_to_file(advisory_dict: dict, filename: str = "sudarshan_master_advisory.json"):
    with open(filename, "w") as f:
        json.dump(advisory_dict, f, indent=4)
    print(f"[+] Master CERT-In Advisory successfully exported to: {filename}")

def execute_sudarshan_master_audit(target_file="sample_app.py", target_url="https://example.com"):
    print("="*60)
    print("      SUDARSHAN SOVEREIGN SHIELD - MASTER AUDIT CORE       ")
    print("="*60)

    code_content = ""
    if os.path.exists(target_file):
        with open(target_file, "r") as f:
            code_content = f.read()

    # 1. Run LLM AST Logic Auditor
    print("\n[+] [1/4] Running SARATHI AST Semantic Logic Auditor...")
    logic_results = generate_sarathi_logic_report(target_file, code_content) if code_content else []

    # 2. Run Source-to-Sink Taint Engine
    print("\n[+] [2/4] Running Source-to-Sink Taint Tracking Engine...")
    taint_results = run_taint_analysis(code_content) if code_content else []

    # 3. Run DAST Live Web Audit
    print("\n[+] [3/4] Running DAST Live Web Audit Engine...")
    dast_results = run_dast_scan(target_url)

    # 4. Run Active Parameter Payload Engine
    print("\n[+] [4/4] Running Active Parameter & Injection Auditor...")
    active_payload_results = audit_url_parameters(target_url)

    # Compile Master Summary
    master_summary = {
        "engine": "SUDARSHAN AUTONOMOUS DEFENSIVE ENGINE",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "target_file": target_file if code_content else "N/A",
        "target_url": target_url,
        "logic_audit_summary": logic_results,
        "taint_violations": taint_results,
        "dast_audit_summary": dast_results,
        "active_parameter_findings": active_payload_results
    }

    export_advisory_to_file(master_summary, "sudarshan_master_advisory.json")
    print("\n[SUCCESS] Master Scan Complete! System is fully operational.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SUDARSHAN Sovereign Shield Core Engine")
    parser.add_argument("--url", type=str, default="https://example.com", help="Target URL for live DAST scanning")
    parser.add_argument("--file", type=str, default="sample_app.py", help="Target Python source code for SAST scanning")
    args = parser.parse_args()

    execute_sudarshan_master_audit(target_file=args.file, target_url=args.url)
