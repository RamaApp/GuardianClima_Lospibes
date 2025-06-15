# src/ia.py

import os
import re
from pathlib import Path

# 1) dotenv para cargar GEMINI_API_KEY
from dotenv import load_dotenv

# 2) SDK Gemini
import google.generativeai as genai

from errores import ConexionIAError, APIKeyMissingError

# Carga de .env
project_root = Path(__file__).parent.parent
dotenv_path = project_root / ".env"
if dotenv_path.exists():
    load_dotenv(dotenv_path=dotenv_path)
else:
    print(f"⚠️ No encontré {dotenv_path}. Revisá que exista tu archivo .env")

# Configura la API key
api_key = os.getenv("GEMINI_API_KEY", "").strip()
if not api_key:
    raise APIKeyMissingError("Define GEMINI_API_KEY en tu .env o en las variables de entorno.")
genai.configure(api_key=api_key)

# Instancia correcta del modelo
model = genai.GenerativeModel("gemini-2.0-flash")

def obtener_consejo(ciudad: str, temperatura: float, condicion: str) -> str:
    """
    Genera un consejo ultra-conciso (5 viñetas máx.) para el clima dado.
    Si la IA falla, devuelve un consejo estático de respaldo.
    """
    descripcion = f"{temperatura}°C y {condicion} en {ciudad}"
    prompt = (
        f"Dame un consejo de vestimenta para {descripcion}. "
        "Resume en 5 viñetas como máximo, conciso y directo, "
        "sin introducciones ni despedidas."
    )

    try:
        response = model.generate_content(content=[prompt])
        texto = response.text.strip()
        texto = texto.replace("*", "")
        texto = re.sub(r"\n{2,}", "\n", texto)

        bullets = []
        for line in texto.split("\n"):
            l = line.strip()
            if not l:
                continue
            if not re.match(r"^[-•*]\s+", l):
                l = f"- {l}"
            bullets.append(l)

        return "\n".join(bullets[:5])

    except Exception:
        # Consejo de respaldo
        return "\n".join([
            "- Usa un impermeable ligero para la llovizna",
            "- Viste en capas: remera manga larga + suéter fino",
            "- Pantalones resistentes que no se ensucien",
            "- Calzado impermeable para mantener pies secos",
            "- Lleva paraguas o piloto y accesorios (bufanda/gorro)"
        ])


# Solo para pruebas rápidas (no se ejecuta cuando importas desde main.py)
if __name__ == "__main__":
    print(obtener_consejo("Buenos Aires", 10.34, "llovizna"))
