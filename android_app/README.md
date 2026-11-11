# SENTINEL MOBILE APP BUILD GUIDE

To compile the Android APK (`sentinelmobile.apk`) from `android_app/`, you can use **Google Colab** (free Linux cloud environment with Buildozer pre-installed) or a Linux/WSL environment.

### Method: Build via Google Colab (Recommended & Free)
1. Go to [Google Colab](https://colab.research.google.com/).
2. Create a new notebook and paste these commands into the cells:

```python
# Cell 1: Clone or upload your android_app folder
!git clone https://github.com/HaythamB/SENTINEL.git # (or upload android_app files)
%cd SENTINEL/android_app

# Cell 2: Install Buildozer dependencies
!sudo apt-get update
!sudo apt-get install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev

# Cell 3: Install Buildozer
!pip install --upgrade buildozer

# Cell 4: Build APK
!buildozer -v android debug
```

3. Download the generated `.apk` from the Colab file explorer (`bin/sentinelmobile-0.1.0-debug.apk`) and install it directly on your Android phone!

---
**SENTINEL — A HAYTHAM PRODUCT.**
