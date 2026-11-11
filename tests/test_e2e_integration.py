import pytest
from core.config import load_config, save_config
from core.protection import ProtectionManager
from core.incident_manager import IncidentManager
from core.login_monitor import LoginMonitor
from usb_guard.device_monitor import USBGuard
from notifications.phone_alerts import TelegramNotifier
from investigator.security_agent import SecurityAgent
from core.tamper_monitor import TamperMonitor
from recovery.recovery_manager import generate_recovery_codes, verify_and_consume_recovery_code

def test_e2e_sentinel_workflow():
    # 1. Clear and init incident manager
    im = IncidentManager()
    im.clear_incidents()
    assert len(im.get_incidents()) == 0

    # 2. Protection Arm/Disarm lifecycle
    pm = ProtectionManager()
    pm.disarm()
    assert pm.is_armed() is False
    pm.arm()
    assert pm.is_armed() is True

    # 3. Simulate security incident creation
    incident = im.create_incident(
        category="E2E_TEST_EVENT",
        severity="HIGH",
        details={"message": "End-to-end integration test incident"}
    )
    assert incident["category"] == "E2E_TEST_EVENT"
    assert len(im.get_incidents()) >= 2 # Disarm + Arm + Test event

    # 4. Run local investigator
    agent = SecurityAgent()
    analysis = agent.analyze_incidents()
    assert len(analysis["confirmed_facts"]) > 0

    # 5. Check integrity and tamper monitor
    tm = TamperMonitor()
    tm.generate_manifest()
    assert tm.verify_integrity() is True

    # 6. Test notifications queue
    notif = TelegramNotifier()
    notif.queue_notification("E2E test alert notification")
    queue = notif._load_queue()
    assert len(queue) > 0

    # 7. Test recovery codes
    codes = generate_recovery_codes()
    assert len(codes) == 5
    assert verify_and_consume_recovery_code(codes[0]) is True

    # 8. Disarm protection
    pm.disarm()
    assert pm.is_armed() is False
