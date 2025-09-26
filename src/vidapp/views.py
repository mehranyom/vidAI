from django.shortcuts import render
from django.http import HttpResponse
from .forms import UrlForm

# Create your views here.

def index(request):
    form = UrlForm()
    list_ = ['alio', 'mammad']
    return render(request, 'vidapp/home.html', {'form' : form, 'list_' : list_})
