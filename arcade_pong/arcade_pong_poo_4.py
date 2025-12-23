'''
Código Python Corregido y Optimizado:
He movido la función reproducir_sonido y las variables de puntuación dentro 
de la clase JuegoPong para encapsular la funcionalidad del juego,
lo cual es fundamental en la POO.
'''

"""
programar el juego de arcade Pong con POO
autor: Teba García Lozano
fecha: 15-07-2025
"""

# standar modules
import turtle
import threading
import time
import os           # <--- NUEVO: Para encontrar la ruta del archivo
import sys          # <--- NUEVO: Para detectar el sistema operativo
import subprocess   # <--- NUEVO: Para reproducir audio sin playsound

# --- I. CLASES DE OBJETOS DEL JUEGO ---

class Pala(turtle.Turtle):
    """Representa una de las dos palas del juego."""
    def __init__(self, x):
        super().__init__()
        self.speed(0)
        self.shape("square")
        self.color("white")
        self.shapesize(stretch_wid=5, stretch_len=1)
        self.penup()
        self.goto(x, 0)
        self.LIMITE_Y = 240 

    def mover_arriba(self):
        if self.ycor() < 250:
            self.sety(self.ycor() + 20)

    def mover_abajo(self):
        if self.ycor() > -240:
            self.sety(self.ycor() - 20)


class Pelota(turtle.Turtle):
    """Representa la pelota que se mueve y rebota."""
    def __init__(self):
        super().__init__()
        self.speed(0)
        self.shape("circle")
        self.color("white")
        self.penup()
        self.goto(0, 0)
        self.dx = 4
        self.dy = 4
        self.LIMITE_Y = 290 

    def mover(self):
        """Actualiza la posición de la pelota en cada frame."""
        self.setx(self.xcor() + self.dx)
        self.sety(self.ycor() + self.dy)


class Marcador(turtle.Turtle):
    """Gestiona y muestra las puntuaciones."""
    def __init__(self):
        super().__init__()
        self.speed(0)
        self.color("white")
        self.penup()
        self.hideturtle()
        self.goto(0, 260) 

    def actualizar(self, puntos_izq, puntos_drch):
        """Dibuja el marcador."""
        self.clear()
        self.write(f"{puntos_izq}      {puntos_drch}", align="center", font=("Fixedsys", 36, "bold"))


class Mensaje(turtle.Turtle):
    """Muestra mensajes de inicio y final de juego."""
    def __init__(self):
        super().__init__()
        self.speed(0)
        self.color("white")
        self.penup()
        self.hideturtle()
        self.goto(0, 100)

    def mostrar(self, texto):
        self.clear()
        self.write(texto, align="center", font=("Fixedsys", 24, "bold"))

    def ocultar(self):
        self.clear()


# --- II. CLASE PRINCIPAL DEL JUEGO ---

