# voice_input.py

import os
import tempfile
import speech_recognition as sr
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Create OpenAI client
client = OpenAI(api_key=api_key)

def record_and_transcribe():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    print("🎤 Please speak your cooking request...")

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # Save audio temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio_file:
        temp_audio_file.write(audio.get_wav_data())
        temp_audio_path = temp_audio_file.name

    print("🧠 Sending your voice to Whisper API for transcription...")

    try:
        with open(temp_audio_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="text"
            )

        print(f"✅ Transcription: {transcript}")
        return transcript

    except Exception as e:
        print(f"❌ Error transcribing audio: {e}")
        return None

    finally:
        if os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)
