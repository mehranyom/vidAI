from celery import shared_task
import yt_dlp
import os
from typing import Optional
from collections.abc import Mapping
from .custom_pp import PP_Store_To_GCS


def yt_extract_meta_data(url: str) -> Optional[Mapping]:
    ydl_opts = {
        'quite' : True,
        'verbose' : False,
        'noplaylist' : True,
        'skip_download' : True,
        'no_warnings' : True
    }
    

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    return {
        'youtube_url' : url,
        'youtube_id' : info.get('id'),
        'title' : info.get('title'),
        'channel_title' : info.get('channel') or info.get('uploader'),
        "published_at": info.get("upload_date"),  # 'YYYYMMDD' or None
        "duration_sec": float(info.get("duration") or 0.0),
        "ext": info.get("ext"),
    }

@shared_task
def yt_download(url : str) -> None:
    ydl_opts = {
        'quite' : True,
        'verbose' : False,
        'noplaylist' : True,
        'skip_download' : True,
        'no_warnings' : True
    }