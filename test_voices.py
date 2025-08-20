from elevenlabs import ElevenLabs
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("ELEVEN_API_KEY")

print(f"\n🔑 Using API key (first 8 characters): {api_key[:8]}...\n")

try:
    client = ElevenLabs(api_key=api_key)
    voices = client.voices.get_all()

    print("🎤 Raw voice list response from API:\n")
    print(voices)

    # Try to list by name, if any
    if isinstance(voices, list) and voices:
        print("\n🎤 Formatted voice names:\n")
        for v in voices:
            name = v.get("name") if isinstance(v, dict) else getattr(v, "name", "Unnamed")
            vid = v.get("voice_id") if isinstance(v, dict) else getattr(v, "voice_id", "Unknown")
            print(f"- {name} (ID: {vid})")
    elif isinstance(voices, dict) and "voices" in voices and voices["voices"]:
        print("\n🎤 Formatted voice names:\n")
        for v in voices["voices"]:
            name = v.get("name")
            vid = v.get("voice_id")
            print(f"- {name} (ID: {vid})")
    else:
        print("\n⚠️ No voices found in your account via the API.")

except Exception as e:
    print(f"\n❌ ERROR: {e}")
