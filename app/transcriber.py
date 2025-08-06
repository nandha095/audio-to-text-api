# app/transcriber.py

import os
import whisper

AUDIO_DIR = "recordings"
TEXT_DIR = "transcripts"

model = whisper.load_model("base")  # or medium/large if you prefer

def transcribe_all_files():
    if not os.path.exists(TEXT_DIR):
        os.makedirs(TEXT_DIR)

    transcripts = []
    for filename in os.listdir(AUDIO_DIR):
        if filename.endswith((".mp3", ".wav", ".m4a")):
            filepath = os.path.join(AUDIO_DIR, filename)
            print(f"Transcribing {filename}...")
            result = model.transcribe(filepath)
            text_path = os.path.join(TEXT_DIR, filename + ".txt")
            with open(text_path, "w", encoding="utf-8") as f:
                f.write(result["text"])
            transcripts.append(text_path)
    return transcripts
