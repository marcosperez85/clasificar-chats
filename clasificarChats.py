#!/usr/bin/env python
# coding: utf-8

# ### Import all needed packages
import boto3
import json
import logging
from pathlib import Path
from botocore.exceptions import ClientError
from jinja2 import Template

# Configurar logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Especifico mi sesión de para el usuario del IAM Identity Center (SSO)
session = boto3.Session(profile_name="AdministratorAccess-376129873205")

# Crear cliente de S3 en la región ingresada sino toma us-east-1 por default
s3_client = session.client('s3', region_name = "us-east-1")

# Creo un objeto s3 para para poder trabajar sobre el mismo. No era parte del tutorial pero lo agergué yo para algunas
# validaciones dentro de VS Code
recurso_s3 = session.resource('s3')

# Guardo en una variable el nombre del bucket
bucket_name = 'chats-limpios'

# Dado que el nombre del bucket está "hardcodeado" agrego un condicional en caso de que un día borre dicho bucket en AWS.

def buscarSiExisteBucket(bucket_name):
    # Obtener la lista de nombre de buckets
    # s3.buckets.all() devuelve un iterador con todos los objetos de tipo Bucket en la cuenta de AWS.
    # Luego se recorre cada objeto "bucket" en s3.buckets.all(), obteniendo su nombre con bucket.name
    # Esto es un "list comprehension" que es una forma abreviada de crear una lista 
    buckets = [bucket.name for bucket in recurso_s3.buckets.all()]
    
    # La instrucción anterior devuelve una lista de objetos, no strings. Además no se puede evaluar son strings,
    # sólo se puede evaluar con índices. Así que tengo que usar la sintaxis "elem in list" o "elem not in list"
    if bucket_name not in buckets:
        logging.info(f"\n\nEl bucket '{bucket_name}' no pudo encontrarse y va a ser creado en us-east-1")
        return crearBucket(bucket_name)

    else:
        logging.info(f"\n\nEl bucket '{bucket_name}' fue encontrado en us-east-1 y no hace falta crearlo")
        return True

def crearBucket(nombreDeBucket):
    #Crear bucket en region us-east-1
    s3_client.create_bucket(Bucket = nombreDeBucket)
    logging.info(f"\n\nEl bucket '{nombreDeBucket}' fue creado con éxito en la región us-east-1'")
    return True

# Llamo a la función de verificación de existencia del bucket
buscarSiExisteBucket(bucket_name)

# ===============================================
# Sección para subir archivos de texto

# Ruta a la carpeta que contiene los chats
carpeta = Path("/home/marcos/Downloads/Chats")

for archivo in carpeta.glob("*.txt"):
    buscarSiExisteObjeto(archivo, bucket_name)


# Recordar que un archivo dentro de un bucket recibe el nombre de "objeto". Para simplificar el código vamos a hacer
# que el nombre del objeto (último parámetro) sea el mismo que el nombre del archivo.

def buscarSiExisteObjeto(file_name, bucket_name):

    # Obtener el objeto Bucket de nuestro bucket específico.
    objetoBucket = recurso_s3.Bucket(bucket_name)

    # Crear una lista usando el list comprehension
    listaDeObjetos = [obj.key for obj in objetoBucket.objects.all()]    
    
    if file_name not in listaDeObjetos:
        return subirArchivo(file_name, bucket_name)
    else:
        logging.info("\nEl archivo ya existía en el bucket")
        return False
    

def subirArchivo(nombreDeArchivo, nombreDelBucket):
    try:
        s3_client.upload_file(nombreDeArchivo, nombreDelBucket, nombreDeArchivo)
        logging.info(f"\nEl archivo '{nombreDeArchivo} fue subido con éxito al bucket '{nombreDelBucket}")

    except ClientError as err:
        logging.info(f"\nNo se pudo subir el archivo debido al error:\n\n{err}")        
        return False
    return True


# ===============================================
# Sección para procesar el archivo de texto.

bedrock_runtime = session.client('bedrock-runtime', region_name='us-east-1')


# Abrir el archivo de texto local con la transcripción que se realizó antes
with open(f'{job_name}.txt', "r") as file:
    transcript = file.read()

# El instructor explica que en el módulo anterior (L1) habíamos usado un string para generar un prompt
# También es factible concatenación de strings y F-String para agregar variables.
# Sin embargo para un entorno de producción como es este caso donde tenemos una arquitectura Serverless, es más conveniente
# o más manejable, usar un template en un archivo separado. En este caso vamos a usar Jinja que es la librería de templates.
# Al usar un template en un archivo separado, se puede realizar un control de versiones y separar el código del template del
# código de la aplicación. Esto permite intercambiar prompts en vivo mientras la aplicación está en producción.

# En el tutorial original se usa una instrucción propia del notebook de Jupyter para crear un archivo con el prompt
# Sin embargo acá en Python no tenemos esa misma instrucción de IPython por lo que el TXT del prompt ya lo dejé localmente.
# y se llama "prompt_template.txt"

# Leemos el archivo de texto del prompt y lo guardamos en una variable.
with open('prompt_template.txt', "r") as file:
    template_string = file.read()

# Si miramos el prompt, sólo nos interesa completar un tag de XML llamado "data" el cual va a contener el "transcript"
# Luego a ese key de transcript le cargamos la variable "transcript" obtenida anteriormente al leer el prompt_template.txt
data = {
    'transcript' : transcript
}

# Llamamos al objeto Template que nos habíamos traido de la librería Jinja y le cargamos el contenido
# de la variable template_string. Para más comodidad ese objeto se lo asignamos a una variable llamada "template" también.
template = Template(template_string)

# Renderizamos todo y lo almacenamos en una variable llamada "prompt". 
# Todo esto es para no tener que crear un prompt manualmente donde le hagamos un copy/paste de la transcripción.
# Una vez más, se pudo haber hecho con concatenación de strings y con el uso de F-String pero de esta forma podemos
# editar el archivo de prompt en vivo y llevar un control de versiones.
prompt = template.render(data)

# Todo lo que sigue ahora es igual a lo que habíamos hecho en el módulo L1.
kwargs = {
    "modelId": "amazon.titan-text-lite-v1",
    "contentType": "application/json",
    "accept": "*/*",
    "body": json.dumps(
        {
            "inputText": prompt,
            "textGenerationConfig": {
                "maxTokenCount": 512,
                "temperature": 0,
                "topP": 0.9
            }
        }
    )
}

print("\nGenerando resumen...")

response = bedrock_runtime.invoke_model(**kwargs)
response_body = json.loads(response.get('body').read())
generation = response_body['results'][0]['outputText']
print(f"El resumen de la transcripción es:\n{generation}")
