import requests
import http.client
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

    print(data.decode("utf-8"))
Futbol()