from auth import register_user, login_user
from clima import consultar_clima
from historial import ver_historial, HISTORIAL_CSV
from estadisticas import mostrar_estadisticas
from ia import obtener_consejo

from utils import box, error
from errores import APIKeyMissingError, CiudadNoEncontradaError, ConexionClimaError, ConexionIAError

import csv
from datetime import datetime

def mostrar_menu_acceso():
    print()
    box("=== GUARDIÁNCLIMA ITBA ===")
    print()
    print("1) Iniciar Sesión")
    print()
    print("2) Registrar Usuario")
    print()
    print("3) Salir")
    print()

def mostrar_menu_principal(username: str):
    print()
    box(f"¡Hola, {username}!")
    print()
    print("1) Consultar clima y guardar en historial")
    print()
    print("2) Ver historial personal")
    print()
    print("3) Ver estadísticas globales")
    print()
    print("4) Obtener consejo de vestimenta (IA)")
    print()
    print("5) Acerca de…")
    print()
    print("6) Cerrar sesión")
    print()

def mostrar_acerca_de():
    print()
    box("ACERCA DE GUARDIÁNCLIMA ITBA")
    print()
    print("Aplicación de consola en Python para consultar clima,")
    print("guardar historial, generar estadísticas y consejos con IA.")
    print()
    print("🛠 Módulos internos:")
    print(" • auth.py: simulación de usuarios y validación de contraseñas.")
    print(" • clima.py: consumo de OpenWeatherMap y normalización de datos.")
    print(" • historial.py y estadisticas.py: gestión y análisis de CSV.")
    print(" • ia.py: integración con Google Gemini para consejos.")
    print()
    print("⚠️ Simulación insegura: las contraseñas se guardan en texto plano.")
    print("En entornos reales, usar hashing (bcrypt, Argon2, etc.).")
    print()
    print("👥 Desarrolladores: Ramiro Appezzato, Maximo Acconcia, Bautista Chiarella, Emiliano Fandiño, Agustin Godoy")
    print("🏷 Nombre de grupo: Equipo 104 GuardianClima ITBA")
    print()

def main():
    usuario_actual = ""
    while True:
        if not usuario_actual:
            mostrar_menu_acceso()
            opcion = input("Elige una opción: ").strip()

            if opcion == "1":
                usuario_actual = login_user()

            elif opcion == "2":
                nuevo = register_user()
                if nuevo:
                    usuario_actual = nuevo

            elif opcion == "3":
                print()
                box("¡Hasta pronto!")
                break

            else:
                print("Opción inválida.")

        else:
            mostrar_menu_principal(usuario_actual)
            opcion = input("Elige una opción: ").strip()

            if opcion == "1":
                try:
                    ciudad, temp, cond, hum, viento = consultar_clima(usuario_actual)
                except (APIKeyMissingError, CiudadNoEncontradaError, ConexionClimaError) as e:
                    error(str(e))
                    continue
                # — Guardar en historial global —
                with open(HISTORIAL_CSV, "a", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow([
                        usuario_actual,
                        ciudad,
                        datetime.now().isoformat(sep=" "),
                        temp,
                        cond,
                        hum,
                        viento
                    ])

            elif opcion == "2":
                ver_historial(usuario_actual)

            elif opcion == "3":
                mostrar_estadisticas()

            elif opcion == "4":
                try:
                    ciudad, temp, cond, hum, viento = consultar_clima(usuario_actual)
                except (APIKeyMissingError, CiudadNoEncontradaError, ConexionClimaError) as e:
                    error(str(e))
                    continue
                try:
                    consejo = obtener_consejo(ciudad, temp, cond)
                except ConexionIAError as e:
                    error(str(e))
                    continue
                print()
                box("Consejo de vestimenta:")
                print(consejo)
                print()

            elif opcion == "5":
                mostrar_acerca_de()

            elif opcion == "6":
                print()
                box(f"Cerrando sesión de {usuario_actual}")
                usuario_actual = ""

            else:
                print("Opción inválida.")

if __name__ == "__main__":
    main()
