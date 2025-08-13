# FastAPI Audio Transcription Service

This project is a FastAPI-based service that takes audio files, transcribes them into text using AssemblyAI, and stores the transcripts in the `transcripts/` folder.

Currently, the audio files are manually placed in the `recordings/` folder and processed via a POST API endpoint.

---

## Features
- Accepts audio files from the `recordings/` folder.
- Transcribes audio to text using **AssemblyAI API**.
- Saves transcripts as `.txt` files in the `transcripts/` folder.
- Simple FastAPI API to trigger transcription.

---

## Project Structure
app/
├── assemblyai_transcriber.py # Handles transcription logic
├── pycache/
config.py # Configuration (API keys, etc.)
main.py # FastAPI app with endpoints
transcriber.py # Processes recordings folder
recordings/ # Place your audio files here
transcripts/ # Generated transcripts
.env # Environment variables
requirements.txt # Python dependencies


---

## Requirements
- Python 3.9+
- FastAPI
- Uvicorn
- requests
- AssemblyAI API Key

Install dependencies:
```bash
pip install -r requirements.txt


Usage
Environment Variables
Create a .env file in the project root with:ASSEMBLYAI_API_KEY=your_api_key_here

Usage
1. Place Audio Files
Put your .mp3 or .wav files in:recordings/

Start the Server
uvicorn app.main:app --reload

3. Trigger Transcription
Send a POST request to:POST http://127.0.0.1:8000/transcribe/

Output
Transcripts will be saved in:transcripts/



