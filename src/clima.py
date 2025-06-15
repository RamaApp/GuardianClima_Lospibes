import os
import requests
from utils import box, success, error
from errores import (
    CiudadNoEncontradaError,
    ConexionClimaError,
    APIKeyMissingError
)


# URL base de OpenWeatherMap
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def consultar_clima(usuario: str):
    """
    Pide al usuario una ciudad, consulta la API de OpenWeather,
    muestra un informe más completo y devuelve (ciudad, temperatura, condición).
    """
    box("CONSULTA DE CLIMA")
    api_key = os.getenv("OPENWEATHER_API_KEY", "").strip()
    if not api_key:
        error("⎮ ❌ Define OPENWEATHER_API_KEY en tu entorno.")
        return None

    ciudad = input("⎮ 🗺 Ciudad (vacío = Buenos Aires): ").strip() or "Buenos Aires"
    params = {
        "q": ciudad,
        "appid": api_key,
        "units": "metric",
        "lang": "es"
    }

    try:
        resp = requests.get(BASE_URL, params=params, timeout=10)
        resp.raise_for_status()
    except Exception as e:
        error("Error al llamar al servicio de clima:")
        print(f"  {e}")
        return None

    data = resp.json()
    # Campos principales
    temperatura = data["main"]["temp"]
    feels_like  = data["main"].get("feels_like")
    humedad     = data["main"].get("humidity")
    presion     = data["main"].get("pressure")
    condicion   = data["weather"][0]["main"]
    descripcion = data["weather"][0].get("description")
    viento      = data.get("wind", {})
    vel_viento  = viento.get("speed")
    dir_viento  = viento.get("deg")

    # Informe por consola
    print("─" * 40)
    print("⎮")
    print(f"⎮ 🗺 Ciudad:           {ciudad}")
    print("⎮")
    print(f"⎮ 🌡 Temperatura (°C):  {temperatura}")
    print("⎮")
    print(f"⎮ 🤗 Sensación (°C):    {feels_like}")
    print("⎮")
    print(f"⎮ 💧 Humedad (%):       {humedad}")
    print("⎮")
    print(f"⎮ 🔽 Presión (hPa):     {presion}")
    print("⎮")
    print(f"⎮ 🌬 Viento (m/s):      {vel_viento} ({dir_viento}°)")
    print("⎮")
    print(f"⎮ 🌥 Condición:         {condicion} – {descripcion}")
    print("⎮")
    print("─" * 40)
    print()

    # Devuelve solo los 3 campos originales para compatibilidad
    return ciudad, temperatura, condicion
