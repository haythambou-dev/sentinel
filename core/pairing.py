import secrets
import json
import time
from pathlib import Path
from core.config import DATA_DIR, load_config, save_config

PAIRING_FILE = DATA_DIR / "pairing_auth.json"

def generate_pairing_code() -> str:
    code = f"{secrets.randbelow(900)+100}-{secrets.randbelow(900)+100}"
    auth_token = secrets.token_hex(16)

    data = {
        "pairing_code": code,
        "auth_token": auth_token,
        "created_at": time.time()
    }
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(PAIRING_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    return code, auth_token

def verify_pairing_token(token: str) -> bool:
    if not PAIRING_FILE.exists():
        return False
    try:
        with open(PAIRING_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return secrets.compare_digest(data.get("auth_token", ""), token)
    except Exception:
        return False
