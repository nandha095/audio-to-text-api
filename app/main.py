# main.py
import os
from fastapi import FastAPI, HTTPException, status
from app.transcriber import transcribe_unconverted_files
from fastapi.responses import FileResponse
from apscheduler.schedulers.background import BackgroundScheduler

app = FastAPI(title="Audio Transcription Service", version="1.0")

# Scheduler Setup
scheduler = BackgroundScheduler()

def scheduled_task():
    print("Checking for unconverted files...")
    transcribe_unconverted_files()

# Run every 5 minutes
scheduler.add_job(scheduled_task, "interval", minutes=1)
scheduler.start()

# Run immediately at startup
@app.on_event("startup")
def startup_event():
    print("Running initial transcription check...")
    transcribe_unconverted_files()


@app.post("/transcribe/", status_code=status.HTTP_200_OK)
def transcribe():
    """
    Manually trigger transcription of unconverted audio files.
    """
    try:
        output_files = transcribe_unconverted_files()
        if not output_files:
            return {
                "status": "success",
                "message": "No new recordings to transcribe",
                "files": []
            }
        return {
            "status": "success",
            "message": "Transcription completed",
            "files": output_files
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Transcription failed: {str(e)}"
        )


@app.get("/download/{filename}")
def download_file(filename: str):
    """
    Download a transcript file by filename.
    """
    file_path = os.path.join("transcripts", filename)
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"File '{filename}' not found in transcripts folder"
        )

    return FileResponse(
        file_path,
        media_type="text/plain",
        filename=filename,
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
