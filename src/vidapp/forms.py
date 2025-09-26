from .models import Video
from django.forms import ModelForm

class UrlForm(ModelForm):
    class Meta:
        model = Video
        fields = ['youtube_url']