import customtkinter as ctk
import urllib.request
import urllib.parse
import json
from core.config import load_config, save_config

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

class SentinelMobileCompanion(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("SENTINEL MOBILE COMPANION")
        self.geometry("380x650")
        self.resizable(False, False)

        self.setup_ui()

    def setup_ui(self):
        # Header
        header = ctk.CTkFrame(self, fg_color="#18181b", corner_radius=0, height=80)
        header.pack(fill="x", side="top")

        title = ctk.CTkLabel(header, text="📱 SENTINEL COMPANION", font=("Arial Bold", 16), text_color="#ef4444")
        title.pack(pady=(15, 2))

        sub = ctk.CTkLabel(header, text="Remote PC Guardian Controller", font=("Arial", 11), text_color="#a1a1aa")
        sub.pack()

        # Body container
        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=20, pady=20)

        # Config section (Bot Token & Chat ID)
        cfg_frame = ctk.CTkFrame(body, fg_color="#27272a", corner_radius=8)
        cfg_frame.pack(fill="x", pady=(0, 15), padx=5)

        ctk.CTkLabel(cfg_frame, text="Telegram Bot Config", font=("Arial Bold", 12), text_color="#f4f4f5").pack(anchor="w", padx=15, pady=(10, 5))

        self.token_entry = ctk.CTkEntry(cfg_frame, placeholder_text="Bot Token", show="*", width=300)
        self.token_entry.pack(padx=15, pady=5)

        self.chat_entry = ctk.CTkEntry(cfg_frame, placeholder_text="Chat ID", width=300)
        self.chat_entry.pack(padx=15, pady=5)

        save_btn = ctk.CTkButton(cfg_frame, text="Save Config", command=self.save_telegram_config, fg_color="#3f3f46", hover_color="#52525b", height=30)
        save_btn.pack(padx=15, pady=(5, 10))

        # Load existing config if present
        config = load_config()
        if config.get("telegram_bot_token"):
            self.token_entry.insert(0, config.get("telegram_bot_token"))
        if config.get("telegram_chat_id"):
            self.chat_entry.insert(0, config.get("telegram_chat_id"))

        # Remote Action Buttons
        actions_frame = ctk.CTkFrame(body, fg_color="transparent")
        actions_frame.pack(fill="both", expand=True)

        btn_lock = ctk.CTkButton(actions_frame, text="🔒 LOCK PC REMOTELY", command=lambda: self.send_command("/lock"), fg_color="#dc2626", hover_color="#b91c1c", height=45, font=("Arial Bold", 13))
        btn_lock.pack(fill="x", pady=8)

        btn_pic = ctk.CTkButton(actions_frame, text="📸 SNAP SECURITY PHOTO", command=lambda: self.send_command("/pic"), fg_color="#2563eb", hover_color="#1d4ed8", height=45, font=("Arial Bold", 13))
        btn_pic.pack(fill="x", pady=8)

        btn_audio = ctk.CTkButton(actions_frame, text="🎙️ RECORD 20s AUDIO", command=lambda: self.send_command("/audio"), fg_color="#16a34a", hover_color="#15803d", height=45, font=("Arial Bold", 13))
        btn_audio.pack(fill="x", pady=8)

        btn_arm = ctk.CTkButton(actions_frame, text="🛡️ ARM PROTECTION", command=lambda: self.send_command("/arm"), fg_color="#d97706", hover_color="#b45309", height=45, font=("Arial Bold", 13))
        btn_arm.pack(fill="x", pady=8)

        btn_disarm = ctk.CTkButton(actions_frame, text="🔓 DISARM PROTECTION", command=lambda: self.send_command("/disarm"), fg_color="#4b5563", hover_color="#374151", height=45, font=("Arial Bold", 13))
        btn_disarm.pack(fill="x", pady=8)

        # Log / Output Box
        self.log_box = ctk.CTkTextbox(body, height=100, fg_color="#18181b", text_color="#22c55e", font=("Consolas", 11))
        self.log_box.pack(fill="x", pady=(10, 0))
        self.log_box.insert("end", "Companion App ready. Connected to Sentinel backend.\n")
        self.log_box.configure(state="disabled")

    def save_telegram_config(self):
        token = self.token_entry.get().strip()
        chat_id = self.chat_entry.get().strip()
        config = load_config()
        config["telegram_bot_token"] = token
        config["telegram_chat_id"] = chat_id
        config["telegram_notifications_enabled"] = True
        save_config(config)
        self.log_message("Telegram configuration saved successfully.")

    def send_command(self, cmd: str):
        config = load_config()
        token = config.get("telegram_bot_token", "")
        chat_id = config.get("telegram_chat_id", "")

        if not token or not chat_id:
            # If telegram not configured, execute locally as companion
            self.execute_local_command(cmd)
            return

        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": f"📱 Companion Command: {cmd}",
            "parse_mode": "Markdown"
        }
        try:
            data = urllib.parse.urlencode(payload).encode("utf-8")
            req = urllib.request.Request(url, data=data, method="POST")
            with urllib.request.urlopen(req, timeout=5) as response:
                if response.status == 200:
                    self.log_message(f"Sent command {cmd} to Sentinel.")
                else:
                    self.execute_local_command(cmd)
        except Exception:
            self.execute_local_command(cmd)

    def execute_local_command(self, cmd: str):
        import ctypes
        from core.protection import ProtectionManager
        from core.evidence_capture import capture_screenshot, record_audio

        pm = ProtectionManager()
        if cmd == "/lock":
            self.log_message("Executing local PC lock...")
            ctypes.windll.user32.LockWorkStation()
        elif cmd == "/pic":
            self.log_message("Capturing screenshot...")
            path = capture_screenshot()
            self.log_message(f"Saved pic to {path}")
        elif cmd == "/audio":
            self.log_message("Recording 20s audio...")
            path = record_audio(20)
            self.log_message(f"Saved audio to {path}")
        elif cmd == "/arm":
            pm.arm()
            self.log_message("Protection ARMED.")
        elif cmd == "/disarm":
            pm.disarm()
            self.log_message("Protection DISARMED.")

    def log_message(self, msg: str):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", f"> {msg}\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

if __name__ == "__main__":
    app = SentinelMobileCompanion()
    app.mainloop()
