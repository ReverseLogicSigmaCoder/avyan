import requests
import socket
from urllib.parse import urlparse

BLOCKED_SUBNETS = ["127.0.0.1", "localhost", "169.254.169.254", "0.0.0.0"]

def safe_scanner_get(target_url, timeout=10, headers=None, allow_redirects=False):
    parsed = urlparse(target_url)
    hostname = parsed.hostname or ""
    
    if hostname.lower() in BLOCKED_SUBNETS:
        raise ValueError("[SSRF_GUARD] Internal infrastructure probing blocked.")
        
    return requests.get(
        target_url,
        timeout=timeout,
        headers=headers or {},
        allow_redirects=allow_redirects
    )
