# transcriber.py

import os
from app.assemblyai_transcriber import transcribe_and_save

def transcribe_all_files(input_folder="recordings", output_folder="transcripts"):
    os.makedirs(output_folder, exist_ok=True)  # Ensure output folder exists

    transcribed_files = []

    # Validate input folder exists
    if not os.path.exists(input_folder):
        raise FileNotFoundError(f"Input folder '{input_folder}' does not exist.")

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(".mp3"):  # Case-insensitive check
            full_path = os.path.join(input_folder, filename)

            try:
                transcript_path = transcribe_and_save(full_path, output_folder)
                transcribed_files.append(transcript_path)
            except Exception as e:
                print(f"Failed to transcribe {filename}: {e}")

    return transcribed_files
