import yt_dlp
import os
from vidapp.models import Video
from django.core.files import File

"""
file related docs in this class can be find here:
https://docs.djangoproject.com/en/5.2/ref/files/file/
"""

class PP_Store_To_GCS(yt_dlp.postprocessor.PostProcessor):
    def run(self, info):
        filepath = info.get('filepath')

        if not filepath or not os.path.exists(filepath):
            return [], info
        video = Video.objects.create()
        video.youtube_url = info.get('webpage_url')
        video.youtube_id = info.get('id')
        video.title = info.get('title')
        video.channel_title = info.get('chennel') or info.get('uploader')
        video.published_at = info.get('upload_date')
        video.duration_sec = info.get('duration')

        with open(filepath, 'rb') as vp:
            video.source_video.save(filepath, File(vp), save=False)

        try:
            os.remove(filepath)
        except Exception:
            pass

        return [], info


