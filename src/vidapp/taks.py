from celery import shared_task
from .models import Video
import yt_dlp

@shared_task
def yt_download(url: str):
