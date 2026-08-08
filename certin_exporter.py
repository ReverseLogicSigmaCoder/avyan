import json
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

class CERTInComplianceExporter:
    def __init__(self, telemetry_file="live_scan_telemetry.json"):
        self.telemetry_file = telemetry_file

    def load_telemetry(self):
        try:
            with open(self.telemetry_file, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"[-] Error loading telemetry: {e}")
            return None

    def export_certin_json(self, output_file="certin_incident_report.json"):
        data = self.load_telemetry()
        if not data:
            return False

        certin_schema = {
            "certin_reporting_version": "2.0",
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "reporter_details": {
                "organization": "PROJECT AVYAN Sovereign Shield",
                "framework": "IDDM / NCIIPC Critical Sector Defense"
            },
            "incident_data": {
                "target_url": data.get("target_url", "N/A"),
                "target_ip": data.get("target_ip", "N/A"),
                "vulnerabilities_detected": data.get("dast_audit", {}).get("vulnerabilities", []),
                "scada_telemetry": data.get("scada_audit", [])
            },
            "compliance_status": "CERT-In Mandatory 6-Hour Window Compliant"
        }

        with open(output_file, "w") as f:
            json.dump(certin_schema, f, indent=4)
        print(f"[+] CERT-In JSON report generated: {output_file}")
        return True

    def export_certin_xml(self, output_file="certin_incident_report.xml"):
        data = self.load_telemetry()
        if not data:
            return False

        root = ET.Element("CERTInIncidentReport")
        ET.SubElement(root, "ReportVersion").text = "2.0"
        ET.SubElement(root, "TimestampUTC").text = datetime.now(timezone.utc).isoformat()
        
        target_node = ET.SubElement(root, "TargetInfo")
        ET.SubElement(target_node, "URL").text = str(data.get("target_url"))
        ET.SubElement(target_node, "IP").text = str(data.get("target_ip"))

        vulns_node = ET.SubElement(root, "Vulnerabilities")
        for v in data.get("dast_audit", {}).get("vulnerabilities", []):
            item = ET.SubElement(vulns_node, "Vulnerability")
            ET.SubElement(item, "Description").text = str(v.get("Vulnerability / Misconfiguration"))
            ET.SubElement(item, "Severity").text = str(v.get("Severity"))
            ET.SubElement(item, "Status").text = str(v.get("Status"))

        tree = ET.ElementTree(root)
        tree.write(output_file, encoding="utf-8", xml_declaration=True)
        print(f"[+] CERT-In XML report generated: {output_file}")
        return True

if __name__ == "__main__":
    exporter = CERTInComplianceExporter()
    exporter.export_certin_json()
    exporter.export_certin_xml()
