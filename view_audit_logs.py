import sqlite3

DB_FILE = "sudarshan_audit.db"

def view_recent_logs():
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, timestamp, monitored_domain, subdomain_count, ioc_status, raw_summary FROM scan_logs ORDER BY id DESC LIMIT 10")
        rows = cursor.fetchall()
        
        print("\n==========================================================")
        print("         SUDARSHAN AUDIT DATABASE - RECENT LOGS           ")
        print("==========================================================\n")
        
        if not rows:
            print("[-] No records found in 'scan_logs' table yet.")
        else:
            for row in rows:
                print(f"🆔 Record ID       : {row[0]}")
                print(f"🕒 Timestamp       : {row[1]}")
                print(f"🌐 Monitored Domain: {row[2]}")
                print(f"📊 Subdomains Count: {row[3]}")
                print(f"⚠️ IOC Status      : {row[4]}")
                print(f"📝 Summary         : {row[5]}")
                print("-" * 58)
                
        conn.close()
    except Exception as e:
        print(f"[-] Database Query Error: {e}")

if __name__ == "__main__":
    view_recent_logs()
