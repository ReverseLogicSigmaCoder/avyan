import sqlite3
import csv
import json
import os

DB_FILE = "sudarshan_audit.db"

def export_to_csv():
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM scan_logs")
        rows = cursor.fetchall()
        
        # Column names
        headers = [description[0] for description in cursor.description]
        
        filename = "sudarshan_audit_export.csv"
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(rows)
            
        print(f"[+] Successfully exported {len(rows)} records to '{filename}'")
        conn.close()
    except Exception as e:
        print(f"[-] CSV Export Error: {e}")

def export_to_json():
    try:
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row  # Return rows as dict-like objects
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM scan_logs")
        rows = [dict(row) for row in cursor.fetchall()]
        
        filename = "sudarshan_audit_export.json"
        with open(filename, mode='w', encoding='utf-8') as file:
            json.dump(rows, file, indent=4)
            
        print(f"[+] Successfully exported {len(rows)} records to '{filename}'")
        conn.close()
    except Exception as e:
        print(f"[-] JSON Export Error: {e}")

if __name__ == "__main__":
    print("==========================================================")
    print("        PROJECT AVYAN - AUDIT LOG EXPORT UTILITY          ")
    print("==========================================================")
    export_to_csv()
    export_to_json()
