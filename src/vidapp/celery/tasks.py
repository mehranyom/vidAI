from celery import shared_task
import yt_dlp
import os
from typing import Optional
from collections.abc import Mapping
from .custom_pp import PP_Store_To_GCS
import tempfile


@shared_task
def yt_download(url : str) -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        ydl_opts = {
            'quiet' : True,
            'verbose' : False,
            'noplaylist' : True,
            'skip_download' : True,
            'no_warnings' : True,
            'format' : 'bestvideo*+bestaudio/best',
            'merge_output_format' : 'mp4',
            'outtmpl' : os.path.join(tmpdir, '%(title)s-%(id)s.%(ext)s'),
            'noplaylist': True,
            'skip_download' : False,
            "http_headers": {                    # real browser headers
                        "User-Agent": ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/124.0.0.0 Safari/537.36"),
                        "Accept-Language": "en-US,en;q=0.9",
    },
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.add_post_processor(PP_Store_To_GCS(ydl))
            ydl.extract_info(url, download=True)