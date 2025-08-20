# eleven_tts.py

import os
from dotenv import load_dotenv
from elevenlabs import ElevenLabs, play

# Load ElevenLabs API key from .env
load_dotenv()
api_key = os.getenv("ELEVEN_API_KEY")
voice_id = "ZT9u07TYPVl83ejeLakq"  # Rachelle

# Initialize ElevenLabs client
client = ElevenLabs(api_key=api_key)

def speak_text_elevenlabs(text, lang="az"):
    """
    Generates and plays Azerbaijani speech using ElevenLabs.
    Uses the ElevenLabs SDK to handle all audio decoding and playback internally.
    """
    try:
        print(f"🔊 Speaking Azerbaijani with voice ID '{voice_id}'...")

        # Generate speech (non-streaming)
        audio = client.text_to_speech.convert(
            voice_id=voice_id,
            text=text,
            model_id="eleven_multilingual_v2"
        )

        # Play decoded audio using ElevenLabs' built-in player
        play(audio)

    except Exception as e:
        print(f"❌ ElevenLabs TTS error: {e}")
