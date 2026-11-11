import http.server
import socketserver
import json
import ctypes
import threading
from core.protection import ProtectionManager
from core.evidence_capture import capture_screenshot, record_audio
from core.incident_manager import IncidentManager
from core.app_lock import AppLockManager
from core.pairing import generate_pairing_code

PORT = 5000

class SentinelAPIHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8') if content_length > 0 else "{}"
        try:
            data = json.loads(body)
        except Exception:
            data = {}

        path = self.path
        pm = ProtectionManager()
        im = IncidentManager()
        alm = AppLockManager()

        response_data = {"status": "success", "message": "Command executed"}

        if path == "/api/lock":
            ctypes.windll.user32.LockWorkStation()
            im.create_incident("REMOTE_COMMAND", "HIGH", {"message": "PC locked remotely from mobile phone."})
            response_data["message"] = "PC locked successfully."

        elif path == "/api/pic":
            path_img = capture_screenshot()
            im.create_incident("REMOTE_EVIDENCE", "MEDIUM", {"message": f"Security snapshot captured remotely: {path_img}"})
            response_data["message"] = f"Screenshot captured at {path_img}"

        elif path == "/api/audio":
            path_aud = record_audio(20)
            im.create_incident("REMOTE_EVIDENCE", "MEDIUM", {"message": f"20s Ambient audio recorded remotely: {path_aud}"})
            response_data["message"] = f"20s Audio recorded at {path_aud}"

        elif path == "/api/arm":
            pm.arm()
            response_data["message"] = "Protection armed."

        elif path == "/api/disarm":
            pm.disarm()
            response_data["message"] = "Protection disarmed."

        elif path == "/api/app_lock_status":
            response_data["locked_apps"] = alm.locked_apps
            response_data["is_armed"] = pm.is_armed()

        else:
            self.send_response(404)
            self.end_headers()
            return

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response_data).encode("utf-8"))

    def log_message(self, format, *args):
        return

def start_remote_bridge_server():
    code, token = generate_pairing_code()
    print(f"\n[SENTINEL REMOTE BRIDGE] Active on port {PORT}")
    print(f"[PAIRING CODE FOR PHONE APP]: {code}\n")

    try:
        with socketserver.TCPServer(("", PORT), SentinelAPIHandler) as httpd:
            httpd.serve_forever()
    except Exception as e:
        print(f"Remote bridge server error: {e}")

def run_bridge_in_background():
    t = threading.Thread(target=start_remote_bridge_server, daemon=True)
    t.start()
