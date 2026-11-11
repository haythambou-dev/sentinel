import hashlib
import secrets
import time
import json
from pathlib import Path
from core.config import load_config, save_config, DATA_DIR

RECOVERY_CODES_FILE = DATA_DIR / "recovery_codes.json"

def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
    return f"{salt}${pwd_hash.hex()}"

def verify_password(password: str, stored_hash: str) -> bool:
    if not stored_hash or "$" not in stored_hash:
        return False
    salt, pwd_hash_hex = stored_hash.split("$", 1)
    pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
    return secrets.compare_digest(pwd_hash.hex(), pwd_hash_hex)

def set_master_password(password: str):
    config = load_config()
    config["password_hash"] = hash_password(password)
    save_config(config)

def verify_master_password(password: str) -> bool:
    config = load_config()
    stored = config.get("password_hash", "")
    if not stored:
        set_master_password(password)
        return True
    return verify_password(password, stored)

def generate_recovery_codes() -> list:
    codes = [secrets.token_hex(4).upper() + "-" + secrets.token_hex(4).upper() for _ in range(5)]
    hashed_codes = []
    for code in codes:
        salt = secrets.token_hex(8)
        h = hashlib.pbkdf2_hmac('sha256', code.encode('utf-8'), salt.encode('utf-8'), 50000)
        hashed_codes.append({"hash": f"{salt}${h.hex()}", "used": False})

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(RECOVERY_CODES_FILE, "w", encoding="utf-8") as f:
        json.dump(hashed_codes, f, indent=4)
    return codes

def verify_and_consume_recovery_code(plain_code: str) -> bool:
    if not RECOVERY_CODES_FILE.exists():
        return False
    try:
        with open(RECOVERY_CODES_FILE, "r", encoding="utf-8") as f:
            codes = json.load(f)
    except Exception:
        return False

    valid = False
    for item in codes:
        if item["used"]:
            continue
        salt, h_hex = item["hash"].split("$", 1)
        h = hashlib.pbkdf2_hmac('sha256', plain_code.encode('utf-8'), salt.encode('utf-8'), 50000)
        if secrets.compare_digest(h.hex(), h_hex):
            item["used"] = True
            valid = True
            break

    if valid:
        with open(RECOVERY_CODES_FILE, "w", encoding="utf-8") as f:
            json.dump(codes, f, indent=4)

    return valid
