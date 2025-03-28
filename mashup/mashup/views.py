from django.shortcuts import render
import requests
from django.conf import settings

def index(request):
    # Aquí puedes agregar la URL de la API que quieras consumir
    api_url = "https://api.example.com/data"  # Reemplaza con tu API
    
    try:
        # Realizar la petición a la API
        response = requests.get(api_url)
        response.raise_for_status()  # Lanza una excepción si hay error HTTP
        
        # Convertir la respuesta a JSON
        data = response.json()
        
        # Pasar los datos al template
        context = {
            'data': data
        }
    except requests.RequestException as e:
        # Manejar errores de la API
        context = {
            'error': f"Error al obtener datos: {str(e)}",
            'data': None
        }
    
    return render(request, "index.html", context)

