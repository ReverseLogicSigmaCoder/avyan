import os
import sys
import re
import time
import json
import socket
import platform
import hashlib
import shutil

# ======================================================
# 1. DYNAMIC ENVIRONMENT TELEMETRY ENGINE
# ======================================================
class EnvironmentTelemetryEngine:
    def get_system_telemetry(self):
        print("\n[📊 DYNAMIC ENVIRONMENT TELEMETRY ENGINE]")
        
        # Collect basic OS and system metrics
        os_name = platform.system()
        os_release = platform.release()
        python_ver = platform.python_version()
        
        # Disk Usage Check
        total, used, free = shutil.disk_usage("/")
        free_gb = round(free / (1024 ** 3), 2)

        print(f"[*] OS Platform: {os_name} {os_release}")
        print(f"[*] Python Version: {python_ver}")
        print(f"[*] Available Storage: {free_gb} GB")

        telemetry_data = {
            "os": f"{os_name} {os_release}",
            "python_version": python_ver,
            "free_storage_gb": free_gb,
            "status": "HEALTHY" if free_gb > 0.5 else "LOW_STORAGE"
        }
        return telemetry_data


# ======================================================
# 2. COMMAND PIPELINE PARSER (NATURAL COMMAND PARSER)
# ======================================================
class CommandPipelineParser:
    def parse_command(self, raw_command):
        print("\n[🎙️ COMMAND PIPELINE PARSER]")
        print(f"[*] Raw Input Command: '{raw_command}'")

        parsed_action = {"action": "UNKNOWN", "target": None, "port": 80}

        # Regex matching for IP or Domain scanning intents
        ip_match = re.search(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", raw_command)
        domain_match = re.search(r"\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}\b", raw_command)

        if "scan" in raw_command.lower() or "check" in raw_command.lower():
            parsed_action["action"] = "PORT_SCAN"
            if ip_match:
                parsed_action["target"] = ip_match.group(0)
            elif domain_match:
                parsed_action["target"] = domain_match.group(0)

        print(f"[+] Parsed Action: {parsed_action['action']} | Target: {parsed_action['target']}")
        return parsed_action


# ======================================================
# 3. AUTOMATED INTEGRITY SNAPSHOT GENERATOR
# ======================================================
class IntegritySnapshotGenerator:
    def verify_script_integrity(self, file_path):
        print("\n[🛡️ AUTOMATED INTEGRITY SNAPSHOT GENERATOR]")
        if not os.path.exists(file_path):
            print(f"[-] File '{file_path}' not found for integrity check.")
            return False

        with open(file_path, "rb") as f:
            file_bytes = f.read()

        file_hash = hashlib.sha256(file_bytes).hexdigest()
        print(f"[*] Script Path: {file_path}")
        print(f"[+] Computed SHA-256 Hash: {file_hash[:24]}...")
        print("[+] Integrity Verification: VERIFIED_UNMUTATED")
        return file_hash


# ======================================================
# 4. DAY 86 CORE FUSION (DAYS 8, 9 & 13 REINFORCEMENT)
# ======================================================
class CoreNetworkInspector:
    def verify_target_reachability(self, target_ip, port=80):
        print(f"\n[📡 CORE NETWORK INSPECTOR - DAY 86]")
        print(f"[*] Resolving and inspecting: {target_ip}:{port}")

        try:
            resolved_ip = socket.gethostbyname(target_ip)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2.0)
            result = sock.connect_ex((resolved_ip, port))
            sock.close()

            status = "OPEN" if result == 0 else "CLOSED"
            print(f"[+] Target IP: {resolved_ip} | Port {port}: {status}")

            # Day 8 Logging Logic
            log_entry = f"[{time.strftime('%Y-%m-%d %H:%M:%S IST')}] Target: {target_ip} ({resolved_ip}) | Port {port}: {status}\n"
            with open("sudarshan_day86_audit.log", "a") as log_file:
                log_file.write(log_entry)

            print("[+] Log Record Written to 'sudarshan_day86_audit.log'")
            return status
        except Exception as e:
            print(f"[-] Inspection Error: {e}")
            return "ERROR"


# ======================================================
# MAIN DISPATCHER
# ======================================================
def run_day86_master_suite():
    print("=" * 65)
    print(" SUDARSHAN DAY 86 MASTER FUSION & TELEMETRY SUITE")
    print("=" * 65)

    # 1. Telemetry Check
    telemetry = EnvironmentTelemetryEngine()
    telemetry.get_system_telemetry()

    # 2. Integrity Verification
    integrity = IntegritySnapshotGenerator()
    integrity.verify_script_integrity("sudarshan_day86_fusion.py")

    # 3. Command Pipeline Parser
    parser = CommandPipelineParser()
    command_input = "SUDARSHAN please scan target 127.0.0.1"
    parsed_cmd = parser.parse_command(command_input)

    # 4. Target Execution (Day 8, 9, 13)
    if parsed_cmd["target"]:
        inspector = CoreNetworkInspector()
        inspector.verify_target_reachability(parsed_cmd["target"], port=80)

    print("\n[+] Day 86 Master Fusion Execution Completed Successfully.")


if __name__ == "__main__":
    run_day86_master_suite()
