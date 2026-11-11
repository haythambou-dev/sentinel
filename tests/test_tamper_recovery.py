import pytest
from core.tamper_monitor import TamperMonitor
from recovery.recovery_manager import generate_recovery_codes, verify_and_consume_recovery_code

def test_tamper_monitor():
    monitor = TamperMonitor()
    monitor.generate_manifest()
    assert monitor.verify_integrity() is True

def test_recovery_codes():
    plain_codes = generate_recovery_codes()
    assert len(plain_codes) == 5
    # Verify and consume first code
    code_to_test = plain_codes[0]
    assert verify_and_consume_recovery_code(code_to_test) is True
    # Cannot reuse same code
    assert verify_and_consume_recovery_code(code_to_test) is False