class JuegoPong:
    """Clase principal que contiene la lógica, estado y bucle del juego."""
    def __init__(self):
        # Inicialización de la ventana
        self.ventana = turtle.Screen()
        self.ventana.title("---PONG---ARCADE---")
        self.ventana.bgcolor("black")
        self.ventana.setup(width=800, height=600)
        self.ventana.tracer(0) 

        # Estado del juego
        self.puntos_izq = 0 
        self.puntos_drch = 0 
        self.juego_activo = False
        self.VELOCIDAD_JUEGO = 20 

        # Creación de objetos
        self.pala_izq = Pala(-350)
        self.pala_drch = Pala(350)
        self.pelota = Pelota()
        self.marcador = Marcador() 
        self.mensaje = Mensaje() 
        
        # Inicialización de la GUI
        self.actualizar_marcador()
        self.mensaje.mostrar("PRESS ENTER TO START")

        # Configuración de controles
        self.configurar_controles()

        # Iniciar el bucle de juego recursivo
        self.bucle_juego()
        self.ventana.mainloop()

    def configurar_controles(self):
        self.ventana.listen()
        self.ventana.onkeypress(self.pala_izq.mover_arriba, "w")
        self.ventana.onkeypress(self.pala_izq.mover_abajo, "s")
        self.ventana.onkeypress(self.pala_drch.mover_arriba, "Up")
        self.ventana.onkeypress(self.pala_drch.mover_abajo, "Down")
        self.ventana.onkeypress(self.iniciar_juego, "Return")
        
    def actualizar_marcador(self):
        self.marcador.actualizar(self.puntos_izq, self.puntos_drch)
        
    # --- Gestión de Sonido (UNIVERSAL: WINDOWS / MAC / LINUX) ---
    def reproducir_sonido(self):
        """Reproduce sonido compatible con cualquier S.O. sin librerías externas."""
        
        # 1. Calcular ruta absoluta (blindado contra errores de carpeta)
        carpeta_script = os.path.dirname(os.path.abspath(__file__))
        ruta_audio = os.path.join(carpeta_script, "pong.mp3")
        
        def _play():
            try:
                # --- CASO LINUX ---
                if sys.platform == "linux":
                    # Intentamos mpv (que ya tienes) silenciando la salida
                    subprocess.run(["mpv", "--no-terminal", "--volume=80", ruta_audio], 
                                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

                # --- CASO MAC (Darwin) ---
                elif sys.platform == "darwin":
                    # afplay es el reproductor nativo de terminal en macOS
                    subprocess.run(["afplay", ruta_audio], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

                # --- CASO WINDOWS ---
                elif sys.platform == "win32":
                    # En Windows, usar subprocess es lento. Usamos ctypes para acceder 
                    # al sistema multimedia (winmm) directamente. Es nativo y rápido.
                    import ctypes
                    # Comando MCI para reproducir MP3
                    mci = ctypes.windll.winmm.mciSendStringW
                    alias = "pong_sound"
                    # Abrir, reproducir y cerrar (Comandos de texto MCI)
                    mci(f'open "{ruta_audio}" type mpegvideo alias {alias}', None, 0, None)
                    mci(f'play {alias} wait', None, 0, None)
                    mci(f'close {alias}', None, 0, None)

            except Exception as e:
                # Si falla el audio, el juego no se rompe, solo imprime el error
                print(f"Error de audio ({sys.platform}): {e}")

        # 2. Ejecutar en hilo secundario para no congelar el juego (Daemon)
        threading.Thread(target=_play, daemon=True).start()
        
    # --- Lógica de Juego ---
    
    def iniciar_juego(self):
        self.juego_activo = True
        self.mensaje.ocultar()

    def reiniciar(self):
        self.juego_activo = False
        self.pelota.goto(0, 0)
        self.pelota.dx *= -1 
        self.pala_izq.goto(-350, 0)
        self.pala_drch.goto(350, 0)
        self.mensaje.mostrar("PRESS ENTER TO START")
        
    def bucle_juego(self):
        if self.juego_activo:
            self.pelota.mover()

            # 1. Rebote Superior e Inferior
            if abs(self.pelota.ycor()) > self.pelota.LIMITE_Y:
                self.pelota.dy *= -1
                self.reproducir_sonido()

            # 2. Punto
            if abs(self.pelota.xcor()) > 390:
                if self.pelota.xcor() > 0:
                    self.puntos_izq += 1
                else:
                    self.puntos_drch += 1
                
                self.actualizar_marcador()
                self.reiniciar()
                
            # 3. Rebote con Palas
            if (340 < self.pelota.xcor() < 350 and 
                self.pala_drch.ycor() - 50 < self.pelota.ycor() < self.pala_drch.ycor() + 50):
                self.pelota.setx(340)
                self.pelota.dx *= -1
                self.reproducir_sonido()

            if (-350 < self.pelota.xcor() < -340 and 
                self.pala_izq.ycor() - 50 < self.pelota.ycor() < self.pala_izq.ycor() + 50):
                self.pelota.setx(-340)
                self.pelota.dx *= -1
                self.reproducir_sonido()

        self.ventana.update()
        self.ventana.ontimer(self.bucle_juego, self.VELOCIDAD_JUEGO)


# --- III. EJECUCIÓN ---

if __name__ == "__main__":
    juego = JuegoPong()