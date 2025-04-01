import requests
import http.client
import json
from django.http import JsonResponse
from django.core.cache import cache
from functools import lru_cache
import asyncio
import aiohttp
from datetime import datetime, timedelta

# Cache duration in seconds (5 minutes)
CACHE_DURATION = 300

@lru_cache(maxsize=128)
def get_driver_image(driver_name):
    # Diccionario de mapeo de nombres de corredores a URLs de imágenes
    driver_images = {
        "Max Verstappen": "https://formula1.lne.es/media/pilotos/medium/max-verstappen.jpg?ttt2023",
        "Sergio Pérez": "https://formula1.lne.es/media/pilotos/medium/sergio-perez.jpg?ttt2023",
        "Lewis Hamilton": "https://formula1.lne.es/media/pilotos/medium/lewis-hamilton.jpg?ttt2023",
        "Charles Leclerc": "https://formula1.lne.es/media/pilotos/medium/charles-leclerc.jpg?ttt2023",
        "Carlos Sainz": "https://formula1.lne.es/media/pilotos/medium/carlos-sainz.jpg?ttt2023",
        "Lando Norris": "https://formula1.lne.es/media/pilotos/medium/lando-norris.jpg?ttt2023",
        "Oscar Piastri": "https://formula1.lne.es/media/pilotos/medium/oscar-piastri.jpg?ttt2023",
        "George Russell": "https://formula1.lne.es/media/pilotos/medium/george-russell.jpg?ttt2023",
        "Fernando Alonso": "https://formula1.lne.es/media/pilotos/medium/fernando-alonso.jpg?ttt2023",
        "Lance Stroll": "https://formula1.lne.es/media/pilotos/medium/lance-stroll.jpg?ttt2023",
        "Pierre Gasly": "https://formula1.lne.es/media/pilotos/medium/pierre-gasly.jpg?ttt2023",
        "Esteban Ocon": "https://formula1.lne.es/media/pilotos/medium/esteban-ocon.jpg?ttt2023",
        "Alexander Albon": "https://formula1.lne.es/media/pilotos/medium/alexander-albon.jpg?ttt2023",
        "Logan Sargeant": "https://formula1.lne.es/media/pilotos/medium/logan-sargeant.jpg?ttt2023",
        "Yuki Tsunoda": "https://formula1.lne.es/media/pilotos/medium/yuki-tsunoda.jpg?ttt2023",
        "Daniel Ricciardo": "https://formula1.lne.es/media/pilotos/medium/daniel-ricciardo.jpg?ttt2023",
        "Zhou Guanyu": "https://formula1.lne.es/media/pilotos/medium/zhou-guanyu.jpg?ttt2023",
        "Valtteri Bottas": "https://formula1.lne.es/media/pilotos/medium/valtteri-bottas.jpg?ttt2023",
        "Nico Hulkenberg": "https://formula1.lne.es/media/pilotos/medium/nico-hulkenberg.jpg?ttt2023",
        "Kevin Magnussen": "https://formula1.lne.es/media/pilotos/medium/kevin-magnussen.jpg?ttt2023",
        "Oliver Bearman": None  # Explícitamente marcamos que no tiene imagen
    }
    
    # Si el piloto no está en el diccionario o su valor es None, retornamos None
    return driver_images.get(driver_name)

async def fetch_drivers_data():
    url = "https://f1connectapi.vercel.app/api/current/drivers"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                drivers_list = data.get('drivers', [])
                for driver in drivers_list:
                    driver['image_url'] = get_driver_image(f"{driver['name']} {driver['surname']}")
                return drivers_list
            return None

async def fetch_football_data():
    conn = http.client.HTTPSConnection("v3.football.api-sports.io")
    headers = {
        'x-rapidapi-host': "v3.football.api-sports.io",
        'x-rapidapi-key': "ef11f29081cb7e476852aa0a039679df"
    }
    conn.request("GET", "/fixtures?league=39&season=2023", headers=headers)
    res = conn.getresponse()
    data = json.loads(res.read().decode())
    
    fixtures = []
    for fixture in data['response'][:6]:  # Limit to 6 fixtures directly
        fixtures.append({
            'local': fixture['teams']['home']['name'],
            'visit': fixture['teams']['away']['name'],
            'localImg': fixture['teams']['home']['logo'],
            'visitImg': fixture['teams']['away']['logo'],
            'date': fixture['fixture']['date'],
            'goleslocal': fixture['goals']['home'],
            'golesvisitante': fixture['goals']['away']
        })
    return fixtures

async def fetch_news_data():
    url = 'https://magicloops.dev/api/loop/49bdee03-4f9e-4f3d-a146-79f6d8fbee82/run'
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    # Verificar si la respuesta tiene el formato esperado
                    if isinstance(data, dict):
                        noticias = data.get('noticias', [])
                        if isinstance(noticias, list):
                            return [{
                                'titulo': new.get('titulo', 'Sin título'),
                                'nota': new.get('Nota', 'Sin contenido'),
                                'img': new.get('Foto', '')
                            } for new in noticias[:8]]
                    return []
                return []
    except Exception as e:
        print(f"Error fetching news: {str(e)}")
        return []

def Drivers():
    cache_key = 'drivers_data'
    cached_data = cache.get(cache_key)
    
    if cached_data is None:
        drivers_data = asyncio.run(fetch_drivers_data())
        if drivers_data:
            cache.set(cache_key, drivers_data, CACHE_DURATION)
            return drivers_data
    return cached_data

def Futbol():
    cache_key = 'football_data'
    cached_data = cache.get(cache_key)
    
    if cached_data is None:
        fixtures = asyncio.run(fetch_football_data())
        if fixtures:
            cache.set(cache_key, fixtures, CACHE_DURATION)
            return fixtures
    return cached_data

def Noticias():
    cache_key = 'news_data'
    try:
        cached_data = cache.get(cache_key)
        
        if cached_data is None:
            news = asyncio.run(fetch_news_data())
            if news:
                cache.set(cache_key, news, CACHE_DURATION)
                return news
        return cached_data or []
    except Exception as e:
        print(f"Error in Noticias function: {str(e)}")
        return []

