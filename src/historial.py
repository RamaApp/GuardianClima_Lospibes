import os
import csv
from utils import box, error

HISTORIAL_CSV = os.path.join(os.path.dirname(__file__), os.pardir, "data", "historial_global.csv")

def ver_historial(usuario_actual: str):
    """
    Muestra tu historial personal solicitando ciudad y filtrando.
    Soporta filas antiguas con sólo 5 columnas rellenando humedad y viento como cadenas vacías.
    """
    if not os.path.exists(HISTORIAL_CSV):
        error("No hay historial global para mostrar.")
        print()
        return

    ciudad_filtro = input("Ciudad para filtrar (vacío = todas): ").strip().lower()

    with open(HISTORIAL_CSV, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = []
        for r in reader:
            if not r or r[0] != usuario_actual:
                continue
            if ciudad_filtro and (len(r) < 2 or r[1].lower() != ciudad_filtro):
                continue
            # Si la fila tiene menos de 7 campos, la rellenamos
            if len(r) < 7:
                r = r + [""] * (7 - len(r))
            rows.append(r)

    if not rows:
        error("No encontré entradas para ese usuario/ciudad.")
        print()
        return

    print()
    box("HISTORIAL PERSONAL")
    for row in rows:
        usr, ciu, ts, temp, cond, hum, viento = row
        print()
        print(f"👤 Usuario : {usr}")
        print()
        print(f"🏙️ Ciudad  : {ciu}")
        print()
        print(f"⏱️ Fecha   : {ts}")
        print()
        print(f"🌡 Temp    : {temp}°C")
        print()
        print(f"☁️  Clima  : {cond}")
        print()
        # Si humedad o viento estaban vacíos, simplemente se muestran en blanco
        print(f"💧 Humedad : {hum}" + ("" if hum == "" else "%"))
        print()
        print(f"🌬 Viento  : {viento}" + ("" if viento == "" else " km/h"))
        print()
        print("-" * 30)
    print()
