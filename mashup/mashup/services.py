import requests
import http.client
import json
from django.http import JsonResponse
def Drivers():
    url = "https://f1connectapi.vercel.app/api/current/drivers"

    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        drivers_list=data.get('drivers',[])
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
    for noticia in responseJson['noticias']:
        news.append({
            'titulo': noticia['titulo'],
            'nota': noticia['Nota'],
            'img': noticia['Foto']
        })
    return news

    

Noticias()