import pytest
import time
import threading
from core.remote_bridge import start_remote_bridge_server
from core.pairing import generate_pairing_code

def test_pairing_code_generation():
    code, token = generate_pairing_code()
    assert len(code) == 7
    assert len(token) == 32
