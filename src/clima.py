import os
import requests
from utils import box, success, error
from errores import CiudadNoEncontradaError, ConexionClimaError, APIKeyMissingError

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def consultar_clima(usuario: str):
    """
    Consulta la API y devuelve:
    ciudad, temp (°C), condición, humedad (%), viento (km/h)
    """
    box("CONSULTA DE CLIMA")
    api_key = os.getenv("OPENWEATHER_API_KEY", "").strip()
    if not api_key:
        raise APIKeyMissingError("Define OPENWEATHER_API_KEY en tu entorno.")

    ciudad = input("⎮ 🗺 Ciudad (vacío = Buenos Aires): ").strip() or "Buenos Aires"
    params = {"q": ciudad, "appid": api_key, "units": "metric", "lang": "es"}

    try:
        resp = requests.get(BASE_URL, params=params, timeout=10)
        resp.raise_for_status()
    except Exception as e:
        raise ConexionClimaError(f"Error al conectar con el servicio de clima: {e}")

    data = resp.json()
    temperatura = data["main"]["temp"]
    condicion   = data["weather"][0]["main"]
    descripcion = data["weather"][0].get("description", "")
    humedad     = data["main"].get("humidity", 0)
    viento_ms   = data.get("wind", {}).get("speed", 0.0)
    viento_kmh  = round(viento_ms * 3.6, 1)

    # Informe por consola (mismo formato que el original)
    print("─" * 40)
    print("⎮")
    print(f"⎮ 🗺 Ciudad:           {ciudad}")
    print("⎮")
    print(f"⎮ 🌡 Temperatura (°C):  {temperatura}")
    print("⎮")
    print(f"⎮ 💧 Humedad (%):       {humedad}")
    print("⎮")
    print(f"⎮ 🌬 Viento (km/h):     {viento_kmh}")
    print("⎮")
    print(f"⎮ ☁️  Condición:         {condicion} – {descripcion}")
    print("⎮")
    print("─" * 40)
    print()

    return ciudad, temperatura, condicion, humedad, viento_kmh
