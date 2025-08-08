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

    # Final conversation text
    conversation_text = "\n".join(output_lines)

    # Analyze the transcript to get insights
    insights = analyze_transcript(conversation_text)

    # Prepare the combined text (conversation + insights)
    combined_text = f"=== CONVERSATION ===\n{conversation_text}\n\n=== INSIGHTS ===\n"

    if isinstance(insights, dict):
        for key, lines in insights.items():
            combined_text += f"{key.upper()}:\n"
            for line in lines:
                combined_text += f"- {line}\n"
            combined_text += "\n"
    elif isinstance(insights, list):
        for line in insights:
            combined_text += f"- {line}\n"
    else:
        combined_text += "No insights available or invalid format.\n"

    # Save to one single combined transcript file
    os.makedirs(output_folder, exist_ok=True)
    base_filename = os.path.splitext(os.path.basename(file_path))[0]
    transcript_path = os.path.join(output_folder, f"{base_filename}.txt")

    with open(transcript_path, "w", encoding="utf-8") as f:
        f.write(combined_text)

    return transcript_path
