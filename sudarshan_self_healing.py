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
