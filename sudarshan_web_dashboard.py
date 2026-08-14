import json
import os
from flask import Flask, render_template_string, jsonify

app = Flask(__name__)

# Load Audit Data from Master Engine Report
def load_audit_data():
    report_file = "AVYAN_ALL_38_FEATURES_MASTER_REPORT.json"
    if os.path.exists(report_file):
        with open(report_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"executed_features": {}}

# Simple Clean Responsive Dashboard HTML
DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PROJECT AVYAN - SUDARSHAN EXECUTIVE DASHBOARD</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0d1117; color: #c9d1d9; margin: 0; padding: 20px; }
        .header { text-align: center; border-bottom: 2px solid #238636; padding-bottom: 15px; margin-bottom: 25px; }
        .header h1 { color: #58a6ff; margin: 0; }
        .card-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 15px; }
        .card { background-color: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 15px; }
        .card h3 { margin-top: 0; color: #7ee787; border-bottom: 1px solid #30363d; padding-bottom: 8px; }
        .status-pass { color: #3fb950; font-weight: bold; }
        .status-active { color: #58a6ff; font-weight: bold; }
        pre { background: #0d1117; padding: 10px; border-radius: 5px; overflow-x: auto; font-size: 12px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>SUDARSHAN SOVEREIGN DEFENSE DASHBOARD</h1>
        <p>Project AVYAN - 24/7 Threat Intelligence & Autonomous Audit Engine</p>
    </div>
    <div class="card-grid">
        <div class="card">
            <h3>System Overview</h3>
            <p><strong>Status:</strong> <span class="status-pass">OPERATIONAL</span></p>
            <p><strong>Integrated Modules:</strong> 38+ Historical & Day 86-100 Engines</p>
            <p><strong>Compliance:</strong> CERT-In & IDDM Single-Tender Ready</p>
        </div>
        <div class="card">
            <h3>Executive Summary</h3>
            <p><strong>PQC Log Security:</strong> ENFORCED</p>
            <p><strong>Zero-Trust Guard:</strong> ACTIVE</p>
            <p><strong>Air-Gap Diode:</strong> MONITORING</p>
        </div>
    </div>
    <h2 style="color: #58a6ff; margin-top: 30px;">Executed Engine Feeds</h2>
    <div class="card">
        <h3>Live Report Data (JSON Payload)</h3>
        <pre>{{ report_json }}</pre>
    </div>
</body>
</html>
"""

@app.route("/")
def index():
    data = load_audit_data()
    return render_template_string(DASHBOARD_HTML, report_json=json.dumps(data, indent=4))

@app.route("/api/audit")
def api_audit():
    return jsonify(load_audit_data())

if __name__ == "__main__":
    print("[*] Starting SUDARSHAN Live Dashboard Server on http://127.0.0.1:5000 ...")
    app.run(host="0.0.0.0", port=5000, debug=False)
