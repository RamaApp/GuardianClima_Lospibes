# src/historial.py

import os
import csv
from utils import box, error

HISTORIAL_CSV = os.path.join(
    os.path.dirname(__file__),
    os.pardir,
    "data",
    "historial_global.csv"
)

def ver_historial(usuario_actual: str):
    """
    Muestra tu historial personal de consultas (o de todos si usuario_actual==""), 
    leyendo data/historial_global.csv.
    """
    if not os.path.exists(HISTORIAL_CSV):
        error("No hay historial personal para mostrar.")
        print()
        return

    # Lee todo y luego selecciona filas que empiecen el usuario (o todas)
    with open(HISTORIAL_CSV, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = [r for r in reader if r and (usuario_actual == "" or r[0] == usuario_actual)]

    if not rows:
        error("No encontré entradas para ese usuario.")
        print()
        return

    # Imprime cada fila adaptando al número de columnas
    box("HISTORIAL PERSONAL")
    for row in rows:
        # asegura al menos 5 columnas
        usr = row[0]
        ciu = row[1] if len(row) > 1 else ""
        ts  = row[2] if len(row) > 2 else ""
        temp= row[3] if len(row) > 3 else ""
        cond= row[4] if len(row) > 4 else ""

        # campos opcionales (humedad, descripción, viento) ya no se usan o pueden imprimirse si existen
        hum = row[5] if len(row) > 5 else ""
        desc= row[6] if len(row) > 6 else ""
        viento = row[7] if len(row) > 7 else ""

        print()
        print(f"👤 Usuario : {usr}")
        print()
        print(f"🏙️ Ciudad  : {ciu}")
        print()
        print(f"⏱️ Fecha   : {ts}")
        print()
        print(f"🌡 Temperatura: {temp}°C")
        print()
        print(f"☁️  Clima    : {cond}")
        print()
        if hum:
            print(f"💧 Humedad : {hum}%")
        if desc:
            print(f"📝 Desc    : {desc}")
        if viento:
            print(f"💨 Viento  : {viento}")
        print("-" * 30)
    print()