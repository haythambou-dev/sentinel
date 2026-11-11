import sys
import os
import winreg as reg
from pathlib import Path

APP_NAME = "SentinelGuardian"

def get_executable_path() -> str:
    if getattr(sys, 'frozen', False):
        return sys.executable
    else:
        # If running as script, point to python running main.py
        return os.path.abspath(sys.argv[0])

def enable_autorun() -> bool:
    """Add SENTINEL to Windows current user startup registry."""
    exe_path = get_executable_path()
    if not exe_path.endswith(".exe"):
        # If running from python script directly, wrap python + main.py
        base_dir = Path(__file__).resolve().parent.parent
        main_script = base_dir / "main.py"
        command = f'python "{main_script}"'
    else:
        command = f'"{exe_path}"'

    try:
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        with reg.OpenKey(reg.HKEY_CURRENT_USER, key_path, 0, reg.KEY_SET_VALUE) as key:
            reg.SetValueEx(key, APP_NAME, 0, reg.REG_SZ, command)
        return True
    except Exception as e:
        print(f"Failed to enable autorun: {e}")
        return False

def disable_autorun() -> bool:
    """Remove SENTINEL from Windows startup registry."""
    try:
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        with reg.OpenKey(reg.HKEY_CURRENT_USER, key_path, 0, reg.KEY_SET_VALUE) as key:
            reg.DeleteValue(key, APP_NAME)
        return True
    except Exception:
        return False

def is_autorun_enabled() -> bool:
    try:
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        with reg.OpenKey(reg.HKEY_CURRENT_USER, key_path, 0, reg.KEY_READ) as key:
            reg.QueryValueEx(key, APP_NAME)
        return True
    except Exception:
        return False
