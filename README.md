# SENTINEL
### A HAYTHAM PRODUCT

**Version:** 0.1.0  
**Platform:** Windows 10 / 11  
**Language:** Python 3.11  
**Developer:** Haytham  

---

## OVERVIEW

**SENTINEL** is a personal Windows PC security and intrusion detection application designed with a local-first, privacy-conscious architecture. It helps protect your workstation against unauthorized access, suspicious Windows login attempts, and unapproved removable USB storage devices.

---

## CORE FEATURES

1. **ARM / DISARM Control:** Securely activate or deactivate protection backed by master password authentication.
2. **Windows Login Monitor:** Monitors Windows Security Event Logs (Event ID 4625) for failed authentication attempts with configurable thresholds.
3. **USB Guard:** Detects newly connected removable storage devices via WMI and checks them against an approved device list.
4. **Incident Manager:** Maintains a structured, immutable-style audit log of security events and anomalies.
5. **Phone Notifications:** Telegram bot integration supporting offline queuing, retry handling, and duplicate prevention.
6. **Local AI Investigator:** Deterministic local rule-based analysis engine breaking down incidents into confirmed facts, strong indications, uncertainties, and recommendations.
7. **Tamper Detection & Startup Restoration:** Verifies SHA-256 file integrity and restores monitoring state across reboots.
8. **Secure Recovery System:** Cryptographically hashed single-use recovery codes and master password management.

---

## TECHNOLOGY STACK

- Python 3.11
- CustomTkinter (Modern Dark UI)
- Windows Event Log (`pywin32`) & WMI
- JSON Local Storage & SQLite Ready
- PyTest for comprehensive test coverage

---

## INSTALLATION & RUNNING

1. Ensure Python 3.11+ is installed.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run SENTINEL:
   ```bash
   python main.py
   ```

---

## RUNNING TESTS

```bash
python -m pytest
```

---

**SENTINEL — A HAYTHAM PRODUCT.**
