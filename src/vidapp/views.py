from django.shortcuts import render, redirect
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
            return redirect("progress", {'url' : url})
    else:
        form = UrlForm()
        return render(request, 'vidapp/home.html', {'form' : form})

def progress(request, url:str):
    yt_download.delay(url)
    return HttpResponse('thanks')
    
