
# Lector de Noticias con Voz (News-to-Speech) 📰🗣️

Aplicación de escritorio que permite introducir la URL de una noticia, extraer su contenido textual y convertirlo en un archivo de audio MP3 para escucharlo.

## Tecnologías
* **Python 3**
* **Tkinter:** Para la interfaz gráfica.
* **Newspaper3k:** Para el scraping y parseo de artículos.
* **gTTS (Google Text-to-Speech):** Para la conversión de texto a voz.
* **NLTK:** Para el procesamiento de lenguaje natural.

## Instrucciones
1.  Ejecutar el script `noticia.py`.
2.  Pegar la URL de un artículo en el campo de texto.
3.  Pulsar **"Convertir a Voz"** y esperar el mensaje de éxito.
4.  Pulsar **"Reproducir Audio"**.

## 🚀 Habilidades Técnicas y Aprendizajes

Este proyecto demuestra competencias en las siguientes áreas:

* **🏗️ Arquitectura Modular (SOLID):**
    El código evita el "código espagueti" dividiendo la lógica en funciones especializadas (`extraer_noticia`, `generar_audio`), lo que demuestra capacidad para escribir software mantenible y escalable.

* **🧩 Integración de Sistemas:**
    Capacidad para leer documentación técnica y conectar distintas tecnologías: scraping web (`newspaper`), síntesis de voz (`gTTS`) y reproducción multimedia (`playsound`).

* **🛡️ Programación Defensiva:**
    El programa anticipa fallos (como una URL caída) y los gestiona mediante `try-except`, asegurando que la aplicación no se cierre inesperadamente y comunicando el error al usuario.

* **🤖 Introducción a NLP:**
    Uso de `NLTK` para el procesamiento inteligente del texto extraído, demostrando habilidades más allá del desarrollo web tradicional.
