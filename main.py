from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import yt_dlp

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/formats")
def get_formats(url: str = Query(...)):
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        formats = [
            {
                "format_id": f["format_id"],
                "ext": f["ext"],
                "format_note": f.get("format_note", ""),
                "filesize": f.get("filesize", 0),
                "resolution": f.get("resolution", "")
            }
            for f in info["formats"]
            if f.get("ext") in ["mp4", "webm", "m4a"]
        ]
        return {"title": info.get("title"), "formats": formats}

@app.get("/download")
def get_direct_url(url: str, format_id: str):
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'format': format_id
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return {"title": info.get("title"), "direct_url": info["url"]}