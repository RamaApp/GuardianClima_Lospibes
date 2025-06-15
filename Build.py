
#!/usr/bin/env python3
"""
build.py: Empaqueta tu app en un solo archivo ejecutable,
ignorando el SDK de Google y dev_appserver.py, y
añadiendo src/ al path para que incluya tu paquete utils.
"""

import os
import re
import sys
import PyInstaller.__main__

# Carpetas y archivos a excluir de la búsqueda
EXCLUDE_DIRS = {'google-cloud-sdk', '.venv', 'venv', '__pycache__'}
SKIP_FILES   = {'build.py', 'Build.py', 'dev_appserver.py'}

def find_entry_script(project_dir):
    """Busca recursivamente el primer .py con guardia __main__, saltando EXCLUDE_DIRS y SKIP_FILES."""
    for root, dirs, files in os.walk(project_dir):
        # Filtramos subdirectorios que no queremos recorrer
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS and not d.startswith('.')]
        for fname in files:
            if not fname.endswith('.py') or fname in SKIP_FILES:
                continue
            path = os.path.join(root, fname)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            if re.search(r"if\s+__name__\s*==\s*[\"']__main__[\"']", content):
                return path
    raise FileNotFoundError(
        "No se encontró ningún script con guard `if __name__ == '__main__'`."
    )

def main():
    project_dir = os.path.abspath(os.path.dirname(__file__))

    # 1) Determinar entrypoint: por parámetro o auto-detección
    if len(sys.argv) > 1:
        entry = os.path.abspath(sys.argv[1])
        if not os.path.isfile(entry):
            raise FileNotFoundError(f"El archivo especificado no existe: {entry}")
    else:
        entry = find_entry_script(project_dir)

    rel_entry = os.path.relpath(entry, project_dir)
    print(f"–> Script de entrada: {rel_entry}")

    # 2) Recolectar .csv y .env en la raíz
    data_files = [f for f in os.listdir(project_dir) if f.endswith('.csv') or f == '.env']
    sep = os.pathsep  # ":" en macOS/Linux, ";" en Windows
    add_data_args = []
    for fname in data_files:
        src = os.path.join(project_dir, fname)
        add_data_args += ['--add-data', f"{src}{sep}."]

    # 3) Opciones de PyInstaller, incluyendo src/ en paths
    opts = [
        '--onefile',
        '--console',   # usa '--windowed' si prefieres GUI sin consola
    ]
    src_dir = os.path.join(project_dir, 'src')
    if os.path.isdir(src_dir):
        opts += ['--paths', src_dir]

    opts += add_data_args + [rel_entry]

    print("Ejecutando PyInstaller con:\n", " ".join(opts))
    PyInstaller.__main__.run(opts)

if __name__ == "__main__":
    main()
