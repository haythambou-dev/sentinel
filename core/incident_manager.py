import json
import uuid
from datetime import datetime
from pathlib import Path
from core.config import DATA_DIR, load_config

INCIDENTS_FILE = DATA_DIR / "incidents.json"

class IncidentManager:
    def __init__(self):
        self.ensure_storage()

    def ensure_storage(self):
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        if not INCIDENTS_FILE.exists():
            self._save_all([])

    def _load_all(self) -> list:
        if not INCIDENTS_FILE.exists():
            return []
        try:
            with open(INCIDENTS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    def _save_all(self, incidents: list):
        with open(INCIDENTS_FILE, "w", encoding="utf-8") as f:
            json.dump(incidents, f, indent=4)

    def create_incident(self, category: str, severity: str, details: dict) -> dict:
        incident = {
            "id": str(uuid.uuid4())[:8],
            "timestamp": datetime.now().isoformat(),
            "category": category,
            "severity": severity,  # LOW, MEDIUM, HIGH, CRITICAL
            "details": details,
            "ai_status": "PENDING",
            "notification_status": "QUEUED"
        }
        incidents = self._load_all()
        incidents.insert(0, incident) # newest first
        self._save_all(incidents)
        return incident

    def get_incidents(self, limit: int = 50) -> list:
        return self._load_all()[:limit]

    def clear_incidents(self):
        self._save_all([])
