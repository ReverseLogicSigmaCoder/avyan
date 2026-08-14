import os
import sys

# Ensure root directory is in python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import subprocess
import json
import shutil
from datetime import datetime, timezone

try:
    from modules.sarathi_logic_auditor import generate_sarathi_logic_report
    from modules.taint_tracker import run_taint_analysis
except ImportError as e:
    print(f"[!] Import error: {e}")

TEMP_DIR = "temp_repo_scan"

# Paths to strictly IGNORE to eliminate false positives
IGNORE_DIRS = {'test', 'tests', 'testing', 'docs', 'examples', 'mock', 'fixtures', 'venv', 'site-packages'}
IGNORE_FILES_PREFIX = ('test_', 'mock_', 'conftest')

def is_production_code(filepath):
    """Filters out non-production code paths like test suites and docs."""
    parts = filepath.lower().split(os.sep)
    for part in parts:
        if part in IGNORE_DIRS:
            return False
    filename = os.path.basename(filepath).lower()
    if filename.startswith(IGNORE_FILES_PREFIX):
        return False
    return True

def clone_public_repo(repo_url):
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)
        
    print(f"[+] [PRODUCTION SAST] Downloading public repository: {repo_url}...")
    try:
        subprocess.run(["git", "clone", "--depth", "1", repo_url, TEMP_DIR], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except Exception as e:
        print(f"[!] Error cloning repository: {e}")
        return False

def scan_cloned_repository(repo_url):
    if not clone_public_repo(repo_url):
        return None

    all_findings = []
    python_files_count = 0
    ignored_files_count = 0

    print("[+] [PRODUCTION SAST] Filtering out test suites & auditing production codebase...")
    
    for root, dirs, files in os.walk(TEMP_DIR):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                rel_path = os.path.relpath(filepath, TEMP_DIR)
                
                # Apply Production Code Filter
                if not is_production_code(rel_path):
                    ignored_files_count += 1
                    continue

                python_files_count += 1
                try:
                    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                        
                    logic_issues = generate_sarathi_logic_report(rel_path, content)
                    taint_issues = run_taint_analysis(content)

                    if logic_issues.get("business_logic_findings") or taint_issues:
                        all_findings.append({
                            "file": rel_path,
                            "logic_findings": logic_issues.get("business_logic_findings", []),
                            "taint_findings": taint_issues
                        })
                except Exception:
                    pass

    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)

    report = {
        "engine": "SUDARSHAN Production-Grade SAST Engine",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "repository_scanned": repo_url,
        "production_files_analyzed": python_files_count,
        "test_files_ignored": ignored_files_count,
        "actionable_vulnerabilities_count": len(all_findings),
        "repository_findings": all_findings
    }

    output_filename = "github_sast_audit_report.json"
    with open(output_filename, "w") as f:
        json.dump(report, f, indent=4)

    print(f"\n[SUCCESS] Production SAST Audit Complete!")
    print(f"[+] Analyzed Production Files: {python_files_count} (Ignored {ignored_files_count} test files)")
    print(f"[+] Actionable Vulnerable Files: {len(all_findings)}")
    print(f"[+] Saved Clean Report To: {output_filename}")
    return report

if __name__ == "__main__":
    target_input = input("Enter Public GitHub Repo URL: ").strip()
    if target_input and "github.com" in target_input.lower():
        scan_cloned_repository(target_input)
    else:
        print("[!] Invalid or empty GitHub repository URL.")
