from django.shortcuts import render
import requests
from django.conf import settings
from .services import *

def index(request):
    drivers = Drivers()
    partidos = Futbol()
    news = Noticias()

    context = {
        'drivers': drivers,
        'partidos': partidos,
        'news': news
    }
    
    return render(request, "index.html", context)
