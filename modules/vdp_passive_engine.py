import os
import json
import urllib.request
import ssl
from datetime import datetime

class PassiveScanner:
    def __init__(self, target_domain):
        self.target = target_domain.replace("http://", "").replace("https://", "").strip("/")
        self.report = {
            "target": self.target,
            "timestamp": str(datetime.now()),
            "security_headers": {},
            "ssl_info": {},
            "vulnerabilities": [],
            "remediation": []
        }

    def check_security_headers(self):
        """Passive header inspection (No active payloads)"""
        url = f"https://{self.target}"
        headers_to_check = [
            "Strict-Transport-Security",
            "Content-Security-Policy",
            "X-Frame-Options",
            "X-Content-Type-Options"
        ]
        
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'SUDARSHAN-Sovereign-Auditor/1.0'})
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE

            with urllib.request.urlopen(req, context=ctx, timeout=10) as response:
                res_headers = response.info()
                for header in headers_to_check:
                    if header in res_headers:
                        self.report["security_headers"][header] = "PRESENT ✅"
                    else:
                        self.report["security_headers"][header] = "MISSING ❌"
                        self.report["vulnerabilities"].append({
                            "title": f"Missing Security Header: {header}",
                            "cwe": "CWE-693: Protection Mechanism Failure",
                            "impact": "Increases risk of Clickjacking/MIME-sniffing attacks.",
                            "remediation": f"Configure {header} in web server response headers."
                        })
        except Exception as e:
            self.report["errors"] = str(e)

    def generate_certin_report_format(self):
        """Generates structured output ready for VDP submission"""
        self.check_security_headers()
        return self.report

def run_passive_audit(target):
    scanner = PassiveScanner(target)
    return scanner.generate_certin_report_format()
