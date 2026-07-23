from flask import Flask, render_template_string
import sqlite3

app = Flask(__name__)
DB_FILE = "sudarshan_audit.db"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Project AVYAN - SUDARSHAN SOC Dashboard</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0f172a; color: #e2e8f0; margin: 0; padding: 20px; }
        .container { max-width: 1000px; margin: auto; }
        h1 { color: #38bdf8; border-bottom: 2px solid #334155; padding-bottom: 10px; }
        .card { background-color: #1e293b; border-radius: 8px; padding: 15px; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
        table { width: 100%; border-collapse: collapse; margin-top: 15px; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #334155; }
        th { background-color: #334155; color: #f8fafc; }
        tr:hover { background-color: #334155; }
        .badge-ioc { background-color: #ef4444; color: white; padding: 3px 8px; border-radius: 4px; font-weight: bold; }
        .badge-clean { background-color: #22c55e; color: white; padding: 3px 8px; border-radius: 4px; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🛡️ PROJECT AVYAN - SUDARSHAN Dashboard</h1>
        <div class="card">
            <h2>Recent Audit Logs</h2>
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Timestamp (UTC)</th>
                        <th>Monitored Domain</th>
                        <th>Subdomains</th>
                        <th>IOC Status</th>
                        <th>Summary</th>
                    </tr>
                </thead>
                <tbody>
                    {% for row in logs %}
                    <tr>
                        <td>{{ row[0] }}</td>
                        <td>{{ row[1] }}</td>
                        <td><code>{{ row[3] }}</code></td>
                        <td>{{ row[4] }}</td>
                        <td>
                            {% if 'IOC' in row[5] %}
                                <span class="badge-ioc">{{ row[5] }}</span>
                            {% else %}
                                <span class="badge-clean">{{ row[5] }}</span>
                            {% endif %}
                        </td>
                        <td>{{ row[6] }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def dashboard():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM scan_logs ORDER BY id DESC LIMIT 20")
    logs = cursor.fetchall()
    conn.close()
    return render_template_string(HTML_TEMPLATE, logs=logs)

if __name__ == '__main__':
    print("[+] Starting SUDARSHAN Web Dashboard on http://127.0.0.1:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)
