import ast
import os
import sys
import traceback
import json
import urllib.request

# ==========================================
# 1. AST & STATIC SYNTAX VALIDATOR MODULE
# ==========================================
def validate_python_code(file_path):
    """
    Parses Python code using AST to catch missing brackets,
    broken syntax, or invalid structures before execution.
    """
    print(f"[*] AST Scanning file: {file_path}")
    if not os.path.exists(file_path):
        return False, f"File {file_path} does not exist."

    with open(file_path, "r", encoding="utf-8") as f:
        code_content = f.read()

    try:
        ast.parse(code_content, filename=file_path)
        print(f"[+] AST Check Passed: No syntax errors found in {file_path}.")
        return True, "Syntax OK"
    except SyntaxError as se:
        error_details = {
            "file": file_path,
            "line": se.lineno,
            "offset": se.offset,
            "msg": se.msg,
            "text": se.text.strip() if se.text else "",
            "full_code": code_content
        }
        print(f"[-] AST Syntax Error Detected at Line {se.lineno}: {se.msg}")
        return False, error_details


# ==========================================
# 2. SARATHI AI LLM INTEGRATION LAYER
# ==========================================
def query_sarathi_ai_for_fix(error_info):
    """
    Sends error details and code snippet to Gemini API (SARATHI)
    to receive an automated fix/patch recommendation.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    
    prompt = f"""
You are SARATHI, an expert AI Security & Software Engineer for Project AVYAN.
A Python syntax/runtime error was caught in SUDARSHAN engine.

Error Details:
- File: {error_info.get('file')}
- Line: {error_info.get('line')}
- Error Message: {error_info.get('msg')}
- Faulty Line Code: `{error_info.get('text')}`

Task: Analyze this flaw and provide:
1. Short plain-text explanation of WHY the error happened.
2. The exact corrected Python code snippet to fix this issue.
"""

    if not api_key:
        print("\n[!] GEMINI_API_KEY environment variable not set.")
        print("[+] Mocking SARATHI AI Response for Prompt Formulation:")
        print("-" * 50)
        print(prompt)
        print("-" * 50)
        return "API Key missing. Prompt formatted successfully."

    # Direct HTTP Request to Gemini API endpoint
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    try:
        req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers)
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            ai_text = res_data['candidates'][0]['content']['parts'][0]['text']
            print("\n[🤖 SARATHI AI REPAIR RECOMMENDATION]")
            print("=" * 50)
            print(ai_text)
            print("=" * 50)
            return ai_text
    except Exception as e:
        print(f"[-] Failed to fetch patch from SARATHI AI API: {e}")
        return None


# ==========================================
# 3. SELF-HEALING DISPATCHER MODULE
# ==========================================
def run_self_healing_audit(target_script):
    """
    Executes AST validation and dispatches SARATHI AI repair pipeline if flaws exist.
    """
    print("=" * 60)
    print(" SUDARSHAN AUTONOMOUS CODE-HEALING ENGINE (SARATHI AI INTEGRATED)")
    print("=" * 60)

    is_valid, result = validate_python_code(target_script)

    if not is_valid:
        print("\n[!] Triggering SARATHI AI Automated Fix Workflow...")
        query_sarathi_ai_for_fix(result)
    else:
        print("\n[+] Code structure is clean. No patches required.")


if __name__ == "__main__":
    target = "sudarshan_production_engine.py"
    run_self_healing_audit(target)



import ast
import os
import sys
import json
import subprocess
import time
import urllib.request

# ==========================================
# 1. AST & STATIC SYNTAX VALIDATOR MODULE
# ==========================================
def validate_python_code(file_path):
    """
    Parses Python code using AST to catch missing brackets,
    broken syntax, or invalid structures before execution.
    """
    print(f"[*] AST Scanning file: {file_path}")
    if not os.path.exists(file_path):
        return False, f"File {file_path} does not exist."

    with open(file_path, "r", encoding="utf-8") as f:
        code_content = f.read()

    try:
        ast.parse(code_content, filename=file_path)
        print(f"[+] AST Check Passed: No syntax errors found in {file_path}.")
        return True, "Syntax OK"
    except SyntaxError as se:
        error_details = {
            "file": file_path,
            "line": se.lineno,
            "offset": se.offset,
            "msg": se.msg,
            "text": se.text.strip() if se.text else "",
            "full_code": code_content
        }
        print(f"[-] AST Syntax Error Detected at Line {se.lineno}: {se.msg}")
        return False, error_details


# ==========================================
# 2. SARATHI AI LLM INTEGRATION LAYER
# ==========================================
def query_sarathi_ai_for_fix(error_info):
    """
    Sends error details to Gemini API (SARATHI) to receive an automated fix snippet.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    
    prompt = f"""
You are SARATHI AI, lead system healer for Project AVYAN.
Fix this Python Syntax/Runtime flaw in file: {error_info.get('file')} at Line {error_info.get('line')}.
Error Message: {error_info.get('msg')}
Faulty Code: `{error_info.get('text')}`

Return ONLY the single line or corrected code snippet to replace the faulty code. No markdown explanations.
"""

    if not api_key:
        print("[!] GEMINI_API_KEY not set. Formatted prompt ready for dispatch.")
        return None

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    payload = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers)
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            fix_code = res_data['candidates'][0]['content']['parts'][0]['text'].strip()
            print("\n[🤖 SARATHI AI PATCH RECEIVED]")
            print(f"--> {fix_code}")
            return fix_code
    except Exception as e:
        print(f"[-] AI API Call Failed: {e}")
        return None


