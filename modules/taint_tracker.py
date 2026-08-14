import ast
import json
from datetime import datetime, timezone

# 1. Define Known Dangerous Sources & Sinks
TAINT_SOURCES = ["request.args", "request.form", "request.json", "input", "sys.argv", "request.get_json"]
TAINT_SINKS = {
    "eval": {"cwe": "CWE-95", "title": "Direct Code Execution / Eval Injection", "severity": "CRITICAL", "cvss": 9.8},
    "exec": {"cwe": "CWE-95", "title": "Direct Code Execution / Exec Injection", "severity": "CRITICAL", "cvss": 9.8},
    "os.system": {"cwe": "CWE-78", "title": "Command Injection via System Call", "severity": "CRITICAL", "cvss": 9.8},
    "subprocess.Popen": {"cwe": "CWE-78", "title": "Command Injection via Subprocess", "severity": "HIGH", "cvss": 8.8},
    "subprocess.run": {"cwe": "CWE-78", "title": "Command Injection via Subprocess", "severity": "HIGH", "cvss": 8.8},
    "execute": {"cwe": "CWE-89", "title": "Potential SQL Injection / Unsanitized Query", "severity": "HIGH", "cvss": 8.5}
}

class TaintTrackerVisitor(ast.NodeVisitor):
    def __init__(self):
        self.tainted_vars = set()
        self.findings = []

    def visit_Assign(self, node):
        """Track if untrusted input (Source) is assigned to a variable."""
        # Check right hand side of assignment
        rhs_code = ast.unparse(node.value) if hasattr(ast, 'unparse') else ""
        
        is_source = any(source in rhs_code for source in TAINT_SOURCES)
        
        if is_source:
            for target in node.targets:
                if isinstance(target, ast.Name):
                    self.tainted_vars.add(target.id)
                    
        self.generic_visit(node)

    def visit_Call(self, node):
        """Check if a tainted variable reaches a dangerous function (Sink)."""
        func_name = ""
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
        elif isinstance(node.func, ast.Attribute):
            func_name = f"{ast.unparse(node.func.value) if hasattr(ast, 'unparse') else ''}.{node.func.attr}"

        if func_name in TAINT_SINKS or any(sink_key in func_name for sink_key in TAINT_SINKS):
            sink_info = TAINT_SINKS.get(func_name, TAINT_SINKS.get("execute"))
            
            # Check arguments passed to sink
            for arg in node.args:
                arg_code = ast.unparse(arg) if hasattr(ast, 'unparse') else ""
                
                # Check if argument uses a tainted variable
                is_tainted_arg = any(t_var in arg_code for t_var in self.tainted_vars) or any(src in arg_code for src in TAINT_SOURCES)
                
                if is_tainted_arg:
                    self.findings.append({
                        "line": node.lineno,
                        "sink_function": func_name,
                        "tainted_argument": arg_code,
                        "cwe_id": sink_info["cwe"],
                        "title": sink_info["title"],
                        "severity": sink_info["severity"],
                        "cvss": sink_info["cvss"],
                        "remediation": "Sanitize and validate all external input before passing to sensitive system/database calls."
                    })
                    
        self.generic_visit(node)

def run_taint_analysis(code_string):
    try:
        parsed_ast = ast.parse(code_string)
        visitor = TaintTrackerVisitor()
        visitor.visit(parsed_ast)
        return visitor.findings
    except Exception as e:
        print(f"[-] Taint Analysis Error: {e}")
        return []

if __name__ == "__main__":
    # Sample Test Code with Source-to-Sink Vulnerability
    sample_vulnerable_code = """
import os
import sqlite3

def handle_request():
    user_input = request.args.get('cmd') # <--- SOURCE
    os.system(user_input)                # <--- SINK (Command Injection!)

    query = f"SELECT * FROM users WHERE name = '{user_input}'"
    db.execute(query)                    # <--- SINK (SQL Injection!)
"""
    print("[+] Running SUDARSHAN Source-to-Sink Taint Engine...")
    results = run_taint_analysis(sample_vulnerable_code)
    
    report = {
        "engine": "SUDARSHAN Source-to-Sink Taint Tracker",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "taint_violations_found": len(results),
        "details": results
    }
    
    print("\n=== TAINT TRACKING AUDIT RESULTS ===")
    print(json.dumps(report, indent=2))
