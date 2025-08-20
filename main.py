# main.py

from voice_input import record_and_transcribe
from ai_logic import get_cooking_instructions
from eleven_tts import speak_text_elevenlabs as speak_text
from ui import CookingAssistantUI

def main():
    transcribed_text = record_and_transcribe()
    if not transcribed_text:
        print("❌ Could not understand your speech. Exiting.")
        return

    cooking_response = get_cooking_instructions(transcribed_text)
    if not cooking_response:
        print("❌ Could not get cooking instructions from AI. Exiting.")
        return

    print("👀 Full GPT reply:\n", cooking_response)

    app = CookingAssistantUI([cooking_response], speak_function=lambda text: speak_text(text))
    app.run()

if __name__ == "__main__":
    main()