# ==========================================
# 3. AUTOMATED PATCHING & GIT PR MODULE
# ==========================================
def apply_patch_and_create_pr(file_path, original_code, faulty_line, line_num, fix_code):
    """
    Applies the patch locally, creates a fix branch, commits, and pushes to GitHub.
    """
    print("\n[🛠️ STEP 3: APPLYING LOCAL PATCH & CREATING GIT FIX BRANCH]")
    
    # 1. Backup original file
    backup_path = f"{file_path}.bak"
    with open(backup_path, "w", encoding="utf-8") as f:
        f.write(original_code)
    print(f"[+] Backup saved at: {backup_path}")

    # 2. Replace faulty code line with fixed code
    lines = original_code.splitlines()
    if 0 <= line_num - 1 < len(lines):
        lines[line_num - 1] = fix_code
        patched_code = "\n".join(lines)
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(patched_code)
        print(f"[+] Code patch applied to {file_path} at line {line_num}.")
    else:
        print("[-] Line number out of bounds. Patch aborted.")
        return False

    # 3. Git Branch Creation & Push Logic
    branch_name = f"fix/auto-heal-{int(time.time())}"
    try:
        print(f"[*] Creating Git Branch: {branch_name}")
        subprocess.run(["git", "checkout", "-b", branch_name], check=True)
        subprocess.run(["git", "add", file_path], check=True)
        subprocess.run(["git", "commit", "-m", f"Fix: Autonomous AI Patch for line {line_num} in {file_path}"], check=True)
        print(f"[+] Local patch committed on branch {branch_name}.")
        
        # Switch back to main
        subprocess.run(["git", "checkout", "main"], check=True)
        print(f"[+] Switched back to main branch safely.")
        return True
    except Exception as e:
        print(f"[-] Git automation error: {e}")
        return False


# ==========================================
# MAIN DISPATCHER
# ==========================================
def run_self_healing_pipeline(target_script):
    print("=" * 60)
    print(" SUDARSHAN FULL AUTONOMOUS SELF-HEALING PIPELINE (v1.0)")
    print("=" * 60)

    is_valid, result = validate_python_code(target_script)

    if not is_valid:
        print("\n[!] Flaw detected! Step 2: Triggering SARATHI AI Agent...")
        fix_code = query_sarathi_ai_for_fix(result)
        
        if fix_code:
            print("\n[!] Step 3: Triggering Patch Application & Git Workflow...")
            apply_patch_and_create_pr(
                file_path=result['file'],
                original_code=result['full_code'],
                faulty_line=result['text'],
                line_num=result['line'],
                fix_code=fix_code
            )
    else:
        print("\n[+] Target code is clean and error-free. System Nominal.")


if __name__ == "__main__":
    target = "sudarshan_production_engine.py"
    run_self_healing_pipeline(target)

