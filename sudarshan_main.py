import os
import sys
import time

# Sub-modules paths import handling
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'modules')))

try:
    import day86_fusion
    import jarvis_ops
except ImportError as e:
    print(f"[-] Module Loading Warning: {e}")

def display_banner():
    print("=" * 70)
    print("          PROJECT AVYAN - SUDARSHAN SOVEREIGN DEFENSE ENGINE          ")
    print("                [ Master Command & Control Center ]                   ")
    print("=" * 70)

def main_menu():
    display_banner()
    print("\nSelect Engine Execution Pipeline:")
    print(" 1. Run Complete System Audit (Telemetry + Mesh Scan + Risk Forecast)")
    print(" 2. Run Day 86 Integration Suite (Telemetry, Command Parser, Socket Inspector)")
    print(" 3. Run Jarvis-Level Operations Suite (Parallel Scanner & Kill-Switch)")
    print(" 4. Dispatch Live Telegram Test Alert")
    print(" 5. Exit Control Room")
    
    choice = input("\nSUDARSHAN Console > ").strip()
    return choice

def run_pipeline():
    while True:
        choice = main_menu()
        
        if choice == '1':
            print("\n[🚀 INITIATING FULL SYSTEM AUDIT]")
            try:
                day86_fusion.run_day86_master_suite()
                jarvis_ops.run_jarvis_master_engine()
            except Exception as e:
                print(f"[-] Execution Error: {e}")
        elif choice == '2':
            try:
                day86_fusion.run_day86_master_suite()
            except Exception as e:
                print(f"[-] Execution Error: {e}")
        elif choice == '3':
            try:
                jarvis_ops.run_jarvis_master_engine()
            except Exception as e:
                print(f"[-] Execution Error: {e}")
        elif choice == '4':
            os.system("python test_telegram.py")
        elif choice == '5':
            print("\n[+] Exiting SUDARSHAN Command Center. System Shield Remains Active.")
            break
        else:
            print("[-] Invalid Selection. Please try again.")
        
        input("\nPress Enter to return to main menu...")
        os.system("clear" if os.name != "nt" else "cls")

if __name__ == "__main__":
    run_pipeline()
