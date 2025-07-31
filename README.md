# Clasificación de chats

## Limpiar Chats
El script `limpiarChats` sirve para eliminar aquellos mensajes automáticos de whatsapp tales como `Esperando este mensaje`, `Multimendia Omitido` y `Se eliminó este mensaje` de forma de evitar texto innecesario para que lo procese el LLM.

## Clasificación de chats en preguntas y respuestas

El script `clasificarChats` es una herramienta que permite clasificar conversaciones de chat en grupos de preguntas de clientes y respuestas del soporte técnico. La herramienta utiliza RegEx para detectar líneas válidas de conversación y luego analizar cada línea para determinar si es una pregunta o una respuesta.
Cada chat exportado en txt debe estar en una carpeta llamada `Chats_Limpios` y el script analiza una por una las conversaciónes. El resultado final se guarda en un archivo llamado `chats_clasificados` el cual contiene los campos

`Fecha de consulta`, `Resumen de la consulta`, `Fecha de respuesta`, `Resumen de la respuesta`

## Instalación
Para instalar el entorno virtual y las dependencias necesarias, siga los siguientes pasos:

1. Instala la versión más reciente de Python en tu sistema operativo. Puedes descargarlo desde la página oficial de Python.
2. Una vez que hayas instalado Python, abre una terminal o consola de comandos y ejecuta el siguiente comando para crear un entorno virtual: `python -m venv clasificarChats`
3. Después de crear el entorno virtual, activa el mismo mediante el siguiente comando en la misma terminal o consola de comandos: `clasificarChats\Scripts\activate.bat` (si estás usando Windows) o `source clasificarChats/bin/activate` (si estás usando Linux o Mac).
4. Una vez que hayas activado el entorno virtual, instala las dependencias necesarias mediante el siguiente comando: `pip install -r requirements.txt`.

## Autenticación (sólo para la versión con AWS)
Antes de poder usar el script, es necesario iniciar sesión en el AWS CLI con un usuario IAM SSO. Para eso hacen falta los siguientes pasos:
1. Ejecutar el comando `aws configure sso`
2. Completar los campos de nombre de sesión y dejar los demás campos con valores por default.
3. Es importante usar un usuario con permisos para ejecutar Bedrock en la región us-east-1.

Con estas instrucciones puedes instalar el entorno virtual y las dependencias necesarias para ejecutar el script `clasificarChats`.