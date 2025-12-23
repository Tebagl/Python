# Alarma Despertador con YouTube ⏰📺

Reloj digital con interfaz gráfica que permite programar una alarma. Cuando llega la hora establecida, el programa selecciona aleatoriamente un video de una lista y lo reproduce automáticamente.

## Características
* Interfaz gráfica moderna con `Tkinter` y `ttk`.
* Manejo de hilos (`threading`) para no congelar la interfaz durante la reproducción.
* Reproducción robusta usando `mpv` o `vlc`.
* Lectura de configuración desde archivo externo.

## Configuración
El programa requiere un archivo llamado `videos_youtube.txt` en la misma carpeta, que debe contener una lista de URLs válidas (una por línea).
