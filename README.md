# Clasificación de chats

## Limpiar Chats
El script `limpiarChats` sirve para eliminar aquellos mensajes automáticos de whatsapp tales como `Esperando este mensaje`, `Multimendia Omitido` y `Se eliminó este mensaje` de forma de evitar texto innecesario para que lo procese el LLM.

## Clasificación de chats en preguntas y respuestas

El script `clasificarChats` es una herramienta que permite clasificar conversaciones de chat en grupos según la respuesta del asistente. La herramienta utiliza una expresión regular para detectar líneas válidas de conversación y luego analizar cada línea para determinar si es una pregunta o una respuesta.
Cada chat exportado en txt debe estar en una carpeta llamada `Chats_Limpios` y el script analiza una por una las conversaciónes. El resultado final se guarda en un archivo llamado `chats_clasificados` el cual contiene los campos

`Fecha de consulta`, `Resumen de la consulta`, `Fecha de respuesta`, `Resumen de la respuesta`

## Instalación
Para instalar el entorno virtual y las dependencias necesarias, sigue los siguientes pasos:

1. Instala la versión más reciente de Python en tu sistema operativo. Puedes descargarlo desde la página oficial de Python.
2. Una vez que hayas instalado Python, abre una terminal o consola de comandos y ejecuta el siguiente comando para crear un entorno virtual: `python -m venv clasificarChats`
3. Después de crear el entorno virtual, activa el mismo mediante el siguiente comando en la misma terminal o consola de comandos: `clasificarChats\Scripts\activate.bat` (si estás usando Windows) o `source clasificarChats/bin/activate` (si estás usando Linux o Mac).
4. Una vez que hayas activado el entorno virtual, instala las dependencias necesarias mediante el siguiente comando: `pip install -r requirements.txt`.

Con estas instrucciones puedes instalar el entorno virtual y las dependencias necesarias para ejecutar el script `clasificarChats`.