from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import subprocess
import uuid
import os
import requests
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

    selected_format = format_id if format_id else "best[ext=mp4]"

    try:
        subprocess.run([
            "yt-dlp",
            "-f", selected_format,
            "-o", output_path,
            url
        ], check=True)
    except subprocess.CalledProcessError:
        return JSONResponse(content={"error": "Download failed"}, status_code=500)

    # GoFile এ আপলোড
    with open(output_path, "rb") as f:
        response = requests.post("https://store1.gofile.io/uploadFile", files={"file": f})

    if response.status_code != 200:
        return JSONResponse(content={"error": "Upload failed"}, status_code=500)

    data = response.json()
    direct_url = data["data"]["downloadPage"]
    title = os.path.basename(output_path).replace(".mp4", "")

    return {
        "direct_url": direct_url,
        "title": title
    }