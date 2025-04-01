import requests
import http.client
import json
from django.http import JsonResponse

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

def Drivers():
    url = "https://f1connectapi.vercel.app/api/current/drivers"

    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        drivers_list = data.get('drivers',[])
        # Agregar la URL de la imagen a cada conductor

        for driver in drivers_list:
            driver['image_url'] = get_driver_image(f"{driver['name']} {driver['surname']}")
        return drivers_list
    else:
        return None

def Futbol():
    conn = http.client.HTTPSConnection("v3.football.api-sports.io")

    headers = {
        'x-rapidapi-host': "v3.football.api-sports.io",
        'x-rapidapi-key': "ef11f29081cb7e476852aa0a039679df"
        }

    conn.request("GET", "/fixtures?league=39&season=2023", headers=headers)

    res = conn.getresponse()
    data = res.read()
    i = 0
    data = json.loads(data)
    fixtures  = []
    for fixture in data['response']:
        fixtures.append({
            'local': fixture['teams']['home']['name'],
            'visit': fixture['teams']['away']['name'],
            'localImg': fixture['teams']['home']['logo'],
            'visitImg': fixture['teams']['away']['logo'],
            'date': fixture['fixture']['date'],
            'goleslocal': fixture['goals']['home'],
            'golesvisitante': fixture['goals']['away']
        })
        i += 1
        if i == 6:
            break
  

    return fixtures

def Noticias():
    url = 'https://magicloops.dev/api/loop/49bdee03-4f9e-4f3d-a146-79f6d8fbee82/run'
    payload = {}

    response = requests.get(url, json=payload)
    responseJson = response.json()
    news= []
    i = 0
    for new in responseJson['noticias']:
        news.append({
            'titulo': new['titulo'],
            'nota': new['Nota'],
            'img': new['Foto']
        })
        i += 1
        if i == 8:
            break

    return news
