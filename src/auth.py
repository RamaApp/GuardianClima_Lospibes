import csv
import os
import re
from typing import Dict, List
from utils import box, success, error
from errores import MaxLoginAttemptsError

USERS_CSV = os.path.join(os.path.dirname(__file__), os.pardir, "data", "usuarios_simulados.csv")

def load_users() -> Dict[str, str]:
    """Carga el CSV de usuarios en un dict {username: password}."""
    if not os.path.exists(USERS_CSV):
        open(USERS_CSV, "w", encoding="utf-8").close()
    users = {}
    with open(USERS_CSV, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) >= 2:
                users[row[0]] = row[1]
    return users

def validate_password(password: str) -> List[str]:
    """Valida la contraseña con reglas de seguridad, devuelve lista de errores."""
    errors = []
    if len(password) < 8:
        errors.append("Debe tener al menos 8 caracteres")
    if not re.search(r"[A-Z]", password):
        errors.append("Debe incluir al menos una letra mayúscula")
    if not re.search(r"\d", password):
        errors.append("Debe incluir al menos un dígito")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        errors.append("Debe incluir al menos un carácter especial")
    return errors

def register_user():
    """Flujo de registro: pide usuario/clave, valida y escribe en el CSV."""
    print()
    box("REGISTRO DE USUARIO")
    print()
    users = load_users()

    username = input("⎯⎯⇥ Nombre de usuario: ").strip()
    if username in users:
        error("⎯⎯ Ese usuario ya existe ⎯⎯.")
        return

    password = input("⌲ Contraseña: ").strip()
    errs = validate_password(password)
    if errs:
        error("Contraseña inválida por las siguientes razones:")
        for e in errs:
            print(f"   • {e}")
        return

    with open(USERS_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([username, password])
    print()
    success("Usuario registrado con éxito.")
    print()

def login_user() -> str:
    """Flujo de login con hasta 3 intentos; si falla, vuelve al menú principal."""
    print()
    box("INICIO DE SESIÓN")
    print()
    users = load_users()

    attempts = 3
    while attempts > 0:
        username = input("———⇥ Usuario: ").strip()
        password = input("———⇥ Contraseña: ").strip()

        if users.get(username) == password:
            print()
            box("SESION INICIADA CON ÉXITO")
            print()
            success(f"¡Bienvenido, {username}!")
            print()
            return username
        else:
            attempts -= 1
            error(f"Usuario o contraseña incorrectos. Te quedan {attempts} intento(s).")
            print()
    error("Demasiados intentos fallidos. Regresando al menú principal.")
    print()
    return ""

if __name__ == "__main__":
    # Modo prueba 
    while True:
        print()
        box("MODO PRUEBA AUTH")
        print()
        cmd = input("Escribe register / login / exit: ").lower().strip()
        print()
        if cmd == "register":
            register_user()
        elif cmd == "login":
            login_user()
        elif cmd == "exit":
            success("Saliendo del modo prueba.")
            break
        else:
            error("Comando inválido. Usa 'register', 'login' o 'exit'.")
            print()
