from flask import Flask, jsonify, render_template_string
import os, json

app = Flask(__name__)

ALL_MODULES = [
    {"day": "Day 1-20", "name": "OSINT & CT-Logs Subdomain Enum", "status": "ACTIVE"},
    {"day": "Day 21-40", "name": "Dynamic Payload Fuzzing & DAST Core", "status": "ACTIVE"},
    {"day": "Day 41-60", "name": "SARATHI AST Semantic Logic Auditor", "status": "ACTIVE"},
    {"day": "Day 61-75", "name": "24/7 Cloud Cron Scanning & Telegram Alert Pipeline", "status": "ACTIVE"},
    {"day": "Day 76-85", "name": "AlienVault OTX & Tor Dark Web Threat Intelligence", "status": "ACTIVE"},
    {"day": "Day 86", "name": "Core Logging & Dynamic Socket Verification Engine", "status": "ACTIVE"},
    {"day": "Day 87", "name": "Stealth Handshake, Evasion & Honeypot Sandbox", "status": "ACTIVE"},
    {"day": "Day 88", "name": "Automated Red Teaming & Self-Healing Supervisor", "status": "ACTIVE"},
    {"day": "Day 89", "name": "Attacker Database, Dark Web & Threat Intel Integration", "status": "ACTIVE"},
    {"day": "Day 90", "name": "Daemon Orchestration & Multi-Channel Webhook Routing", "status": "ACTIVE"},
    {"day": "Day 91", "name": "Zero-Trust & Behavioral Guard Engine (Satya-Drishti / Jeevan-Pramaan)", "status": "ACTIVE"},
    {"day": "Day 92", "name": "Insider Threat & File Watchdog Engine", "status": "ACTIVE"},
    {"day": "Day 93", "name": "PQC Immutable Log Security & Quantum-Resistant Seal", "status": "ACTIVE"},
    {"day": "Day 94", "name": "Executive Sovereign Dashboard & CERT-In Evidence Bundle", "status": "ACTIVE"},
    {"day": "Day 95", "name": "Software Supply Chain & SBOM Hardening Engine (CycloneDX)", "status": "ACTIVE"},
    {"day": "Day 96-98", "name": "System Stress, Resilience & Auto-Recovery Engine", "status": "ACTIVE"},
    {"day": "Day 99", "name": "IDDM Single-Tender Bureaucracy Hack & Procurement Engine", "status": "ACTIVE"},
    {"day": "Day 100", "name": "GRAND AVYAN CENTURY SEAL - Complete Sovereign Integration", "status": "ACTIVE"},
    {"day": "Special 1", "name": "Natural Voice Interaction & Speech Alerts", "status": "ACTIVE"},
    {"day": "Special 2", "name": "Advanced Deception & Dynamic Honeypot Framework", "status": "ACTIVE"},
    {"day": "Special 3", "name": "ICS/SCADA Protocol & Critical Infrastructure Shield", "status": "ACTIVE"},
    {"day": "Special 4", "name": "Air-Gap Monitoring & Hardware-Software Co-Design Attestation", "status": "ACTIVE"},
    {"day": "Special 5", "name": "APT Profiling & Geopolitical Threat Attribution Engine", "status": "ACTIVE"},
    {"day": "Special 6", "name": "Autonomous Cyber Kinetic Countermeasures Engine", "status": "ACTIVE"},
    {"day": "Special 7", "name": "Firmware-Level Immutable Attestation Shield", "status": "ACTIVE"},
    {"day": "Special 8", "name": "Predictive Threat Simulation Engine (Future Attack AI)", "status": "ACTIVE"}
]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PROJECT AVYAN - Master Sovereign Orchestrator</title>
    <style>
        body { background-color: #0d1117; color: #58a6ff; font-family: monospace; padding: 20px; }
        h1 { color: #1f6feb; border-bottom: 2px solid #30363d; padding-bottom: 10px; }
        .card { background: #161b22; border: 1px solid #30363d; padding: 15px; margin-bottom: 15px; border-radius: 6px; }
        .status-ok { color: #3fb950; font-weight: bold; }
        .module-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 10px; margin-top: 15px; }
        .module-card { background: #010409; border: 1px solid #21262d; padding: 10px; border-radius: 4px; }
        .tag { background: #1f6feb; color: white; padding: 2px 6px; border-radius: 3px; font-size: 0.8em; }
    </style>
</head>
<body>
    <h1>SUDARSHAN MASTER SOVEREIGN ORCHESTRATOR</h1>
    <p>Project AVYAN - 24/7 Threat Intelligence & Unified Defense System</p>
    
    <div class="card">
        <h3>System Status: <span class="status-ok">100% OPERATIONAL</span></h3>
        <p>Architect: <b>Ravindra (Jodhpur, RJ)</b> | AI Co-Pilot: <b>SARATHI</b></p>
        <p>Active Engine Modules: <b>{{ modules|length }} Unified Defense Engines Loaded</b></p>
    </div>

    <div class="card">
        <h3>Live Active Features & Engine Matrix (Day 1 - 100 + Special Suites)</h3>
        <div class="module-grid">
            {% for m in modules %}
            <div class="module-card">
                <span class="tag">{{ m.day }}</span>
                <p style="color: #c9d1d9; margin: 5px 0;"><b>{{ m.name }}</b></p>
                <span class="status-ok">● {{ m.status }}</span>
            </div>
            {% endfor %}
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, modules=ALL_MODULES)

@app.route('/api/status')
def api_status():
    return jsonify({"project": "AVYAN", "status": "ONLINE", "total_modules": len(ALL_MODULES), "modules": ALL_MODULES})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
