import sys
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from core.config import setup_logging
from core.remote_bridge import run_bridge_in_background
from interface.dashboard import SentinelDashboard

def main():
    setup_logging()
    # Start the mobile remote bridge server in background thread
    run_bridge_in_background()

    app = SentinelDashboard()
    app.mainloop()

if __name__ == "__main__":
    main()
