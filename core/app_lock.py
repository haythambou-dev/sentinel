import time
import logging
from core.config import load_config
from core.incident_manager import IncidentManager

logger = logging.getLogger("AppLock")

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

class AppLockManager:
    def __init__(self):
        self.incident_manager = IncidentManager()
        # Default locked apps (e.g. browsers or sensitive tools configured by user)
        self.locked_apps = ["cmd.exe", "powershell.exe", "chrome.exe", "msedge.exe"]

    def check_and_enforce_locks(self, is_armed: bool):
        if not is_armed or not PSUTIL_AVAILABLE:
            return

        try:
            for proc in psutil.process_iter(['name', 'pid']):
                pname = proc.info.get('name', '')
                if pname in self.locked_apps:
                    # When armed, if a locked app is running, log an incident and optionally terminate or alert
                    self.incident_manager.create_incident(
                        category="APP_LOCK_VIOLATION",
                        severity="HIGH",
                        details={"message": f"Restricted application running while armed: {pname} (PID: {proc.info['pid']})"}
                    )
                    # For safety, we log and notify. We don't forcefully kill user apps unless configured, but we record the intrusion.
        except Exception as e:
            logger.error(f"Error checking app lock: {e}")
