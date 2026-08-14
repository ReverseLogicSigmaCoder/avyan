import ast
import json
import os
from datetime import datetime, timezone

class SARATHILogicAuditor(ast.NodeVisitor):
    def __init__(self, filename="target_code.py"):
        self.filename = filename
        self.functions_found = []
        self.routes_found = []
        self.auth_checks = []

    def visit_FunctionDef(self, node):
        """Parse functions and extract logic structure."""
        func_info = {
            "name": node.name,
            "lineno": node.lineno,
            "args": [arg.arg for arg in node.args.args],
            "decorators": [self._get_decorator_name(d) for d in node.decorator_list],
            "has_if_statements": any(isinstance(n, ast.If) for n in ast.walk(node)),
            "calls": [self._get_func_call_name(n) for n in ast.walk(node) if isinstance(n, ast.Call)]
        }
        self.functions_found.append(func_info)
        self.generic_visit(node)

    def _get_decorator_name(self, node):
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Call):
            return self._get_decorator_name(node.func)
        elif isinstance(node, ast.Attribute):
            return node.attr
        return "unknown_decorator"

    def _get_func_call_name(self, node):
        if isinstance(node.func, ast.Name):
            return node.func.id
        elif isinstance(node.func, ast.Attribute):
            return node.func.attr
        return "unknown_call"

def parse_code_to_ast(code_string):
    """Converts raw source code into an AST representation."""
    try:
        parsed_ast = ast.parse(code_string)
        auditor = SARATHILogicAuditor()
        auditor.visit(parsed_ast)
        return auditor.functions_found
    except Exception as e:
        print(f"[-] AST Parsing Error: {e}")
        return []

def sarathi_semantic_logic_analysis(functions_structure):
    """
    Simulates / Calls SARATHI Engine to audit extracted logic flows for Business Logic Flaws.
    """
    findings = []
    
    for func in functions_structure:
        func_name = func["name"]
        args = func["args"]
        decorators = func["decorators"]
        calls = func["calls"]
        
        # 1. Semantic Check for IDOR / Direct Object Access
        if any(param in args for param in ["user_id", "account_id", "id", "order_id"]):
            has_auth_decorator = any(d in ["login_required", "roles_required", "authenticated"] for d in decorators)
            has_auth_check_call = any(c in ["check_perm", "verify_token", "is_admin", "get_current_user"] for c in calls)
            
            if not has_auth_decorator and not has_auth_check_call:
                findings.append({
                    "function": func_name,
                    "line": func["lineno"],
                    "cwe_id": "CWE-639",
                    "title": "Potential Insecure Direct Object Reference (IDOR) / Missing Access Control",
                    "severity": "HIGH",
                    "cvss": 7.5,
                    "reasoning": f"Function '{func_name}' accepts sensitive parameter {args} but lacks authorization decorators or explicit verification calls."
                })

        # 2. Semantic Check for Mass Assignment or Privilege Mutation
        if "update" in func_name.lower() or "role" in func_name.lower():
            if "is_admin" in args or "role" in args:
                findings.append({
                    "function": func_name,
                    "line": func["lineno"],
                    "cwe_id": "CWE-915",
                    "title": "Potential Privilege Mutation / Mass Assignment",
                    "severity": "CRITICAL",
                    "cvss": 8.8,
                    "reasoning": f"Function '{func_name}' directly accepts role/admin parameter in arguments without strict payload filtering."
                })
                
    return findings

def generate_sarathi_logic_report(target_file, code_content):
    print(f"[+] SARATHI AST Auditor scanning: {target_file}")
    ast_structure = parse_code_to_ast(code_content)
    
    print(f"[+] Extracted {len(ast_structure)} functional blocks for logic inspection.")
    logic_findings = sarathi_semantic_logic_analysis(ast_structure)
    
    report = {
        "engine": "SARATHI LLM Semantic Logic Auditor",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "target_file": target_file,
        "functions_analyzed": len(ast_structure),
        "business_logic_findings": logic_findings
    }
    
    return report

if __name__ == "__main__":
    # Test sample with business logic flaw (IDOR)
    sample_code = """
def get_user_profile(user_id):
    # Missing session verification check!
    return db.query(User).filter_by(id=user_id).first()

@login_required
def update_user_email(user_id, new_email):
    verify_token()
    db.update(user_id, new_email)
"""
    results = generate_sarathi_logic_report("sample_app.py", sample_code)
    print("\n=== SARATHI AUDIT RESULTS ===")
    print(json.dumps(results, indent=2))
