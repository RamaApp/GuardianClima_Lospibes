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

def register_user() -> str:
    """Pide usuario/clave, valida, sugiere mejoras y auto-loguea."""
    print()
    box("REGISTRO DE USUARIO")
    print()
    users = load_users()

    username = input("⎯⎯⇥ Nombre de usuario: ").strip()
    if username in users:
        error("⎯⎯ Ese usuario ya existe ⎯⎯.")
        print()
        return ""

    password = input("⌲ Contraseña: ").strip()
    errs = validate_password(password)
    if errs:
        error("Contraseña inválida por las siguientes razones:")
        for e in errs:
            print(f"   • {e}")
        # Sugerencias
        recomendaciones = []
        if "Debe tener al menos 8 caracteres" in errs:
            recomendaciones.append("usar ≥8 caracteres")
        if "Debe incluir al menos una letra mayúscula" in errs:
            recomendaciones.append("incluir letras MAYÚSCULAS")
        if "Debe incluir al menos un dígito" in errs:
            recomendaciones.append("añadir números (0-9)")
        if "Debe incluir al menos un carácter especial" in errs:
            recomendaciones.append("añadir símbolos (!@#…)")
        if recomendaciones:
            print()
            print("Para una contraseña más segura, considera:",
                  "; ".join(recomendaciones) + ".")
        print()
        return ""

    with open(USERS_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([username, password])

    print()
    success(f"Usuario '{username}' registrado con éxito.")
    print()
    print("Te conecto automáticamente…")
    print()
    return username

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
            box("SESIÓN INICIADA CON ÉXITO")
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
