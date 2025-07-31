#!/usr/bin/env python
# coding: utf-8

# ### Import all needed packages
import boto3
import json
import os
import glob
from pathlib import Path
import logging
from pathlib import Path
from jinja2 import Template
from botocore.config import Config

# Imported os and glob modules, which are needed for working with file paths and pattern matching.
# Used the os.path.join() function to construct the path correctly, regardless of the operating system.
# This is a good practice when working with file paths in Python.

# Ruta a la carpeta que contiene los chats
carpeta = Path("c:\\Marcos\\Chats_Limpios")

# Configurar logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Especifico mi sesión de para el usuario del IAM Identity Center (SSO)
session = boto3.Session(profile_name="AdministratorAccess-376129873205")

# ===============================================
# Sección para procesar el archivo de texto.
config = Config(read_timeout=120, connect_timeout=30)
bedrock_runtime = session.client('bedrock-runtime', region_name='us-east-1', config=config)

# Creo un archivo vacío antes del loop
Path("chats_clasificados.txt").write_text("", encoding="utf-8")

# Crear nombre de archivo limpio (por fuera del loop que viene luego)
with open("chats_clasificados.txt", "w", encoding="utf-8") as f:

    # Recorre todos los archivos .txt en la carpeta
    for archivo in glob.glob(os.path.join(carpeta, "*.txt")):
        with open(archivo, "r", encoding="utf-8") as file:
            conversacion = file.read()

            # En este caso donde tenemos una arquitectura Serverless vamos a tener un template de Jinja.
            # Al usar un template en un archivo separado (prompt_template.txt), se puede realizar un control de versiones y
            # separar el código del template del código de la aplicación.
            # Esto permite intercambiar prompts en vivo mientras la aplicación está en producción.

            # Leemos el archivo de texto del prompt y lo guardamos en una variable.
            with open('prompt_template.txt', "r", encoding="utf-8") as file:
                template_string = file.read()

            # Llamamos al objeto Template que nos habíamos traido de la librería Jinja y le cargamos el contenido
            # de la variable template_string. Para más comodidad ese objeto se lo asignamos a una variable llamada "template" también.
            template = Template(template_string)

            # Renderizamos todo y lo almacenamos en una variable llamada "prompt". 
            # Todo esto es para no tener que crear un prompt manualmente donde le hagamos un copy/paste de la transcripción.
            prompt = template.render({'conversacion': conversacion})

            # Declaro todos los argumentos que le pasamos a Bedrock más adelante.
            kwargs = {
                "modelId": "cohere.command-r-plus-v1:0",
                "contentType": "application/json",
                "accept": "*/*",
                "body": json.dumps(
                    {
                        "message": prompt,
                        "max_tokens": 16000,
                        "temperature": 0
                    }
                )
            }

            response = bedrock_runtime.invoke_model(**kwargs)
            response_body = json.loads(response.get('body').read())
            generation = response_body.get("text", "")
            print(f"\nClasificación para el archivo: {archivo}:\n{generation}")
            
            with open("chats_clasificados.txt", "a", encoding="utf-8") as f:
                f.write(f"\n--- Clasificación del archivo: {archivo} ---\n")
                f.write(generation + "\n")
