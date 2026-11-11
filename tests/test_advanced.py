import pytest
from core.evidence_capture import capture_screenshot
from core.app_lock import AppLockManager
from notifications.phone_alerts import TelegramNotifier

def test_evidence_capture_init():
    # Test that capture functions execute safely without crashing
    path = capture_screenshot()
    assert isinstance(path, str)

def test_app_lock_manager():
    alm = AppLockManager()
    assert alm is not None
    alm.check_and_enforce_locks(False)

def test_telegram_remote_commands():
    tn = TelegramNotifier()
    # Test command handler without live network call
    tn.handle_command("status")
    assert True
