from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import os
from utils.ffmpeg_utils import video_to_gif

app = FastAPI()

UPLOAD_DIR = "uploads/"
OUTPUT_DIR = "output/"

# Create directories if missing
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


@app.post("/video-to-gif", status_code=201)
async def convert_video_to_gif(file: UploadFile = File(...)):
    # Validate file type
    if not file.filename.lower().endswith((".mp4", ".mov", ".avi", ".mkv")):
        raise HTTPException(
            status_code=400,
            detail="Invalid file format. Only video files are allowed."
        )

    try:
        # Save the uploaded video
        input_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(input_path, "wb") as f:
            f.write(await file.read())

        # Output GIF path
        gif_path = os.path.join(OUTPUT_DIR, file.filename + ".gif")

        # Convert using FFmpeg
        result_path = video_to_gif(input_path, gif_path)

        return JSONResponse(
            status_code=201,
            content={
                "status": "success",
                "gif_path": result_path
            }
        )

    except FileNotFoundError:
        raise HTTPException(
            status_code=500,
            detail="Server error while saving the file."
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Conversion failed: {str(e)}"
        )

