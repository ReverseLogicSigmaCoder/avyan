import shlex
import subprocess
from urllib.parse import urlparse

def run_diagnostic_ping(target_domain: str) -> str:
    cleaned = target_domain.strip().lower()
    if "://" in cleaned:
        cleaned = urlparse(cleaned).netloc
    safe_target = shlex.quote(cleaned)
    try:
        result = subprocess.run(["ping", "-c", "1", safe_target], capture_output=True, text=True, timeout=5, check=False)
        return result.stdout if result.returncode == 0 else "Host unreachable."
    except Exception as e:
        return f"Error: {e}"
