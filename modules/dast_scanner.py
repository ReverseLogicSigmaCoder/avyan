import urllib.request
import urllib.error
import json
from datetime import datetime, timezone

# Common security headers to check
SECURITY_HEADERS = {
    "Strict-Transport-Security": {"cwe": "CWE-523", "title": "Missing HSTS Header", "severity": "LOW", "cvss": 3.7},
    "X-Frame-Options": {"cwe": "CWE-1021", "title": "Missing Clickjacking Protection (X-Frame-Options)", "severity": "MEDIUM", "cvss": 4.3},
    "Content-Security-Policy": {"cwe": "CWE-693", "title": "Missing Content Security Policy (CSP)", "severity": "MEDIUM", "cvss": 5.4},
    "X-Content-Type-Options": {"cwe": "CWE-693", "title": "Missing MIME-Sniffing Protection (X-Content-Type-Options)", "severity": "LOW", "cvss": 3.1},
    "Access-Control-Allow-Origin": {"cwe": "CWE-942", "title": "Permissive CORS Configuration Check Needed", "severity": "LOW", "cvss": 3.7}
}

# Sensitive sensitive path endpoints for configuration audits
SENSITIVE_PATHS = ["/.env", "/.git/HEAD", "/robots.txt"]

def scan_security_headers(target_url):
    """Scans HTTP headers of a given authorized target URL."""
    findings = []
    try:
        req = urllib.request.Request(target_url, headers={'User-Agent': 'SUDARSHAN-Sovereign-Scanner/1.0'})
        with urllib.request.urlopen(req, timeout=10, timeout=10, timeout=5) as response:
            headers = {k.title(): v for k, v in response.headers.items()}
            
            for header, info in SECURITY_HEADERS.items():
                if header not in headers:
                    findings.append({
                        "header_missing": header,
                        "cwe_id": info["cwe"],
                        "title": info["title"],
                        "severity": info["severity"],
                        "cvss": info["cvss"],
                        "remediation": f"Configure '{header}' in web server response headers."
                    })
    except Exception as e:
        print(f"[!] Header Scan Warning for {target_url}: {e}")
    return findings

def scan_exposed_endpoints(target_url):
    """Checks for standard misconfiguration paths on authorized targets."""
    findings = []
    base_url = target_url.rstrip("/")
    
    for path in SENSITIVE_PATHS:
        full_url = base_url + path
        try:
            req = urllib.request.Request(full_url, headers={'User-Agent': 'SUDARSHAN-Sovereign-Scanner/1.0'})
            with urllib.request.urlopen(req, timeout=10, timeout=10, timeout=4) as response:
                if response.status == 200:
                    findings.append({
                        "endpoint": full_url,
                        "status_code": 200,
                        "cwe_id": "CWE-538",
                        "title": "Potentially Exposed Sensitive Path / File",
                        "severity": "HIGH" if ".env" in path or ".git" in path else "INFO",
                        "cvss": 7.5 if ".env" in path or ".git" in path else 0.0,
                        "remediation": f"Restrict public access to '{path}' via web server access control rules."
                    })
        except urllib.error.HTTPError as e:
            pass  # Expected 403 / 404
        except Exception:
            pass
            
    return findings

def run_dast_scan(target_url):
    print(f"[+] DAST Engine scanning live target: {target_url}")
    header_issues = scan_security_headers(target_url)
    endpoint_issues = scan_exposed_endpoints(target_url)
    
    return {
        "engine": "SUDARSHAN Dynamic Web Audit Engine (DAST)",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "target_url": target_url,
        "missing_headers_count": len(header_issues),
        "header_findings": header_issues,
        "exposed_endpoints_count": len(endpoint_issues),
        "endpoint_findings": endpoint_issues
    }

if __name__ == "__main__":
    # Test scan on authorized public domain
    test_target = "https://example.com"
    results = run_dast_scan(test_target)
    print("\n=== DAST SCAN RESULTS ===")
    print(json.dumps(results, indent=2))
