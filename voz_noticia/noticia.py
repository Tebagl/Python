'''

Autor: Teba García Lozano
Fecha: 18-07-2025
Proyecto: Lector de Noticias con Voz (News-to-Speech Converter)
Objetivo: Introducir una URL de una noticia de internet y pasarla a voz.
Tecnologías: Python 3, tkinter, newspaper3k, gTTS, playsound, nltk.
'''

import tkinter as tk
from tkinter import messagebox
from newspaper import Article,Config
from gtts import gTTS
# from playsound import playsound COMENTA ESTA LÍNEA
import subprocess                
import sys                         
import os
import nltk

# 1. Configuración inicial
# Descarga el modelo necesario para la tokenización del texto
try:
    nltk.download("punkt", quiet=True)
    nltk.download("punkt_tab")
except Exception as e:
    print(f"Error al descargar NLTK punkt: {e}")

# 2. Funciones Core (Modularidad y Responsabilidad Única)

def extraer_noticia(url):
    """Descarga la noticia disfrazándose de navegador real para evitar el Error 403."""
    
    # 1. Preparamos el "disfraz" (User-Agent)
    config = Config()
    # Este string tan largo le dice a la web que somos un PC normal usando Chrome
    config.browser_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    config.request_timeout = 10 

    # 2. Creamos el artículo PASÁNDOLE LA CONFIGURACIÓN (Importante)
    articulo = Article(url, language='es', config=config)
    
    # 3. Descargamos y procesamos
    articulo.download()
    articulo.parse()
    
    return articulo

def generar_audio(texto, nombre_archivo="noticia.mp3"):
    """Guarda el audio en la MISMA carpeta que el script (Ruta Absoluta)."""
    carpeta_script = os.path.dirname(os.path.abspath(__file__))
    ruta_completa = os.path.join(carpeta_script, nombre_archivo)
    
    voz = gTTS(text=texto, lang="es")
    voz.save(ruta_completa)
    return ruta_completa


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

def reproducir_audio(nombre_archivo):
    """Busca y reproduce el audio desde la MISMA carpeta que el script."""
    
    # 1. Calculamos la ruta exacta otra vez (igual que al guardar)
    carpeta_script = os.path.dirname(os.path.abspath(__file__))
    ruta_completa = os.path.join(carpeta_script, nombre_archivo)
    
    try:
        if sys.platform == "linux":
            subprocess.call(["xdg-open", ruta_completa]) # <--- Ahora usamos la ruta completa
        elif sys.platform == "darwin":
            subprocess.call(["open", ruta_completa])
        else:
            os.startfile(ruta_completa)
            
    except FileNotFoundError:
        messagebox.showerror("Error", f"No se encuentra el archivo en:\n{ruta_completa}")
    except Exception as e:
        messagebox.showerror("Error", f"Error al reproducir: {e}")


# 3. Interfaz Gráfica (tkinter)

ventana = tk.Tk()
ventana.title("Lector de Noticias con Voz")
ventana.geometry("550x300")
ventana.resizable(False, False)

# Widgets
label_titulo = tk.Label(ventana, text="Convertir Noticia a Audio", font=("Helvetica", 18, "bold"))
label_titulo.pack(pady=20)

entrada_url = tk.Entry(ventana, width=50, fg="grey") # Texto gris para que parezca placeholder
entrada_url.pack(pady=5)
entrada_url.insert(0, "Introduce una URL aquí...")

# --- BORRADO AUTOMÁTICO ---
def on_entry_click(event):
    """Borra el texto de ejemplo cuando el usuario hace clic."""
    if entrada_url.get() == "Introduce una URL aquí...":
        entrada_url.delete(0, "end") # Borra todo
        entrada_url.insert(0, "")    # Lo deja vacío
        entrada_url.config(fg="black") # Cambia el color del texto a negro normal

def on_focus_out(event):
    """Vuelve a poner el texto si el usuario no escribió nada."""
    if entrada_url.get() == "":
        entrada_url.insert(0, "Introduce una URL aquí...")
        entrada_url.config(fg="grey")

# Vinculamos los eventos (clic dentro y clic fuera)
entrada_url.bind('<FocusIn>', on_entry_click)
entrada_url.bind('<FocusOut>', on_focus_out)
# -----------------------------------------------

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
