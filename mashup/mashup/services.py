import requests

def Drivers():
    url = "https://f1connectapi.vercel.app/api/current/drivers"

    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        drivers_list=data.get('drivers',[])
        return drivers_list
    else:
        return None
