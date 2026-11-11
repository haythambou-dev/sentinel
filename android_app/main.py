import json
import urllib.request
import urllib.parse
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

class SentinelMobileApp(App):
    def build(self):
        self.title = "SENTINEL Mobile Guardian"

        root = BoxLayout(orientation='vertical', padding=20, spacing=12)

        # Title
        root.add_widget(Label(text="🛡️ SENTINEL MOBILE", font_size=22, size_hint_y=None, height=45, color=(0.93, 0.26, 0.26, 1)))
        root.add_widget(Label(text="Remote PC Security & Evidence Hub", font_size=12, size_hint_y=None, height=25, color=(0.6, 0.6, 0.6, 1)))

        # PC IP & Pairing Code Input
        self.ip_input = TextInput(text="192.168.1.", hint_text="PC Local IP (e.g. 192.168.1.50)", multiline=False, size_hint_y=None, height=40)
        root.add_widget(self.ip_input)

        self.code_input = TextInput(hint_text="Pairing Code (e.g. 482-913)", multiline=False, size_hint_y=None, height=40)
        root.add_widget(self.code_input)

        # Action Buttons
        btn_lock = Button(text="🔒 LOCK PC REMOTELY", size_hint_y=None, height=48, background_color=(0.85, 0.15, 0.15, 1))
        btn_lock.bind(on_press=lambda x: self.send_command("lock"))
        root.add_widget(btn_lock)

        btn_pic = Button(text="📸 SNAP SECURITY PHOTO", size_hint_y=None, height=48, background_color=(0.15, 0.4, 0.85, 1))
        btn_pic.bind(on_press=lambda x: self.send_command("pic"))
        root.add_widget(btn_pic)

        btn_audio = Button(text="🎙️ RECORD 20s AUDIO", size_hint_y=None, height=48, background_color=(0.1, 0.6, 0.2, 1))
        btn_audio.bind(on_press=lambda x: self.send_command("audio"))
        root.add_widget(btn_audio)

        btn_arm = Button(text="🛡️ ARM PROTECTION", size_hint_y=None, height=48, background_color=(0.85, 0.5, 0.1, 1))
        btn_arm.bind(on_press=lambda x: self.send_command("arm"))
        root.add_widget(btn_arm)

        btn_disarm = Button(text="🔓 DISARM PROTECTION", size_hint_y=None, height=48, background_color=(0.4, 0.4, 0.4, 1))
        btn_disarm.bind(on_press=lambda x: self.send_command("disarm"))
        root.add_widget(btn_disarm)

        # Status Log
        self.status_label = Label(text="Status: Ready to connect", font_size=12, color=(0.2, 0.8, 0.2, 1), size_hint_y=None, height=40)
        root.add_widget(self.status_label)

        return root

    def send_command(self, cmd: str):
        ip = self.ip_input.text.strip()
        if not ip:
            self.status_label.text = "Error: Enter PC IP address first"
            return

        url = f"http://{ip}:5000/api/{cmd}"
        try:
            req = urllib.request.Request(url, data=b"{}", headers={'Content-Type': 'application/json'}, method="POST")
            with urllib.request.urlopen(req, timeout=4) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode("utf-8"))
                    self.status_label.text = f"Success: {data.get('message', cmd)}"
                else:
                    self.status_label.text = f"Command failed."
        except Exception as e:
            self.status_label.text = f"Connection error: {e}"

if __name__ == '__main__':
    SentinelMobileApp().run()
