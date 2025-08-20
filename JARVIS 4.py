import os
import threading
import tempfile
import numpy as np
import sounddevice as sd
from pydub import AudioSegment
import tkinter as tk
from tkinter import scrolledtext
import speech_recognition as sr
from langdetect import detect
from dotenv import load_dotenv
from openai import OpenAI

# Load API key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Globals
current_audio = None
playback_data = None
paused = False
position = 0
stream = None
last_reply = ""

# -------------------------- AUDIO CONTROL --------------------------

def play_audio_segment(segment, start_position=0):
    global playback_data, stream, position, paused, current_audio

    def callback(outdata, frames, time, status):
        global position
        if status:
            print(status)
        start = position
        end = start + frames * 2
        chunk = playback_data[start:end]
        if len(chunk) < frames * 2:
            outdata[:len(chunk)//2] = np.frombuffer(chunk, dtype=np.int16).reshape(-1, 1)
            outdata[len(chunk)//2:] = np.zeros((frames - len(chunk)//2, 1), dtype=np.int16)
            raise sd.CallbackStop()
        else:
            outdata[:] = np.frombuffer(chunk, dtype=np.int16).reshape(-1, 1)
            position += frames * 2

    audio = segment.set_channels(1).set_frame_rate(24000)
    playback_data = audio.raw_data
    position = start_position
    paused = False
    current_audio = audio
    stream = sd.OutputStream(
        samplerate=audio.frame_rate,
        channels=1,
        dtype='int16',
        callback=callback
    )
    stream.start()

def pause_audio():
    global stream, paused
    if stream:
        stream.stop()
        paused = True

def resume_audio():
    global paused, position, current_audio
    if paused and current_audio:
        play_audio_segment(current_audio, start_position=position)

def stop_audio():
    global stream, paused, position
    if stream:
        stream.stop()
        stream.close()
    paused = False
    position = 0

def speak(text):
    global current_audio, position
    def run():
        try:
            response = client.audio.speech.create(
                model="tts-1",
                voice="nova",
                input=text
            )
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
                tmp_file.write(response.read())
                tmp_file.flush()
                audio = AudioSegment.from_file(tmp_file.name, format="mp3")
                current_audio = audio
                position = 0
                play_audio_segment(audio)
        except Exception as e:
            log("TTS xətası: " + str(e))
    threading.Thread(target=run).start()

# -------------------------- GPT & VOICE --------------------------

def record_voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        log("🎤 Dinlənilir...")
        audio = recognizer.listen(source)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        f.write(audio.get_wav_data())
    try:
        with open(f.name, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="az"
            )
        text = transcript.text.strip()
        log(f"Siz (səs): {text}")
        process_input(text, from_voice=True)
    except Exception as e:
        log("Səs çevirmədə xəta: " + str(e))

def detect_language(text):
    try:
        return detect(text)
    except:
        return "en"

def correct_azerbaijani_text(text):
    try:
        correction_prompt = f"Sən Azərbaycanca danışığı düzgün cümlə şəklində düzəlt. Giriş: '{text}'"
        correction = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": correction_prompt}],
            max_tokens=60
        )
        return correction.choices[0].message.content.strip()
    except Exception as e:
        log("Düzəliş xətası: " + str(e))
        return text

def get_gpt_reply(text):
    global last_reply
    messages = [
        {"role": "system", "content": (
            "You are Chief Chef, a smart and friendly multilingual cooking assistant. "
            "Help the user with recipes, cooking steps, and kitchen-related questions. "
            "Respond in the user's language."
        )},
        {"role": "user", "content": text}
    ]
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            max_tokens=1000,
            temperature=0.7
        )
        reply = response.choices[0].message.content.strip()
        last_reply = reply
        return reply
    except Exception as e:
        log("GPT xəta: " + str(e))
        return "Bağışlayın, cavab verə bilmədim."

def process_input(text, from_voice=False):
    lang = detect_language(text)
    if lang == "az":
        text = correct_azerbaijani_text(text)
    reply = get_gpt_reply(text)
    log(f"👨‍🍳 Chief Chef:\n{reply}\n")
    if from_voice:
        speak(reply)

# -------------------------- GUI --------------------------

def send_input():
    text = input_box.get()
    input_box.delete(0, tk.END)
    if text.strip() == "":
        return
    log(f"📝 Siz: {text}")
    process_input(text, from_voice=False)

def read_last():
    if last_reply:
        speak(last_reply)

def log(message):
    output_box.insert(tk.END, message + "\n")
    output_box.see(tk.END)

# -------------------------- Build GUI --------------------------

root = tk.Tk()
root.title("Chief Chef – Smart Cooking Assistant")
root.geometry("770x640")
root.configure(bg="#fff9f3")

# Fonts and styles
font_title = ("Verdana", 20, "bold")
font_label = ("Arial", 11)
font_button = ("Arial", 11, "bold")
button_bg = "#f58c42"
button_fg = "#ffffff"
highlight_bg = "#ffcb77"

# Title
tk.Label(root, text="👨‍🍳 Chief Chef", font=font_title, bg="#fff9f3", fg="#333").pack(pady=(10, 0))
tk.Label(root, text="Your Smart Multilingual Cooking Assistant", font=("Arial", 10), bg="#fff9f3", fg="#666").pack()

# Output area
output_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=18, font=("Arial", 11), bg="#fffdf5", fg="#222")
output_box.pack(padx=12, pady=10, fill=tk.BOTH, expand=True)

# Input area
input_frame = tk.Frame(root, bg="#fff9f3")
input_frame.pack(pady=6)

input_box = tk.Entry(input_frame, font=("Arial", 12), width=50, bg="#ffffff", fg="#333")
input_box.pack(side=tk.LEFT, padx=5)

send_btn = tk.Button(input_frame, text="Göndər", font=font_button, bg="#56cfe1", fg="white", activebackground="#48bfe3", command=send_input)
send_btn.pack(side=tk.LEFT, padx=3)

voice_btn = tk.Button(input_frame, text="🎙️ Səsli danış", font=font_button, bg="#80ed99", fg="#222", activebackground="#70e000", command=lambda: threading.Thread(target=record_voice_input).start())
voice_btn.pack(side=tk.LEFT, padx=3)

# Playback controls
control_frame = tk.Frame(root, bg="#fff9f3")
control_frame.pack(pady=10)

tk.Button(control_frame, text="⏸ Dayandır", font=font_button, bg="#ffd166", command=pause_audio).pack(side=tk.LEFT, padx=6)
tk.Button(control_frame, text="▶ Davam et", font=font_button, bg="#06d6a0", fg="white", command=resume_audio).pack(side=tk.LEFT, padx=6)
tk.Button(control_frame, text="⏹ Stop", font=font_button, bg="#ef476f", fg="white", command=stop_audio).pack(side=tk.LEFT, padx=6)
tk.Button(control_frame, text="🔁 Təkrar", font=font_button, bg="#118ab2", fg="white", command=read_last).pack(side=tk.LEFT, padx=6)

root.mainloop()
