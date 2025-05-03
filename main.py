from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
import subprocess
import uuid
import os
from typing import Optional

app = FastAPI()

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

@app.get("/download")
def download_video(
    url: str = Query(..., description="YouTube video URL"),
    format_id: Optional[str] = Query(None, description="Optional format ID (e.g. 18, 22)")
):
    video_id = str(uuid.uuid4())
    output_path = os.path.join(DOWNLOAD_DIR, f"{video_id}.mp4")

    # যদি format_id না পাঠানো হয়, তাহলে default best mp4
    selected_format = format_id if format_id else "best[ext=mp4]"

    try:
        subprocess.run([
            "yt-dlp",
            "-f", selected_format,
            "-o", output_path,
            url
        ], check=True)
    except subprocess.CalledProcessError:
        return {"error": "Download failed"}

    return FileResponse(
        path=output_path,
        filename="video.mp4",
        media_type="video/mp4"
    )