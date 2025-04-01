from django.shortcuts import render
import requests
from django.conf import settings
from .services import *
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

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

@require_http_methods(["GET"])
def search(request):
    query = request.GET.get('q', '').lower()
    
    # Get all data
    drivers = Drivers()
    partidos = Futbol()
    news = Noticias()
    
    # Search in drivers
    drivers_results = []
    if drivers:
        for driver in drivers:
            full_name = f"{driver['name']} {driver['surname']}".lower()
            if query in full_name or query in driver.get('nationality', '').lower():
                drivers_results.append({
                    'type': 'driver',
                    'name': f"{driver['name']} {driver['surname']}",
                    'nationality': driver.get('nationality', ''),
                    'image_url': driver.get('image_url', ''),
                    'team': driver.get('teamId', '')
                })
    
    # Search in football matches
    football_results = []
    if partidos:
        for partido in partidos:
            if query in partido['local'].lower() or query in partido['visit'].lower():
                football_results.append({
                    'type': 'match',
                    'local': partido['local'],
                    'visit': partido['visit'],
                    'localImg': partido['localImg'],
                    'visitImg': partido['visitImg'],
                    'date': partido['date'],
                    'score': f"{partido['goleslocal']} : {partido['golesvisitante']}"
                })
    
    # Search in news
  
    news_results = []
    if news:
        for new in news:
            if query in new['titulo'].lower() or query in new['nota'].lower():
                news_results.append({
                    'type': 'news',
                    'title': new['titulo'],
                    'content': new['nota'],
                    'image': new['img']
                })
    
    return JsonResponse({
        'drivers': drivers_results,
        'matches': football_results,
        'news': news_results
    })
