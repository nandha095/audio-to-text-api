# assemblyai_transcriber.py

import os
import assemblyai as aai

# Set your API key
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("ASSEMBLYAI_API_KEY")
aai.settings.api_key = api_key
# Transcribe and save to file with speaker label mapping to User1, User2, etc.
def transcribe_and_save(file_path, output_folder):
    config = aai.TranscriptionConfig(speaker_labels=True)
    transcriber = aai.Transcriber()

    # Transcribe with speaker diarization config
    transcript = transcriber.transcribe(file_path, config=config)

    # Map speakers (e.g., "Speaker A", "Speaker B") to "User1", "User2", etc.
    speaker_mapping = {}
    speaker_count = 1
    output_lines = []

    for utterance in transcript.utterances:
        speaker = utterance.speaker

        if speaker not in speaker_mapping:
            speaker_mapping[speaker] = f"User{speaker_count}"
            speaker_count += 1

        user_label = speaker_mapping[speaker]
        output_lines.append(f"{user_label}: {utterance.text.strip()}")

    # Create transcript text
    final_transcript = "\n".join(output_lines)

    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)
    filename = os.path.splitext(os.path.basename(file_path))[0] + ".txt"
    transcript_path = os.path.join(output_folder, filename)

    with open(transcript_path, "w", encoding="utf-8") as f:
        f.write(final_transcript)

    return transcript_path
