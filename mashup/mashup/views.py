from django.shortcuts import render
import requests
from django.conf import settings
from .services import *

def index(request):
    drivers = Drivers()
    return render(request, "index.html",{'drivers':drivers})

