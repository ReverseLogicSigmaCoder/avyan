import os
import pytest

# 1. SCADA Scanner File Check
def test_scada_scanner_exists():
    assert os.path.exists("real_scada_scanner.py"), "SCADA Scanner script missing!"

# 2. Master Orchestrator Check
def test_orchestrator_exists():
    assert os.path.exists("sudarshan_master_orchestrator.py"), "Master Orchestrator file missing!"

# 3. Air-gap Monitor Module Check (Root Level)
def test_airgap_module_exists():
    assert os.path.exists("modules/ics_airgap_monitor.py"), "Airgap Monitoring module missing!"

# 4. Config JSON Integrity Check
def test_config_file():
    assert os.path.exists("config.json"), "Config file missing!"
