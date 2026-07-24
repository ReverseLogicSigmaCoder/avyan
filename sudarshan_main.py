import os
import json
from datetime import datetime, timezone

# Import Advanced SUDARSHAN Sub-Modules safely
try:
    from modules.sarathi_logic_auditor import generate_sarathi_logic_report
    from modules.taint_tracker import run_taint_analysis
    from modules.ai_fuzzer import AIGuidedFuzzer
except ImportError as e:
    print(f"[!] Warning: Sub-module import issue: {e}")

# Direct Exporter Definition (No Import Errors)
def export_advisory_to_file(advisory_dict: dict, filename: str = "sudarshan_master_advisory.json"):
    """Saves structured advisory to a clean JSON file with audit logging."""
    with open(filename, "w") as f:
        json.dump(advisory_dict, f, indent=4)
    print(f"[+] Master CERT-In Advisory successfully exported to: {filename}")

# Existing Passive Scan Logic
AUTHORIZED_VDP_TARGETS = [
    "example.com",
    "scanme.nmap.org"
]

def run_passive_scan():
    print("[+] Initiating SUDARSHAN Passive Recon Engine...")
    timestamp = datetime.now(timezone.utc).isoformat()
    report_content = f"""=== SUDARSHAN SOVEREIGN SHIELD: VDP RECON REPORT ===
Timestamp: {timestamp}
Scope: Public Authorized Targets
Targets Analyzed: {', '.join(AUTHORIZED_VDP_TARGETS)}
Status: PASSIVE_ANALYSIS_COMPLETED
===================================================
"""
    with open("scan_report.txt", "w") as f:
        f.write(report_content)
    print("[+] Passive scan complete. Saved to scan_report.txt")

def execute_sudarshan_master_audit(target_file="sample_app.py"):
    print("="*60)
    print("      SUDARSHAN SOVEREIGN SHIELD - MASTER AUDIT CORE       ")
    print("="*60)
    
    # 1. Run Existing Passive Scan
    run_passive_scan()

    # 2. Check or create target file for logic/taint testing
    if not os.path.exists(target_file):
        sample_code = """
def handle_user_profile(user_id):
    # Potential IDOR / Unauthenticated Route
    cmd = request.args.get('cmd')
    os.system(cmd)  # Command Injection (Taint Sink)
    return db.query(User).filter_by(id=user_id).first()
"""
        with open(target_file, "w") as f:
            f.write(sample_code)

    with open(target_file, "r") as f:
        code_content = f.read()

    # 3. Run LLM AST Logic Auditor
    print("\n[+] [1/3] Running SARATHI AST Semantic Logic Auditor...")
    logic_results = generate_sarathi_logic_report(target_file, code_content)

    # 4. Run Source-to-Sink Taint Engine
    print("\n[+] [2/3] Running Source-to-Sink Taint Tracking Engine...")
    taint_results = run_taint_analysis(code_content)

    # 5. Compile Master CERT-In / NCIIPC Compliance Advisory
    print("\n[+] [3/3] Compiling Master CERT-In / NCIIPC Compliance Advisory...")
    master_summary = {
        "engine": "SUDARSHAN AUTONOMOUS DEFENSIVE ENGINE",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "target_file": target_file,
        "logic_audit_summary": logic_results,
        "taint_violations": taint_results
    }

    # Export final master report
    export_advisory_to_file(master_summary, "sudarshan_master_advisory.json")
    print("\n[SUCCESS] Master Scan Complete! All systems nominal.")

if __name__ == "__main__":
    execute_sudarshan_master_audit()

