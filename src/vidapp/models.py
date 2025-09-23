from django.db import models
import uuid
from pathlib import Path
from django.utils import timezone

# Create your models here.

def user_directory_path(instanse, filename):
    ts = timezone.now()
    ext = Path(filename).suffix
    return f"{getattr(instanse, 'user_id', 'annon')}/{ts:%Y/%m}/{uuid.uuid4().hex}{ext}"


class RM(models.Model):
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to=user_directory_path)
    ipload_at = models.DateTimeField(auto_now_add=True)