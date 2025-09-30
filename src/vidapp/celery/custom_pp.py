import os
from vidapp.models import Video
from django.core.files import File
from yt_dlp.postprocessor.common import PostProcessor
import subprocess
from typing import Optional
from datetime import date, datetime
"""
file related docs in this class can be find here:
https://docs.djangoproject.com/en/5.2/ref/files/file/
"""

class PP_Store_To_GCS(PostProcessor):
    def __init__(self, downloader, **kwargs):
        super().__init__(downloader)   # ← important
        self.kwargs = kwargs           # optional

    #this method will create a path for wav file and convert .mp4 to .wav and save into the wavpath
    def convert_to_wav(self, vidpath : str) -> Optional[str]:
        #creating a path for wav audio
        base, _ = os.path.splitext(vidpath)
        wavpath = base + '.wav'
        cmd = ["ffmpeg", "-y", "-i", vidpath, "-acodec", "pcm_s16le", "-ac", "2", "-ar", "44100", wavpath]
        try:
            subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            wavpath = None
        return wavpath
    
    #upload_date field in the model accepts datetimefield, so this method, will convert the string to datettime.date
    def standard_upload_date(self, upload_date : str | None) -> Optional[date]:
        try:
            return datetime.strptime(upload_date, '%Y%m%d').date()
        except:
            return None
    
    def run(self, info):
        #extracting video path from yt-dlp info that contain video information
        vidpath = info.get('filepath')

        #check if the filepath exist and is valid
        if not vidpath or not os.path.exists(vidpath):
            return [], info

        #create an instance of Video model and pass video metadata
        up_date = self.standard_upload_date(info.get('upload_date')) #convert string to datetime.date
        video = Video.objects.create(
            youtube_url = info.get('webpage_url'),
            youtube_id = info.get('id'),
            title = info.get('title'),
            channel_title = info.get('channel') or info.get('uploader') or '',
            published_at = up_date,
            duration_sec = info.get('duration') or 0,
        )

        #open the filepath to access downloaded video inside the tempdir
        with open(vidpath, 'rb') as vp:
            vidname = os.path.basename(vidpath) #selecting just the basename of the filepath, don't need temp/tmpABC
            video.source_video.save(vidname, File(vp), save=False) #store the video in the GCS

        wavpath = self.convert_to_wav(vidpath)
        if wavpath and os.path.exists(wavpath):
            with open(wavpath, 'rb') as wp:
                wavname = os.path.basename(wavpath)
                video.wav_audio.save(wavname, File(wp), save=False)
            
        video.save()

        #to have access to added instance, we add primary key to yt-dlp info dictionary
        video_pk = {'video_pk' : video.pk}
        info.update(video_pk)

        #remove temporary directories and downloaded video
        try:
            os.remove(vidpath)
        except OSError:
            pass

        try:
            os.remove(wavpath)
        except OSError:
            pass
        return [], info


