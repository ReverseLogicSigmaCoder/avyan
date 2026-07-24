import os
import re
import json
import logging
import urllib.request
import urllib.error
from datetime import datetime, timezone

# ---------------------------------------------------------
# 1. AUDIT TRAIL & LOGGING
# ---------------------------------------------------------
logging.basicConfig(
    filename="sudarshan_audit_trail.log",
    level=logging.INFO,
    format="%(asctime)s UTC - [AUDIT] - %(message)s"
)

def log_audit_event(event_type: str, details: str):
    timestamp = datetime.now(timezone.utc).isoformat()
    log_message = f"[{event_type.upper()}] {details}"
    logging.info(log_message)
    print(f"[{timestamp}] {log_message}")


def validate_scope(target_domain: str, authorized_scope: list) -> bool:
    if target_domain in authorized_scope:
        log_audit_event("SCOPE_VALIDATION", f"Target '{target_domain}' is AUTHORIZED.")
        return True
    else:
        log_audit_event("SCOPE_VIOLATION", f"Target '{target_domain}' BLOCKED.")
        return False


# ---------------------------------------------------------
# 2. REAL LIVE PASSIVE HEADER ANALYZER (HTTP OSINT)
# ---------------------------------------------------------
RECOMMENDED_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options"
]

def analyze_live_passive_headers(target_domain: str) -> dict:
    """Fetch public headers without sending malicious payloads (Passive OSINT)."""
    url = f"https://{target_domain}"
    log_audit_event("PASSIVE_SCAN_START", f"Fetching public headers for {url}")
    
    missing_headers = []
    headers_received = {}
    
    try:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        # Timeout set to 10 seconds to avoid hung requests
        with urllib.request.urlopen(req, timeout=10) as response:
            response_headers = response.info()
            for header_name in response_headers.keys():
                headers_received[header_name] = response_headers[header_name]

            # Check for missing standard security headers
            for sec_header in RECOMMENDED_HEADERS:
                if sec_header.lower() not in [h.lower() for h in response_headers.keys()]:
                    missing_headers.append(sec_header)
                    
    except urllib.error.URLError as e:
        log_audit_event("PASSIVE_SCAN_ERROR", f"Network error for {target_domain}: {str(e)}")
        return {"status": "ERROR", "reason": str(e)}
    except Exception as e:
        log_audit_event("PASSIVE_SCAN_ERROR", f"Execution error for {target_domain}: {str(e)}")
        return {"status": "ERROR", "reason": str(e)}

    return {
        "status": "SUCCESS",
        "domain": target_domain,
        "missing_headers": missing_headers,
        "raw_headers": headers_received
    }


# ---------------------------------------------------------
# 3. EVIDENCE SANITIZER (PII REDACTION)
# ---------------------------------------------------------
def sanitize_evidence(raw_text: str) -> str:
    sanitized = re.sub(r'(Authorization:\s*Bearer\s+)[A-Za-z0-9\-\._~\+\/]+=*', r'\1[REDACTED_TOKEN]', raw_text, flags=re.IGNORECASE)
    sanitized = re.sub(r'("(?:password|api_key|secret|token)"\s*:\s*")[^"]+(")', r'\1[REDACTED_CREDENTIAL]\2', sanitized, flags=re.IGNORECASE)
    sanitized = re.sub(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', '[REDACTED_EMAIL]', sanitized)
    sanitized = re.sub(r'\b(?:10|172\.(?:1[6-9]|2[0-9]|3[01])|192\.168)\.\d{1,3}\.\d{1,3}\b', '[REDACTED_INTERNAL_IP]', sanitized)
    return sanitized


# ---------------------------------------------------------
# 4. CERT-In / NCIIPC ADVISORY GENERATOR
# ---------------------------------------------------------
def generate_certin_advisory(target: str, scan_result: dict) -> dict:
    if scan_result.get("status") != "SUCCESS":
        return {"error": "Scan failed, cannot generate advisory"}

    missing = scan_result.get("missing_headers", [])
    raw_headers = json.dumps(scan_result.get("raw_headers", {}), indent=2)
    clean_evidence = sanitize_evidence(raw_headers)

    cwe_id = "CWE-693"
    title = "Protection Mechanism Failure (Missing HTTP Security Headers)"
    
    if len(missing) > 0:
        cvss_score = 5.3
        severity = "MEDIUM"
        findings_summary = f"The following security headers are missing: {', '.join(missing)}"
    else:
        cvss_score = 0.0
        severity = "INFORMATIONAL"
        findings_summary = "All basic HTTP security headers are present."

    advisory = {
        "advisory_meta": {
            "generator": "SUDARSHAN Sovereign Shield Engine",
            "timestamp_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "compliance_standard": "CERT-In / NCIIPC Vulnerability Disclosure Format"
        },
        "target_information": {
            "domain": target,
            "scope_verification": "VERIFIED_IN_SCOPE"
        },
        "vulnerability_details": {
            "cwe_id": cwe_id,
            "title": title,
            "cvss_v31_score": cvss_score,
            "severity": severity,
            "summary": findings_summary
        },
        "sanitized_live_evidence": clean_evidence,
        "remediation_advisory": {
            "recommended_action": "Configure HTTP response security headers on server/WAF.",
            "nginx_snippet": "add_header X-Frame-Options \"DENY\";\nadd_header X-Content-Type-Options \"nosniff\";\nadd_header Strict-Transport-Security \"max-age=31536000; includeSubDomains\" always;",
            "official_references": [
                "https://owasp.org/www-project-secure-headers/",
                "https://cwe.mitre.org/data/definitions/693.html"
            ]
        }
    }
    
    log_audit_event("ADVISORY_GENERATED", f"Advisory for {target} generated.")
    return advisory


def export_advisory_to_file(advisory_dict: dict, filename: str):
    with open(filename, "w") as f:
        json.dump(advisory_dict, f, indent=4)
    log_audit_event("FILE_EXPORT", f"Advisory exported to {filename}")
    print(f"[+] Live CERT-In Advisory saved to: {filename}")


# ---------------------------------------------------------
# EXECUTION RUNNER
# ---------------------------------------------------------
if __name__ == "__main__":
    ALLOWED_SCOPE = [
        "digitalindia.gov.in",
        "mygov.in",
        "ncs.gov.in",
        "mca.gov.in"
    ]
    
    target_domain = "digitalindia.gov.in"
    
    if validate_scope(target_domain, ALLOWED_SCOPE):
        # Perform real passive header fetch
        scan_result = analyze_live_passive_headers(target_domain)
        
        if scan_result.get("status") == "SUCCESS":
            advisory = generate_certin_advisory(target_domain, scan_result)
            export_advisory_to_file(advisory, filename=f"certin_advisory_{target_domain}.json")
        else:
            print(f"[-] Scan could not be completed: {scan_result.get('reason')}")
