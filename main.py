from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import os
import uuid
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
        # ----------- 1. Generate safe unique file names -----------
        input_ext = file.filename.split(".")[-1]
        input_filename = f"{uuid.uuid4()}.{input_ext}"
        output_filename = f"{uuid.uuid4()}.gif"

        input_path = os.path.join(UPLOAD_DIR, input_filename)
        gif_path = os.path.join(OUTPUT_DIR, output_filename)

        # ----------- 2. Save uploaded file -----------
        with open(input_path, "wb") as f:
            f.write(await file.read())

        # ----------- 3. Convert video -> GIF -----------
        video_to_gif(input_path, gif_path)

        # ----------- 4. Return GIF file directly -----------
        return FileResponse(
            gif_path,
            media_type="image/gif",
            filename=output_filename
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Conversion failed: {str(e)}"
        )

