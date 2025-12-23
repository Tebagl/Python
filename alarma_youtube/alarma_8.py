import tkinter as tk
from tkinter import ttk, messagebox
from time import strftime
import random
import threading
import subprocess 
import os 
import time

# --- I. Funciones y Variables Globales de Lectura (Constantes) ---

def cargar_videos():
    """Carga las URLs de YouTube desde el archivo 'videos_youtube.txt'."""
    try:
        with open("videos_youtube.txt", 'r') as archivo_objeto:
            return [linea.strip() for linea in archivo_objeto if linea.strip()]
    except FileNotFoundError:
        messagebox.showerror("Error", "Archivo 'videos_youtube.txt' no encontrado.")
        return []

# Constantes del programa, accesibles por la clase
horas = list(range(24))
minutos = list(range(60))
segundos = list(range(60))
videos = cargar_videos()


# ----------------------------------------------------------------------
# II. CLASE PRINCIPAL: AlarmaApp 
# ----------------------------------------------------------------------

class AlarmaApp:
    # --- Constantes de Clase ---
    
    CMD_PYTHON = "python3" 
    CMD_MPV = "mpv" 
    
    def __init__(self, master):
        self.master = master
        master.title("Alarma YouTube: Final Depurado")
        master.geometry("400x300")
        master.config(bg="black")
        
        # Atributos de Instancia
        self.proceso_mpv = None 
        self.alarma_disparada = False 
        
        self.crear_widgets()
        self.obtener_hora() 

    # --- Creación de la Interfaz (GUI) ---
    
    def crear_widgets(self):
        # Etiqueta hora real
        self.hora_real_label = tk.Label(self.master, bg="Black", fg="White", font=("Arial", 20))
        self.hora_real_label.grid(row=0, column=1, pady=10)

        # Etiquetas Hora, Minutos, Segundos
        tk.Label(self.master, text="Hora", bg="Black", fg="White", font=("Arial", 10)).grid(row=1, column=0, padx=10, pady=2)
        tk.Label(self.master, text="Minutos", bg="Black", fg="White", font=("Arial", 10)).grid(row=1, column=1, padx=10, pady=2)
        tk.Label(self.master, text="Segundos", bg="Black", fg="White", font=("Arial", 10)).grid(row=1, column=2, padx=10, pady=2)

        # Comboboxes
        self.horas_combobox = ttk.Combobox(self.master, values=horas, width=10, justify="center")
        self.horas_combobox.grid(row=2, column=0, padx=10, pady=(2, 10))
        self.horas_combobox.current(0)

        self.minutos_combobox = ttk.Combobox(self.master, values=minutos, width=10)
        self.minutos_combobox.grid(row=2, column=1, padx=10, pady=(2, 10))
        self.minutos_combobox.current(0)

        self.segundos_combobox = ttk.Combobox(self.master, values=segundos, width=10)
        self.segundos_combobox.grid(row=2, column=2, padx=10, pady=(2, 10))
        self.segundos_combobox.current(0)

        # Visualizar la hora de la alarma
        tk.Label(self.master, text="ALARMA", font=("Arial", 12), bg="black", fg="Yellow").grid(row=3, column=1, padx=2, pady=1)
        self.hora_alarma = tk.Label(self.master, text="00:00:00", font=("Arial", 20), bg="black", fg="Yellow")
        self.hora_alarma.grid(row=4, column=1, padx=2, pady=1)
        self.actualizar_alarma_display()

        # >>> CAMBIO AQUÍ: Botón de Cerrar Aplicación <<<
        boton_cerrar = tk.Button(self.master, text="Cerrar Aplicación", 
                                command=self.cerrar_aplicacion, 
                                width=20, bg="#DC143C", fg="white")
        boton_cerrar.grid(row=5, column=1, pady=10)
        # >>> FIN DEL CAMBIO <<<


        # Eventos para actualizar la visualización de la alarma
        self.horas_combobox.bind("<<ComboboxSelected>>", self.actualizar_alarma_display)
        self.minutos_combobox.bind("<<ComboboxSelected>>", self.actualizar_alarma_display)
        self.segundos_combobox.bind("<<ComboboxSelected>>", self.actualizar_alarma_display)
        
    def actualizar_alarma_display(self, event=None):
        """Actualiza la etiqueta de la hora de la alarma."""
        try:
            h = int(self.horas_combobox.get())
            m = int(self.minutos_combobox.get())
            s = int(self.segundos_combobox.get())
            self.hora_alarma.config(text=f"{h:02d}:{m:02d}:{s:02d}")
        except ValueError:
            self.hora_alarma.config(text="XX:XX:XX")

    # --- Nuevo Método de Control ---
    def cerrar_aplicacion(self):
        """Intenta detener la reproducción y luego cierra la GUI."""
        if self.proceso_mpv and self.proceso_mpv.poll() is None:
            self.proceso_mpv.terminate() 
            try:
                self.proceso_mpv.wait(timeout=2)
            except subprocess.TimeoutExpired:
                self.proceso_mpv.kill()
        
        # Destruye la ventana principal
        self.master.destroy()

    # --- Lógica de la Reproducción (Se mantiene la lógica robusta) ---

    def activar_alarma_thread(self):
        """Reproduce un video de YouTube con MPV de forma robusta."""
        self.alarma_disparada = True 
        
        try:
            if not videos:
                messagebox.showerror("Error", "No hay URLs válidas cargadas.")
                return

            video_aleatorio = random.choice(videos)
            
            # Reproducción con MPV y ytdl:// (método robusto)
            mpv_cmd = [
                self.CMD_MPV, 
                f"ytdl://{video_aleatorio}",  
                "--no-terminal", 
                "--force-media-title=Alarma Activa"
            ] 
            
            self.proceso_mpv = subprocess.Popen(mpv_cmd, 
                                                stdout=subprocess.DEVNULL, 
                                                stderr=subprocess.DEVNULL) 
            
            # El hilo espera aquí hasta que el video termine o sea detenido
            self.proceso_mpv.wait() 
            
        except FileNotFoundError as e:
             messagebox.showerror("Error de Ejecutable", f"No se encontró el ejecutable: {e.filename}. Asegúrese de que MPV esté instalado y en el PATH.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado al reproducir: {e}")
            
        finally:
            self.alarma_disparada = False
            self.proceso_mpv = None

    # --- Lógica del Reloj Principal ---
    
    def obtener_hora(self):
        """Actualiza el reloj cada segundo y compara la hora actual con la alarma."""
        horas_real = strftime("%H")
        minutos_real = strftime("%M")
        segundos_real = strftime("%S")
        self.hora_real_label.config(text=f"{horas_real}:{minutos_real}:{segundos_real}")

        # Obtener valores de la alarma
        try:
            horas_alarma = f"{int(self.horas_combobox.get()):02d}"
            minutos_alarma = f"{int(self.minutos_combobox.get()):02d}"
            segundos_alarma = f"{int(self.segundos_combobox.get()):02d}"
        except ValueError:
            horas_alarma, minutos_alarma, segundos_alarma = "XX", "XX", "XX"
        
        # Comparar la hora con la alarma
        if (horas_real == horas_alarma) and \
           (minutos_real == minutos_alarma) and \
           (segundos_real == segundos_alarma) and \
           (not self.alarma_disparada):
            
            hilo_alarma = threading.Thread(target=self.activar_alarma_thread, daemon=True)
            hilo_alarma.start()

        # Actualizar hora real cada 1000ms (1 segundo)
        self.master.after(1000, self.obtener_hora)


# ----------------------------------------------------------------------
# III. EJECUCIÓN DEL PROGRAMA
# ----------------------------------------------------------------------

if __name__ == "__main__":
    root = tk.Tk()
    app = AlarmaApp(root)
    root.mainloop()