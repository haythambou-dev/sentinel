import time
from datetime import datetime, timedelta
import logging
from core.config import load_config
from core.incident_manager import IncidentManager

logger = logging.getLogger("LoginMonitor")

try:
    import win32evtlog
    import win32evtlogutil
    WINDOWS_LOG_AVAILABLE = True
except ImportError:
    WINDOWS_LOG_AVAILABLE = False

class LoginMonitor:
    def __init__(self):
        self.incident_manager = IncidentManager()
        self.failed_attempts = [] # timestamps of recent failed attempts

    def check_logins(self) -> int:
        """Poll Windows Security event log for failed login attempts (Event ID 4625)."""
        if not WINDOWS_LOG_AVAILABLE:
            logger.warning("win32evtlog not available. Windows login monitoring disabled.")
            return 0

        config = load_config()
        threshold = config.get("failed_attempt_threshold", 3)
        window_sec = config.get("time_window_seconds", 300)

        new_failures_count = 0
        server = 'localhost'
        logtype = 'Security'

        try:
            hand = win32evtlog.OpenEventLog(server, logtype)
            flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ

            # Read recent events
            events = win32evtlog.ReadEventLog(hand, flags, 0)
            cutoff_time = datetime.now() - timedelta(seconds=window_sec)

            for event in events:
                # Event ID 4625: An account failed to log on
                if event.EventID == 4625:
                    event_time = event.TimeGenerated
                    # Convert pytime to datetime if needed or compare
                    # event.TimeGenerated is typically a pywintypes.time object or datetime
                    try:
                        dt_event = datetime(
                            event_time.year, event_time.month, event_time.day,
                            event_time.hour, event_time.minute, event_time.second
                        )
                    except Exception:
                        dt_event = datetime.now()

                    if dt_event >= cutoff_time:
                        # Check if we already recorded this exact timestamp
                        timestamp_str = dt_event.isoformat()
                        if timestamp_str not in self.failed_attempts:
                            self.failed_attempts.append(timestamp_str)
                            new_failures_count += 1

            win32evtlog.CloseEventLog(hand)
        except Exception as e:
            logger.error(f"Error reading Windows Security Event Log: {e}")

        # Check threshold
        if len(self.failed_attempts) >= threshold:
            self.incident_manager.create_incident(
                category="WINDOWS_LOGIN_FAILURE",
                severity="HIGH",
                details={
                    "message": f"Detected {len(self.failed_attempts)} failed login attempts within {window_sec}s.",
                    "attempts_count": len(self.failed_attempts),
                    "threshold": threshold
                }
            )
            # Clear after alerting to prevent spamming
            self.failed_attempts.clear()

        return new_failures_count
