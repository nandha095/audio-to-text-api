# 
# transcriber.py

import os
from app.assemblyai_transcriber import transcribe_and_save

def transcribe_all_files(input_folder="recordings", output_folder="transcripts"):
    transcribed_files = []
    for filename in os.listdir(input_folder):
        if filename.endswith(".mp3"):
            full_path = os.path.join(input_folder, filename)
            transcript_path = transcribe_and_save(full_path, output_folder)
            transcribed_files.append(transcript_path)
    return transcribed_files
