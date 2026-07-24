import os
import sys
import json

sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

try:
    import test_telegram
except ImportError:
    test_telegram = None

try:
    from modules import vdp_passive_engine
except ImportError:
    vdp_passive_engine = None

def run_authorized_vdp_scan():
    print("\n==================================================")
    print("      SUDARSHAN VDP PASSIVE AUDIT ENGINE          ")
    print("==================================================")
    target = input("Enter Authorized Target Domain (e.g. example.com): ").strip()
    
    if not target:
        print("[-] Target Domain required!")
        return

    print(f"\n[+] Initializing Passive Reconnaissance on: {target}...")
    
    if vdp_passive_engine:
        results = vdp_passive_engine.run_passive_audit(target)
        vuln_count = len(results.get("vulnerabilities", []))
        
        print(f"\n[+] Audit Completed!")
        print(f"📊 Missing Security Headers / Findings: {vuln_count}")
        
        # Build Telegram Payload
        msg = f"🛡️ [SUDARSHAN VDP PASSIVE AUDIT REPORT]\n" \
              f"----------------------------------------\n" \
              f"🌐 Target: {target}\n" \
              f"⚠️ Findings Identified: {vuln_count}\n" \
              f"📄 Report Status: Formatted for CERT-In / NCIIPC Submission\n" \
              f"⚡ Engine: Passive Recon Mode Active"
              
        if test_telegram:
            test_telegram.send_test_alert(msg)
            print("[+] Scan Telemetry Dispatched To Telegram Successfully!")
    else:
        print("[-] Passive Scanner Module Not Found.")

def main_menu():
    print("==================================================")
    print("         PROJECT AVYAN - SUDARSHAN DEFENSE ENGINE")
    print("            [ Master Command & Control Center ]")
    print("==================================================")
    print("\nSelect Engine Execution Pipeline:")
    print("  1. Run Authorized VDP Passive Scan (Generates VDP Findings)")
    print("  2. Dispatch Live Telegram Test Alert")
    print("  3. Exit Control Room")

    choice = input("\nSUDARSHAN Console > ").strip()

    if choice == '1':
        run_authorized_vdp_scan()
    elif choice == '2':
        if test_telegram:
            test_telegram.send_test_alert("🚨 [SUDARSHAN ALERT]: Manual Test Trigger Successful!")
    elif choice == '3':
        print("\n[+] Exiting Control Room. Shield Active.")
        sys.exit(0)

if __name__ == "__main__":
    main_menu()

