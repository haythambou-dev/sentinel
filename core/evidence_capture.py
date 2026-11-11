import os
import time
import logging
from pathlib import Path
from core.config import DATA_DIR

logger = logging.getLogger("EvidenceCapture")

AUDIO_DIR = DATA_DIR / "audio"
PICS_DIR = DATA_DIR / "pics"

try:
    from PIL import ImageGrab
    IMAGE_GRAB_AVAILABLE = True
except ImportError:
    IMAGE_GRAB_AVAILABLE = False

try:
    import sounddevice as sd
    import numpy as np
    import scipy.io.wavfile as wav
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False

def ensure_evidence_dirs():
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    PICS_DIR.mkdir(parents=True, exist_ok=True)

def capture_screenshot() -> str:
    ensure_evidence_dirs()
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filepath = PICS_DIR / f"capture_{timestamp}.png"

    if IMAGE_GRAB_AVAILABLE:
        try:
            img = ImageGrab.grab()
            img.save(filepath)
            return str(filepath)
        except Exception as e:
            logger.error(f"Failed to capture screenshot: {e}")
    return ""

def record_audio(duration: int = 20) -> str:
    ensure_evidence_dirs()
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filepath = AUDIO_DIR / f"audio_{timestamp}.wav"

    if AUDIO_AVAILABLE:
        try:
            fs = 44100  # Sample rate
            logger.info(f"Recording {duration}s audio...")
            recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
            sd.wait()  # Wait until the recording is finished
            wav.write(filepath, fs, recording)
            return str(filepath)
        except Exception as e:
            logger.error(f"Failed to record audio: {e}")
    else:
        logger.warning("sounddevice/scipy not available for audio recording.")
    return ""
