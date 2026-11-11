import json
import logging
from pathlib import Path
from core.config import DATA_DIR, load_config
from core.incident_manager import IncidentManager

logger = logging.getLogger("USBGuard")

APPROVED_USB_FILE = DATA_DIR / "approved_usb.json"

try:
    import wmi
    WMI_AVAILABLE = True
except ImportError:
    WMI_AVAILABLE = False

class USBGuard:
    def __init__(self):
        self.incident_manager = IncidentManager()
        self.ensure_approved_storage()

    def ensure_approved_storage(self):
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        if not APPROVED_USB_FILE.exists():
            self._save_approved([])

    def _load_approved(self) -> list:
        if not APPROVED_USB_FILE.exists():
            return []
        try:
            with open(APPROVED_USB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    def _save_approved(self, devices: list):
        with open(APPROVED_USB_FILE, "w", encoding="utf-8") as f:
            json.dump(devices, f, indent=4)

    def get_connected_usb_devices(self) -> list:
        devices = []
        if not WMI_AVAILABLE:
            logger.warning("WMI not available. USB detection simulated or disabled.")
            return devices

        try:
            c = wmi.WMI()
            # Query USB disk drives or PNP entities
            for disk in c.Win32_DiskDrive(InterfaceType="USB"):
                devices.append({
                    "device_id": disk.DeviceID,
                    "name": disk.Caption,
                    "serial": getattr(disk, "SerialNumber", "UNKNOWN").strip(),
                    "pnp_device_id": getattr(disk, "PNPDeviceID", "UNKNOWN")
                })
        except Exception as e:
            logger.error(f"Error querying USB devices via WMI: {e}")

        return devices

    def scan_and_guard(self):
        config = load_config()
        if not config.get("usb_guard_enabled", True):
            return

        connected = self.get_connected_usb_devices()
        approved_list = self._load_approved()
        approved_serials = [d.get("serial") for d in approved_list]

        for dev in connected:
            serial = dev["serial"]
            if serial not in approved_serials and serial != "UNKNOWN":
                # Unapproved USB device detected!
                self.incident_manager.create_incident(
                    category="USB_GUARD_ALERT",
                    severity="MEDIUM",
                    details={
                        "message": f"Unapproved USB storage device detected: {dev['name']}",
                        "device_name": dev["name"],
                        "serial": serial
                    }
                )
                # Auto-approve or log? We log incident and alert owner.

    def approve_device(self, device_info: dict):
        approved = self._load_approved()
        if device_info not in approved:
            approved.append(device_info)
            self._save_approved(approved)
