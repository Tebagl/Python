# Alarma Despertador con YouTube ⏰📺

Reloj digital con interfaz gráfica que permite programar una alarma. Cuando llega la hora establecida, el programa selecciona aleatoriamente un video de una lista y lo reproduce automáticamente.

## Características
* Interfaz gráfica moderna con `Tkinter` y `ttk`.
* Manejo de hilos (`threading`) para no congelar la interfaz durante la reproducción.
* Reproducción robusta usando `mpv` o `vlc`.
* Lectura de configuración desde archivo externo.

## Configuración
El programa requiere un archivo llamado `videos_youtube.txt` en la misma carpeta, que debe contener una lista de URLs válidas (una por línea).

# Alarma Despertador con YouTube ⏰📺

Aplicación de escritorio que funciona como un reloj digital y permite programar una alarma. Cuando llega la hora establecida, el programa selecciona aleatoriamente un enlace de una lista personalizada y reproduce el video automáticamente.

## Tecnologías
* **Python 3**
* **Tkinter / ttk:** Para la construcción de la interfaz gráfica y selectores de tiempo.
* **Threading:** Para la ejecución de tareas en segundo plano sin congelar la interfaz.
* **Subprocess:** Para la gestión de procesos del sistema y ejecución del reproductor.
* **MPV Player:** Motor externo utilizado para la reproducción robusta de streaming.

## Instrucciones
1.  Asegurarse de tener el archivo `videos_youtube.txt` en la misma carpeta con una lista de URLs válidas.
2.  Tener instalado `mpv` en el sistema (o configurar la ruta en el script).
3.  Ejecutar el script `alarma_8.py`.
4.  Seleccionar la hora, minutos y segundos deseados.
5.  Dejar la aplicación abierta; el video se lanzará automáticamente a la hora programada.

## 🚀 Habilidades Técnicas y Aprendizajes
Este proyecto demuestra competencias en las siguientes áreas:

* **🧵 Manejo de Concurrencia (Threading):**
    Implementación del módulo `threading` para separar la lógica de reproducción de video del bucle principal de la interfaz gráfica (GUI). Esto evita que la aplicación se "congele" mientras carga el video, asegurando una experiencia de usuario fluida.

* **⚙️ Interacción con el Sistema Operativo:**
    Uso de `subprocess` para invocar ejecutables externos (`mpv`) desde Python. Esto demuestra la capacidad de integrar scripts de Python con herramientas del sistema y manejar flujos de entrada/salida estándar (`stdout`/`stderr`).

* **📂 Gestión de Configuración Externa:**
    El programa no tiene los datos "hardcodeados", sino que lee la configuración desde un archivo externo (`videos_youtube.txt`). Esto es una buena práctica que separa el código de los datos, facilitando la actualización de la lista de reproducción sin tocar el código fuente.

* **🛡️ Robustez y Manejo de Recursos:**
    Incluye una función de "Cerrar Aplicación" que se encarga de terminar limpiamente los procesos hijos (`terminate/kill`) antes de destruir la ventana, evitando fugas de memoria o procesos "zombie" en el sistema.
