# main.py

from fastapi import FastAPI
from app.transcriber import transcribe_all_files


app = FastAPI()

@app.post("/transcribe/")
def transcribe():
    output_files = transcribe_all_files()
    return {"message": "Transcription completed", "files": output_files}
