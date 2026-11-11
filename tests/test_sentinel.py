import pytest
import os
from pathlib import Path
from core.config import load_config, save_config, DEFAULT_CONFIG
from core.protection import ProtectionManager
from core.incident_manager import IncidentManager
from recovery.recovery_manager import hash_password, verify_password, set_master_password

def test_config_loading():
    config = load_config()
    assert isinstance(config, dict)
    assert "armed" in config
    assert "failed_attempt_threshold" in config

def test_password_hashing():
    pwd = "securepassword123"
    hashed = hash_password(pwd)
    assert verify_password(pwd, hashed) is True
    assert verify_password("wrongpassword", hashed) is False

def test_incident_manager():
    mgr = IncidentManager()
    mgr.clear_incidents()
    inc = mgr.create_incident("TEST_EVENT", "HIGH", {"test_key": "test_value"})
    assert inc["category"] == "TEST_EVENT"
    assert inc["severity"] == "HIGH"

    incidents = mgr.get_incidents()
    assert len(incidents) == 1
    assert incidents[0]["id"] == inc["id"]

def test_protection_manager():
    prot = ProtectionManager()
    prot.disarm()
    assert prot.is_armed() is False
    prot.arm()
    assert prot.is_armed() is True
    prot.disarm()
    assert prot.is_armed() is False
