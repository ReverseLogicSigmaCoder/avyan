import os
import re
import json
import logging
from datetime import datetime, timezone

# ---------------------------------------------------------
# 1. AUDIT TRAIL & VERIFICATION LOGGER
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
    """Check if target domain is strictly within the allowed disclosure scope."""
    if target_domain in authorized_scope:
        log_audit_event("SCOPE_VALIDATION", f"Target '{target_domain}' is AUTHORIZED.")
        return True
    else:
        log_audit_event("SCOPE_VIOLATION", f"Target '{target_domain}' BLOCKED (Out of Scope).")
        return False


# ---------------------------------------------------------
# 2. EVIDENCE & METADATA SANITIZER (PII REDACTION)
# ---------------------------------------------------------
def sanitize_evidence(raw_text: str) -> str:
    """Redacts sensitive credentials, tokens, and PII from evidence."""
    # Redact Bearer Tokens / Authorization Headers
    sanitized = re.sub(r'(Authorization:\s*Bearer\s+)[A-Za-z0-9\-\._~\+\/]+=*', r'\1[REDACTED_TOKEN]', raw_text, flags=re.IGNORECASE)
    
    # Redact Passwords / API Keys in JSON/Query Params
    sanitized = re.sub(r'("(?:password|api_key|secret|token)"\s*:\s*")[^"]+(")', r'\1[REDACTED_CREDENTIAL]\2', sanitized, flags=re.IGNORECASE)
    
    # Redact Email Addresses
    sanitized = re.sub(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', '[REDACTED_EMAIL]', sanitized)
    
    # Redact IPv4 Addresses
    sanitized = re.sub(r'\b(?:10|172\.(?:1[6-9]|2[0-9]|3[01])|192\.168)\.\d{1,3}\.\d{1,3}\b', '[REDACTED_INTERNAL_IP]', sanitized)
    
    return sanitized


# ---------------------------------------------------------
# 3. REMEDIATION & PATCH ADVISORY DATABASE
# ---------------------------------------------------------
REMEDIATION_DB = {
    "CWE-693": {
        "title": "Protection Mechanism Failure (Missing Security Headers)",
        "remediation": "Configure HTTP Response Headers (HSTS, Content-Security-Policy, X-Frame-Options, X-Content-Type-Options) on the web application firewall or web server configuration.",
        "nginx_snippet": "add_header X-Frame-Options \"DENY\";\nadd_header X-Content-Type-Options \"nosniff\";\nadd_header Strict-Transport-Security \"max-age=31536000; includeSubDomains\" always;",
        "references": [
            "https://owasp.org/www-project-secure-headers/",
            "https://cwe.mitre.org/data/definitions/693.html"
        ]
    },
    "CWE-200": {
        "title": "Exposure of Sensitive Information to an Unauthorized Actor",
        "remediation": "Disable server banner tokens, remove verbose error messages, and sanitize public response headers.",
        "nginx_snippet": "server_tokens off;",
        "references": [
            "https://cwe.mitre.org/data/definitions/200.html",
            "https://cheatsheetseries.owasp.org/cheatsheets/Information_Exposure_Prevention_Cheat_Sheet.html"
        ]
    }
}


# ---------------------------------------------------------
# 4. CERT-In / NCIIPC ADVISORY FORMATTER
# ---------------------------------------------------------
def generate_certin_advisory(target: str, cwe_id: str, cvss_score: float, raw_evidence: str) -> dict:
    """Formats findings into official CERT-In / NCIIPC compliant JSON advisory."""
    
    clean_evidence = sanitize_evidence(raw_evidence)
    
    remediation_info = REMEDIATION_DB.get(cwe_id, {
        "title": "Security Configuration Issue",
        "remediation": "Apply vendor security patches and follow OWASP hardening guidelines.",
        "nginx_snippet": "N/A",
        "references": ["https://cert-in.org.in/"]
    })
    
    if cvss_score >= 9.0:
        severity = "CRITICAL"
    elif cvss_score >= 7.0:
        severity = "HIGH"
    elif cvss_score >= 4.0:
        severity = "MEDIUM"
    else:
        severity = "LOW"

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
            "title": remediation_info["title"],
            "cvss_v31_score": cvss_score,
            "severity": severity
        },
        "sanitized_evidence": clean_evidence,
        "remediation_advisory": {
            "recommended_action": remediation_info["remediation"],
            "configuration_fix_example": remediation_info["nginx_snippet"],
            "official_references": remediation_info["references"]
        }
    }
    
    log_audit_event("ADVISORY_GENERATED", f"Advisory for {target} ({cwe_id}) generated successfully.")
    return advisory


def export_advisory_to_file(advisory_dict: dict, filename: str = "certin_advisory_output.json"):
    """Saves structured advisory to a clean JSON file."""
    with open(filename, "w") as f:
        json.dump(advisory_dict, f, indent=4)
    log_audit_event("FILE_EXPORT", f"Advisory exported to {filename}")
    print(f"[+] CERT-In Advisory saved to: {filename}")


# ---------------------------------------------------------
# LOCAL MODULE TEST RUNNER (PUBLIC GOV DOMAINS SCOPE)
# ---------------------------------------------------------
if __name__ == "__main__":
    # Allowed Scope list with official Public Government Domains
    ALLOWED_SCOPE = [
        "digitalindia.gov.in",
        "mygov.in",
        "ncs.gov.in",
        "mca.gov.in"
    ]
    
    # Target domain selected for passive analysis advisory generation
    target_domain = "digitalindia.gov.in"
    
    if validate_scope(target_domain, ALLOWED_SCOPE):
        # Sample non-destructive HTTP metadata response
        sample_raw_evidence = f"""
        HTTP/1.1 200 OK
        Server: NGINX Public Gateway
        Target: {target_domain}
        Notice: Passive OSINT metadata collection for security compliance check.
        """
        
        advisory = generate_certin_advisory(
            target=target_domain,
            cwe_id="CWE-693",
            cvss_score=5.3,
            raw_evidence=sample_raw_evidence
        )
        
        export_advisory_to_file(advisory, filename=f"certin_advisory_{target_domain}.json")
