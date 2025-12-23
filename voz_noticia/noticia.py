'''

Autor: Teba García Lozano
Fecha: 18-07-2025
Proyecto: Lector de Noticias con Voz (News-to-Speech Converter)
Objetivo: Introducir una URL de una noticia de internet y pasarla a voz.
Tecnologías: Python 3, tkinter, newspaper3k, gTTS, playsound, nltk.
'''

import tkinter as tk
from tkinter import messagebox
from newspaper import Article
from gtts import gTTS
from playsound import playsound
import nltk

# 1. Configuración inicial
# Descarga el modelo necesario para la tokenización del texto
try:
    nltk.download("punkt", quiet=True)
except Exception as e:
    print(f"Error al descargar NLTK punkt: {e}")

# 2. Funciones Core (Modularidad y Responsabilidad Única)

def extraer_noticia(url):
    """Descarga, analiza y devuelve el objeto Article de newspaper."""
    articulo = Article(url, lang="es")
    articulo.download()
    articulo.parse()
    return articulo


def generar_audio(texto, archivo_salida="noticia.mp3"):
    """Convierte el texto en audio (MP3) usando gTTS y lo guarda localmente."""
    voz = gTTS(text=texto, lang="es")
    voz.save(archivo_salida)
    return archivo_salida


def convertir_a_voz():
    """Función principal que gestiona el flujo de trabajo."""
    url = entrada_url.get()
    if not url:
        messagebox.showwarning("Atención", "Introduce una URL.")
        return
    
    label_estado.config(text="Procesando...", fg="blue")
    
    try:
        # Extraer texto de la URL
        articulo = extraer_noticia(url)
        # Combinar título y texto para una mejor lectura
        texto = articulo.title + ". " + articulo.text
        
        # Generar archivo de audio
        audio = generar_audio(texto)
        
        messagebox.showinfo("Éxito", f"Audio guardado como {audio}")
        label_estado.config(text="Conversión completada", fg="green")
        
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un problema: {type(e).__name__} - {e}")
        label_estado.config(text="Error al convertir", fg="red")


def reproducir_audio(audio):
    """Reproduce el archivo de audio guardado."""
    try:
        playsound(audio)
    except FileNotFoundError:
        messagebox.showerror("Error", "El archivo noticia.mp3 no se ha encontrado. ¿Ha convertido la URL?")
    except Exception as e:
        messagebox.showerror("Error", f"No se ha podido reproducir el audio: {e}")

        
# 3. Interfaz Gráfica (tkinter)

ventana = tk.Tk()
ventana.title("Lector de Noticias con Voz")
ventana.geometry("550x300")
ventana.resizable(False, False) # Mejor práctica para GUIs sencillas

# Widgets
label_titulo = tk.Label(ventana, text="Convertir Noticia a Audio", font=("Helvetica", 18, "bold"))
label_titulo.pack(pady=20)

entrada_url = tk.Entry(ventana, width=50)
entrada_url.pack(pady=5)
entrada_url.insert(0, "Introduce una URL aquí...") # Placeholder para UX

# Botones
boton_convertir = tk.Button(ventana, text="1. Convertir a Voz", command=convertir_a_voz, width=25, height=2, bg="#4CAF50", fg="white")
boton_convertir.pack(pady=10)

boton_reproducir = tk.Button(ventana, text="2. Reproducir Audio", command=lambda: \
                             reproducir_audio("noticia.mp3"), width=25, height=2, bg="#2196F3", fg="white")
boton_reproducir.pack(pady=5)

# Etiqueta de estado
label_estado = tk.Label(ventana, text="Esperando URL...", fg="gray")
label_estado.pack(pady=10)

ventana.mainloop()