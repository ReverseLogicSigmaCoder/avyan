import os
import json
import shutil

class MultiTenantWorkspaceManager:
    def __init__(self, base_dir="client_workspaces"):
        self.base_dir = base_dir
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)

    def create_workspace(self, client_id, sector_name):
        tenant_path = os.path.join(self.base_dir, client_id)
        os.makedirs(tenant_path, exist_ok=True)
        os.makedirs(os.path.join(tenant_path, "telemetry"), exist_ok=True)
        os.makedirs(os.path.join(tenant_path, "reports"), exist_ok=True)

        config = {
            "client_id": client_id,
            "critical_sector": sector_name,
            "created_at": os.path.getctime(tenant_path),
            "isolated_storage": tenant_path
        }

        with open(os.path.join(tenant_path, "workspace_config.json"), "w") as f:
            json.dump(config, f, indent=4)

        print(f"[+] Isolated Workspace Created for Tenant: {client_id} [{sector_name}]")
        return tenant_path

    def save_tenant_telemetry(self, client_id, telemetry_data):
        tenant_path = os.path.join(self.base_dir, client_id, "telemetry")
        if not os.path.exists(tenant_path):
            print("[-] Workspace does not exist.")
            return False

        filepath = os.path.join(tenant_path, "live_scan_telemetry.json")
        with open(filepath, "w") as f:
            json.dump(telemetry_data, f, indent=4)
        print(f"[+] Telemetry isolated and saved to tenant: {client_id}")
        return True

if __name__ == "__main__":
    manager = MultiTenantWorkspaceManager()
    manager.create_workspace("client_ashwin_lead", "Power & Energy Sector")
