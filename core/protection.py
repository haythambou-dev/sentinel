import time
from core.config import load_config, save_config
from core.incident_manager import IncidentManager

class ProtectionManager:
    def __init__(self):
        self.incident_manager = IncidentManager()

    def is_armed(self) -> bool:
        config = load_config()
        return config.get("armed", False)

    def arm(self) -> bool:
        config = load_config()
        config["armed"] = True
        config["armed_timestamp"] = time.time()
        save_config(config)
        self.incident_manager.create_incident(
            category="SYSTEM_STATE",
            severity="LOW",
            details={"message": "SENTINEL protection armed by user."}
        )
        return True

    def disarm(self) -> bool:
        config = load_config()
        config["armed"] = False
        save_config(config)
        self.incident_manager.create_incident(
            category="SYSTEM_STATE",
            severity="LOW",
            details={"message": "SENTINEL protection disarmed by user."}
        )
        return True
