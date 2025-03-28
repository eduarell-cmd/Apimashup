import requests

def Drivers():
    url = "https://f1connectapi.vercel.app/api/current/drivers?limit=1"

    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        print(data)
        return data
    else:
        return None

Drivers()