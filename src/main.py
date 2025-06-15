# src/main.py

from auth import register_user, login_user
from clima import consultar_clima
from historial import ver_historial
from estadisticas import mostrar_estadisticas
from ia import obtener_consejo

from utils import box, error
from errores import (
    MaxLoginAttemptsError,
    APIKeyMissingError,
    CiudadNoEncontradaError,
    ConexionClimaError,
    ConexionIAError
)

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
    print("5) Cerrar sesión")
    print()
    

def main():
    usuario_actual = ""
    while True:
        if not usuario_actual:
            mostrar_menu_acceso()
            opcion = input("Elige una opción: ").strip()

            if opcion == "1":
                try:
                    usuario_actual = login_user()
                except MaxLoginAttemptsError as e:
                    error(str(e))

            elif opcion == "2":
                register_user()

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
                    ciudad, temp, cond = consultar_clima(usuario_actual)
                except APIKeyMissingError as e:
                    error(str(e))
                except CiudadNoEncontradaError as e:
                    error(str(e))
                except ConexionClimaError as e:
                    error(str(e))
                else:
                    # Aquí podrías guardar en historial si lo deseas
                    pass

            elif opcion == "2":
                ver_historial(usuario_actual)

            elif opcion == "3":
                mostrar_estadisticas()

            elif opcion == "4":
                # Primero, vuelvo a consultar el clima para tener datos actualizados
                try:
                    ciudad, temp, cond = consultar_clima(usuario_actual)
                except (APIKeyMissingError, CiudadNoEncontradaError, ConexionClimaError) as e:
                    error(str(e))
                    continue

                # Luego, obtengo el consejo de IA
                try:
                    consejo = obtener_consejo(ciudad, temp, cond)
                except ConexionIAError as e:
                    error(str(e))
                else:
                    print()
                    box("Consejo de vestimenta:")
                    print(consejo)

            elif opcion == "5":
                print()
                box(f"Cerrando sesión de {usuario_actual}")
                usuario_actual = ""

            else:
                print("Opción inválida.")

if __name__ == "__main__":
    main()
