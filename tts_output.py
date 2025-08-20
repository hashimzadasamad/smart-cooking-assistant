# tts_output.py

from gtts import gTTS
from playsound import playsound
import os
import tempfile

# Supported gTTS languages; "az" isn't natively supported
SUPPORTED_LANGS = {"en", "ru", "tr"}

def speak_text(text, lang="en"):
    """
    Converts text to speech using gTTS and plays it.
    Falls back to English if the language is unsupported.
    """
    temp_path = None

    if lang not in SUPPORTED_LANGS:
        print(f"⚠️ Language '{lang}' not supported by gTTS. Falling back to English.")
        lang = "en"

    try:
        tts = gTTS(text=text, lang=lang)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio_file:
            temp_path = temp_audio_file.name
            tts.save(temp_path)

        playsound(temp_path)

    except Exception as e:
        print(f"❌ Error in gTTS TTS: {e}")

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
