import urllib.request
import ssl
import json

class DASTAuditEngine:
    def audit_endpoint(self, target_url):
        results = {"url": target_url, "missing_headers": [], "vulnerabilities": []}
        try:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            
            req = urllib.request.Request(
                target_url, 
                headers={'User-Agent': 'SUDARSHAN-Sovereign-Audit-Engine/1.0'}
            )
            with urllib.request.urlopen(req, context=ctx, timeout=5) as response:
                headers = dict(response.info())
                
                # Check Essential Security Headers
                security_headers = [
                    "Strict-Transport-Security",
                    "Content-Security-Policy",
                    "X-Frame-Options",
                    "X-Content-Type-Options"
                ]
                for header in security_headers:
                    if header.lower() not in [h.lower() for h in headers.keys()]:
                        results["missing_headers"].append(header)
                        results["vulnerabilities"].append({
                            "issue": f"Missing Security Header: {header}",
                            "severity": "Medium"
                        })
                        
                results["http_status"] = response.getcode()
                results["server_banner"] = headers.get("Server", "Hidden")
        except Exception as e:
            results["error"] = str(e)
            
        return results

if __name__ == "__main__":
    engine = DASTAuditEngine()
    print(engine.audit_endpoint("https://example.com"))
      
