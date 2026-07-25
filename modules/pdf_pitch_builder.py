import json
import os

def build_html_pitch_deck():
    """
    Generates a high-grade HTML/PDF-ready Executive Pitch Summary
    for B2B Outreach (PW, Creators, Enterprises) with Zero Budget.
    """
    deck_file = "AVYAN_B2B_EXECUTIVE_PITCH_DECK.json"
    output_html = "SUDARSHAN_EXECUTIVE_SECURITY_PITCH.html"
    
    if os.path.exists(deck_file):
        with open(deck_file, "r") as f:
            data = json.load(f)
    else:
        data = {"platform_name": "PROJECT AVYAN", "key_capabilities": []}

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{data.get('platform_name')} - Security Pitch</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 30px; background: #f4f6f9; color: #333; }}
            .container {{ background: white; padding: 25px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
            h1 {{ color: #1a202c; border-bottom: 2px solid #3182ce; padding-bottom: 10px; }}
            .badge {{ background: #3182ce; color: white; padding: 5px 10px; border-radius: 4px; font-weight: bold; }}
            ul {{ line-height: 1.8; }}
            .footer {{ margin-top: 30px; font-size: 12px; color: #718096; text-align: center; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>{data.get('platform_name')}</h1>
            <p><strong>Value Proposition:</strong> {data.get('value_proposition', 'Autonomous Cyber Shield')}</p>
            <p><span class="badge">Sovereign Grade</span> <strong>Authenticated Modules:</strong> {data.get('total_modules_authenticated', 38)}</p>
            
            <h3>Core Capabilities:</h3>
            <ul>
    """
    
    for cap in data.get("key_capabilities", []):
        html_content += f"<li>{cap}</li>\n"

    html_content += """
            </ul>
            <h3>14-Day Free PoC Audit Offer:</h3>
            <p>Zero-impact, non-intrusive passive security monitoring for high-scale digital infrastructure.</p>
            
            <div class="footer">
                Project AVYAN • SUDARSHAN Engine • Sovereign Cyber Security Architecture
            </div>
        </div>
    </body>
    </html>
    """

    with open(output_html, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"[+] Free Executive Presentation Generated: {output_html}")

if __name__ == "__main__":
    build_html_pitch_deck()
