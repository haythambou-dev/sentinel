import hashlib
import json
import logging
from pathlib import Path
from core.config import BASE_DIR, DATA_DIR, load_config, save_config
from core.incident_manager import IncidentManager

logger = logging.getLogger("TamperMonitor")

INTEGRITY_MANIFEST_FILE = DATA_DIR / "integrity_manifest.json"

CRITICAL_FILES = [
    "core/config.py",
    "core/protection.py",
    "core/login_monitor.py",
    "core/incident_manager.py",
    "usb_guard/device_monitor.py",
    "recovery/recovery_manager.py",
    "notifications/phone_alerts.py",
    "investigator/security_agent.py"
]

class TamperMonitor:
    def __init__(self):
        self.incident_manager = IncidentManager()

    def _hash_file(self, file_path: Path) -> str:
        sha256 = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                while True:
                    data = f.read(65536)
                    if not data:
                        break
                    sha256.update(data)
            return sha256.hexdigest()
        except Exception:
            return ""

    def generate_manifest(self):
        manifest = {}
        for rel_path in CRITICAL_FILES:
            full_path = BASE_DIR / rel_path
            if full_path.exists():
                manifest[rel_path] = self._hash_file(full_path)
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        with open(INTEGRITY_MANIFEST_FILE, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=4)

    def verify_integrity(self) -> bool:
        if not INTEGRITY_MANIFEST_FILE.exists():
            self.generate_manifest()
            return True

        try:
            with open(INTEGRITY_MANIFEST_FILE, "r", encoding="utf-8") as f:
                saved_manifest = json.load(f)
        except Exception:
            return True

        tampered = False
        for rel_path in CRITICAL_FILES:
            full_path = BASE_DIR / rel_path
            if not full_path.exists():
                tampered = True
                self.incident_manager.create_incident(
                    category="TAMPER_DETECTION",
                    severity="CRITICAL",
                    details={"message": f"Critical file missing: {rel_path}"}
                )
                continue

            current_hash = self._hash_file(full_path)
            saved_hash = saved_manifest.get(rel_path, "")
            if current_hash != saved_hash:
                tampered = True
                self.incident_manager.create_incident(
                    category="TAMPER_DETECTION",
                    severity="CRITICAL",
                    details={"message": f"Critical file modified (tamper detected): {rel_path}"}
                )

        return not tampered

    def check_startup_state(self):
        """Restore monitoring state after reboot if previously armed."""
        config = load_config()
        if config.get("armed", False):
            self.incident_manager.create_incident(
                category="SYSTEM_STATE",
                severity="LOW",
                details={"message": "SENTINEL restarted and restored armed protection state."}
            )
