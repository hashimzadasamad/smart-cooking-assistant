# 🧑‍🍳 Smart Cooking AI Assistant

Smart Cooking AI is a voice-controlled cooking assistant built with Python. It listens to your cooking request, fetches a full recipe using OpenAI GPT, and reads the recipe aloud in your language using ElevenLabs text-to-speech — all within a clean graphical interface.

## 🎯 Features

- 🎤 Voice-controlled input using OpenAI Whisper
- 🤖 Recipe generation using OpenAI GPT (GPT-4-turbo)
- 🗣️ Real-time spoken instructions using ElevenLabs multilingual voices
- 🪟 Graphical UI with Next/Repeat step controls
- 🌍 Multilingual support (Azerbaijani, English, Russian)
- 🧠 Language-aware GPT output (responds in your spoken language)

## 🏗️ Project Structure

smart-cooking-ai/
│
├── main.py # Entry point: orchestrates the assistant flow
├── voice_input.py # Records and transcribes your voice to text using OpenAI Whisper
├── ai_logic.py # Sends the transcribed query to ChatGPT and retrieves a recipe
├── eleven_tts.py # Converts recipe text to spoken audio using ElevenLabs streaming
├── ui.py # Graphical interface (Tkinter-based) with step navigation
├── .env # Environment variables for API keys (not included in repo)
├── requirements.txt # Python dependencies
└── README.md # Project documentation
