from django.shortcuts import render
from django.http import HttpResponse
from .forms import UrlForm
from .celery.tasks import yt_download
from .models import Video

# Create your views here.

def index(request):
    if request.method == 'POST':
        s_form = UrlForm(request.POST)
        
        if s_form.is_valid():
            url = s_form.data.get('youtube_url')
            yt_download.delay(url)
            return HttpResponse('thanks')
    else:
        form = UrlForm()
        return render(request, 'vidapp/home.html', {'form' : form})


    
