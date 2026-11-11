import pytest
from core.login_monitor import LoginMonitor
from usb_guard.device_monitor import USBGuard
from core.incident_manager import IncidentManager

def test_login_monitor_init():
    monitor = LoginMonitor()
    assert monitor is not None

def test_usb_guard_init():
    guard = USBGuard()
    assert guard is not None
    devices = guard.get_connected_usb_devices()
    assert isinstance(devices, list)
