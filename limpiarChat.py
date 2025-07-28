import re
from pathlib import Path

# Ruta a la carpeta que contiene los chats
carpeta = Path("c:\Marcos\Chats")  # Podés cambiarla si querés

# Expresión regular para detectar líneas válidas de conversación
regex_mensaje = re.compile(r"^\d{1,2}/\d{1,2}/\d{2}, \d{2}:\d{2} - [^:]+: .+")

# Recorre todos los archivos .txt en la carpeta
for archivo in carpeta.glob("*.txt"):
    clean_lines = []
    with archivo.open(encoding="utf-8") as f:
        for linea in f:
            if (
                regex_mensaje.match(linea)
                and "esperando este mensaje" not in linea.lower()
                and "<multimedia omitido>" not in linea.lower()
                and "se eliminó este mensaje" not in linea.lower()
                and linea.strip() != ""
            ):
                clean_lines.append(linea.strip())

    # Crear nombre de archivo limpio
    archivo_salida = archivo.with_name(archivo.stem + "_limpio.txt")

    # Guardar resultado
    with archivo_salida.open("w", encoding="utf-8") as f:
        f.write("\n".join(clean_lines))

    print(f"✅ Archivo procesado: {archivo_salida.name}")
