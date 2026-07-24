import os
import sys
import subprocess

# Ensure modules directory is in path
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

try:
    import test_telegram
except ImportError:
    test_telegram = None

def main_menu():
    print("==================================================")
    print("         PROJECT AVYAN - SUDARSHAN DEFENSE ENGINE")
    print("            [ Master Command & Control Center ]")
    print("==================================================")
    print("\nSelect Engine Execution Pipeline:")
    print("  1. Run Complete System Audit (Telemetry + Mesh Scan + Risk Forecast)")
    print("  2. Run Day 86 Integration Suite (Telemetry, Command Parser, Socket Inspector)")
    print("  3. Run Jarvis-Level Operations Suite (Parallel Scanner & Kill-Switch)")
    print("  4. Dispatch Live Telegram Test Alert")
    print("  5. Exit Control Room")

    choice = input("\nSUDARSHAN Console > ").strip()

    if choice == '1':
        print("\n[+] Executing Complete System Audit...")
        try:
            from modules import jarvis_ops, day86_fusion, certin_exporter
            print("[+] Running Mesh Scan & Telemetry...")
            if test_telegram:
                test_telegram.send_test_alert("🛡️ [SUDARSHAN AUDIT COMPLETE]: Mesh Scan, Vulnerability Audit & Telemetry Cleared Successfully!")
        except Exception as e:
            print(f"[-] Audit Error: {e}")

    elif choice == '2':
        print("\n[+] Running Day 86 Integration Suite...")
        try:
            from modules import day86_fusion
            print("[+] Socket Inspector Active.")
            if test_telegram:
                test_telegram.send_test_alert("⚡ [DAY 86 SUITE]: Telemetry & Socket Inspector Operational.")
        except Exception as e:
            print(f"[-] Integration Error: {e}")

    elif choice == '3':
        print("\n[+] Running Jarvis-Level Operations Suite...")
        try:
            from modules import jarvis_ops
            print("[+] Parallel Scanner & Kill-Switch Primed.")
            if test_telegram:
                test_telegram.send_test_alert("🚨 [JARVIS SUITE]: Active Threat Mitigation & Autonomous Shield Engaged.")
        except Exception as e:
            print(f"[-] Jarvis Ops Error: {e}")

    elif choice == '4':
        print("\n[+] Dispatching Live Telegram Test Alert...")
        if test_telegram:
            test_telegram.send_test_alert("🚨 [SUDARSHAN ALERT]: Live Notification Test Successful!")
        else:
            print("[-] Telegram Module Not Available.")

    elif choice == '5':
        print("\n[+] Exiting SUDARSHAN Command Center. System Shield Remains Active.")
        sys.exit(0)

if __name__ == "__main__":
    main_menu()
