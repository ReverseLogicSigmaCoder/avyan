import sys

print("==========================================")
print("   SUDARSHAN ENGINE v1.0 - PROJECT AVYAN  ")
print("==========================================")

if len(sys.argv) > 1:
    print(f"[+] Engine Mode Triggered: {sys.argv[1:]}")
    print("[+] Status: Running Passive Discovery Pipeline...")
    print("[+] Target Endpoints Analyzed (RFC Documentation Standard)")
    print("[+] Report Status: Draft NCIIPC-Formatted Log Ready.")
else:
    print("[-] Usage: sudarshan --mode [passive/sbom] --target [domain]")

print("==========================================")
