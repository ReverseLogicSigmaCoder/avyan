import ast
import os
import sys
import traceback

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
            "text": se.text.strip() if se.text else ""
        }
        print(f"[-] AST Syntax Error Detected at Line {se.lineno}: {se.msg}")
        return False, error_details


# ==========================================
# 2. LLM PROMPT GENERATOR (SARATHI AI LAYER)
# ==========================================
def generate_ai_repair_prompt(error_info):
    """
    Formats the captured syntax/runtime flaw into a structured 
    AI prompt for automated patch generation.
    """
    prompt = f"""
    [SARATHI AI CODE HEALER INSTRUCTION]
    Target File: {error_info.get('file')}
    Line Number: {error_info.get('line')}
    Error Message: {error_info.get('msg')}
    Faulty Code Line: `{error_info.get('text')}`

    Task: Provide the corrected Python code snippet to fix this error permanently.
    """
    return prompt


# ==========================================
# 3. SELF-HEALING DISPATCHER MODULE
# ==========================================
def run_self_healing_audit(target_script):
    """
    Executes AST validation and dispatches repair pipeline if flaws exist.
    """
    print("=" * 60)
    print(" SUDARSHAN AUTONOMOUS CODE-HEALING ENGINE v1.0")
    print("=" * 60)

    is_valid, result = validate_python_code(target_script)

    if not is_valid:
        print("\n[!] Triggering SARATHI AI Automated Fix Workflow...")
        ai_prompt = generate_ai_repair_prompt(result)
        
        print("\n[+] Generated AI Repair Payload:")
        print("-" * 40)
        print(ai_prompt.strip())
        print("-" * 40)
        print("[+] Status: Ready to dispatch to AI API / GitHub PR Pipeline.")
    else:
        print("\n[+] Code structure is clean. No patches required.")


if __name__ == "__main__":
    # Test audit on main production engine
    target = "sudarshan_production_engine.py"
    run_self_healing_audit(target)


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

