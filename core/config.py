import json
import os
import logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = BASE_DIR / "config"
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"

CONFIG_FILE = CONFIG_DIR / "settings.json"
INCIDENTS_FILE = DATA_DIR / "incidents.json"

DEFAULT_CONFIG = {
    "armed": False,
    "failed_attempt_threshold": 3,
    "time_window_seconds": 300,
    "usb_guard_enabled": True,
    "telegram_notifications_enabled": False,
    "telegram_bot_token": "",
    "telegram_chat_id": "",
    "password_hash": ""  # empty initially, set on first setup
}

def ensure_dirs():
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)

def load_config() -> dict:
    ensure_dirs()
    if not CONFIG_FILE.exists():
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Ensure all default keys exist
            updated = False
            for k, v in DEFAULT_CONFIG.items():
                if k not in data:
                    data[k] = v
                    updated = True
            if updated:
                save_config(data)
            return data
    except Exception:
        return DEFAULT_CONFIG.copy()

def save_config(config: dict):
    ensure_dirs()
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)

def setup_logging():
    ensure_dirs()
    log_file = LOGS_DIR / "sentinel.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler()
        ]
    )
