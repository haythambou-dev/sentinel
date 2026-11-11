import os
import subprocess
import sys
from pathlib import Path

def main():
    print("==========================================")
    print("   SENTINEL ANDROID APK BUILD HELPER      ")
    print("==========================================")

    app_dir = Path("android_app")
    if not app_dir.exists():
        print("Error: android_app directory not found!")
        input("\nPress Enter to exit...")
        return

    print("[*] Checking build environment...")
    try:
        res = subprocess.run(["docker", "--version"], capture_output=True, text=True)
        if res.returncode == 0:
            print("[+] Docker detected! Building APK inside Docker container...")
            current_dir = os.path.abspath(".")
            docker_cmd = [
                "docker", "run", "--rm",
                "-v", f"{current_dir}:/home/user/hostfolder",
                "-w", "/home/user/hostfolder/android_app",
                "kivy/buildozer",
                "buildozer", "android", "debug"
            ]
            print(f"Running: {' '.join(docker_cmd)}")
            subprocess.run(docker_cmd)
            print("\n[+] APK build process completed via Docker! Check android_app/bin/ for the .apk file.")
            input("\nPress Enter to exit...")
            return
    except Exception:
        pass

    print("\n[!] Docker not found on Windows. Buildozer requires Linux.")
    print("[*] To generate your APK instantly in 1 click:")
    print("    1. Open Google Colab: https://colab.research.google.com/")
    print("    2. Follow the instructions in android_app/README.md")
    print("    3. Download your sentinelmobile.apk!")

    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
