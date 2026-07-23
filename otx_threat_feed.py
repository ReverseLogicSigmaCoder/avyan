import requests

# Public Indicator Feed Endpoint (No API Key Required)
OTX_PUBLIC_API = "https://otx.alienvault.com/api/v1/indicators/IPv4/8.8.8.8/general"

def fetch_threat_intelligence():
    print("[+] SUDARSHAN Engine: Fetching Global Threat Data...")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }
    
    try:
        response = requests.get(OTX_PUBLIC_API, headers=headers, timeout=20)
        
        if response.status_code == 200:
            print("[SUCCESS] OTX Threat Intelligence Feed Connected Successfully!")
            data = response.json()
            pulse_info = data.get('pulse_info', {})
            count = pulse_info.get('count', 0)
            print(f"[+] Total Threat Records Associated: {count}")
            return True
        else:
            print(f"[-] OTX API Returned Status Code: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"[-] Threat Feed Fetch Error: {e}")
        return False

if __name__ == "__main__":
    fetch_threat_intelligence()

