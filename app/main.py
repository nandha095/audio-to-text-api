# app/main.py

from fastapi import FastAPI
from app.transcriber import transcribe_all_files

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Audio-to-Text API is working!"}

@app.post("/transcribe/")
def transcribe():
    result = transcribe_all_files()
    return {"message": "Transcription complete", "files": result}
