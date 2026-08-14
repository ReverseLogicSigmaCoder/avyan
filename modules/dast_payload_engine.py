import urllib.request
import urllib.parse
import json
from datetime import datetime, timezone

# Common safe probes for active reflection testing
ACTIVE_PAYLOADS = [
    {"type": "XSS", "payload": "<script>console.log(1337)</script>", "check": "<script>console.log(1337)</script>", "cwe": "CWE-79", "severity": "MEDIUM"},
    {"type": "SQLi", "payload": "' OR '1'='1", "check": "syntax error", "cwe": "CWE-89", "severity": "HIGH"},
    {"type": "PathTraversal", "payload": "../../../../etc/passwd", "check": "root:x:0:0:", "cwe": "CWE-22", "severity": "HIGH"}
]

def audit_url_parameters(target_url):
    """
    Tests live query parameters for input reflection and common injection behaviors.
    """
    parsed_url = urllib.parse.urlparse(target_url)
    params = urllib.parse.parse_qs(parsed_url.query)
    findings = []

    if not params:
        return findings

    print(f"[+] Active Payload Auditor scanning parameters on: {target_url}")

    for param_name in params:
        for test in ACTIVE_PAYLOADS:
            modified_params = params.copy()
            modified_params[param_name] = test["payload"]
            
            # Reconstruct URL with test payload
            encoded_query = urllib.parse.urlencode(modified_params, doseq=True)
            test_url = urllib.parse.urlunparse((
                parsed_url.scheme,
                parsed_url.netloc,
                parsed_url.path,
                parsed_url.params,
                encoded_query,
                parsed_url.fragment
            ))

            try:
                req = urllib.request.Request(test_url, headers={'User-Agent': 'SUDARSHAN-Sovereign-Scanner/1.0'})
                with urllib.request.urlopen(req, timeout=10, timeout=10, timeout=5) as response:
                    res_body = response.read().decode('utf-8', errors='ignore')

                    # Check for payload reflection or error patterns in HTTP response
                    if test["check"].lower() in res_body.lower():
                        findings.append({
                            "vulnerable_parameter": param_name,
                            "poc_url": test_url,
                            "cwe_id": test["cwe"],
                            "title": f"Potential {test['type']} Vulnerability Detected",
                            "severity": test["severity"],
                            "remediation": "Sanitize and encode all HTTP parameter inputs prior to rendering or database querying."
                        })
            except Exception:
                pass

    return findings

if __name__ == "__main__":
    # Test execution on parameter-based target
    sample_target = "https://example.com/search?q=test"
    results = audit_url_parameters(sample_target)
    print("\n=== ACTIVE PAYLOAD AUDIT RESULTS ===")
    print(json.dumps(results, indent=2))
