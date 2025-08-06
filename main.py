from fastapi import FastAPI
import os
import whisper

app = FastAPI()
model = whisper.load_model("small")  # Or use "tiny" for faster processing

AUDIO_FOLDER = "audio_files"
OUTPUT_FOLDER = "transcripts"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Audio-to-Text API"}

@app.get("/process-folder")
def process_all_audio():
    results = []

    for filename in os.listdir(AUDIO_FOLDER):
        if filename.endswith((".mp3", ".wav", ".m4a")):
            audio_path = os.path.join(AUDIO_FOLDER, filename)
            print(f"Processing {filename}...")

            # Transcribe
            result = model.transcribe(audio_path)
            text = result["text"]

            # Save output
            output_filename = os.path.splitext(filename)[0] + ".txt"
            output_path = os.path.join(OUTPUT_FOLDER, output_filename)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(text)

            results.append({
                "file": filename,
                "text": text
            })

    return results
