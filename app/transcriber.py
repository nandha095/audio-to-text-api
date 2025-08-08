# transcriber.py

import os
from app.assemblyai_transcriber import transcribe_and_save


def save_combined_transcript(conversation_text, insights_text, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("=== CONVERSATION ===\n\n")
        f.write(conversation_text.strip())
        f.write("\n\n=== INSIGHTS ===\n\n")
        f.write(insights_text.strip())

def transcribe_all_files(input_folder="recordings", output_folder="transcripts"):
    os.makedirs(output_folder, exist_ok=True)

    transcribed_files = []

    if not os.path.exists(input_folder):
        raise FileNotFoundError(f"Input folder '{input_folder}' does not exist.")

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(".mp3"):
            full_path = os.path.join(input_folder, filename)

            try:
                transcript_path = transcribe_and_save(full_path, output_folder)
                transcribed_files.append(transcript_path)
            except Exception as e:
                print(f"Failed to transcribe {filename}: {e}")

    return transcribed_files
