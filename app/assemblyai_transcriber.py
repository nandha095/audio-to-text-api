import os
import assemblyai as aai
from dotenv import load_dotenv
from app.conversation_analyzer import analyze_transcript  # Ensure this function returns a dict

# Load environment variables and set API key
load_dotenv()
api_key = os.getenv("ASSEMBLYAI_API_KEY")
aai.settings.api_key = api_key

# Transcribe and save to file with speaker label mapping to User1, User2, etc.
def transcribe_and_save(file_path, output_folder):
    config = aai.TranscriptionConfig(speaker_labels=True)
    transcriber = aai.Transcriber()

    try:
        # Transcribe with speaker diarization config
        transcript = transcriber.transcribe(file_path, config=config)
    except Exception as e:
        print(f"Failed to transcribe {file_path}: {e}")
        return None

    # Map speakers to User1, User2, etc.
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

    # Create final transcript
    final_transcript = "\n".join(output_lines)

    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Save transcript
    base_filename = os.path.splitext(os.path.basename(file_path))[0]
    transcript_path = os.path.join(output_folder, f"{base_filename}.txt")
    with open(transcript_path, "w", encoding="utf-8") as f:
        f.write(final_transcript)

    # Analyze the transcript and save insights
    insights = analyze_transcript(final_transcript)

    insights_path = os.path.join(output_folder, f"{base_filename}_insights.txt")

    #  Correct handling of insights (check if it's dict or list)
    with open(insights_path, "w", encoding="utf-8") as f:
        if isinstance(insights, dict):
            for key, lines in insights.items():
                f.write(f"{key.upper()}:\n")
                for line in lines:
                    f.write(f"- {line}\n")
                f.write("\n")
        elif isinstance(insights, list):
            f.write("INSIGHTS:\n")
            for line in insights:
                f.write(f"- {line}\n")
        else:
            f.write("No insights available or invalid format.\n")

    return transcript_path, insights_path
