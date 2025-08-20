# ai_logic.py

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
openai_model = os.getenv("OPENAI_MODEL", "gpt-4-turbo")

client = OpenAI(api_key=api_key)

def get_cooking_instructions(user_text):
    try:
        system_prompt = (
            "You are a helpful and fluent cooking assistant. "
            "When the user asks for a recipe in any language (Azerbaijani, English, or Russian), "
            "reply in the same language using full detailed instructions and ingredients. "
            "Format the response clearly and conversationally. Do not switch languages."
        )

        response = client.chat.completions.create(
            model=openai_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_text}
            ],
            temperature=0.7,
            max_tokens=800
        )

        reply = response.choices[0].message.content
        print("✅ AI response received.")
        return reply

    except Exception as e:
        print(f"❌ Error talking to ChatGPT: {e}")
        return None
