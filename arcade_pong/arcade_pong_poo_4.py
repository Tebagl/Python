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
# Nota: La librería playsound a veces es difícil de configurar o puede fallar. 
# Si el archivo "pong.mp3" no está en la misma carpeta, fallará.
from playsound import playsound 

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
        # Limites definidos en JuegoPong.bucle_juego
        self.LIMITE_Y = 240 

    def mover_arriba(self):
        # NOTA: Límite superior corregido a 250 para mejor manejo
        if self.ycor() < 250:
            self.sety(self.ycor() + 20)

    def mover_abajo(self):
        # NOTA: Límite inferior corregido a -240 para mejor manejo
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
        # Límite superior/inferior para el rebote en el bucle principal
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
        self.goto(0, 260) # Posición ajustada a la parte superior (260)

    def actualizar(self, puntos_izq, puntos_drch):
        """Dibuja el marcador."""
        self.clear()
        self.write(f"{puntos_izq}      {puntos_drch}", align="center", font=("Fixedsys", 36, "bold")) # Tamaño de fuente ajustado


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
        self.ventana.tracer(0) # Desactiva el auto-refresco para control manual

        # Estado del juego
        self.puntos_izq = 0 
        self.puntos_drch = 0 
        self.juego_activo = False
        self.VELOCIDAD_JUEGO = 20 # Milisegundos para el refresco (50 FPS)

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
        # FUNCIÓN EXTERNA: self.ventana.mainloop() (turtle.Screen)
        self.ventana.mainloop()

    def configurar_controles(self):
        """Asigna las funciones de movimiento y inicio a las teclas."""
        # FUNCIÓN EXTERNA: self.ventana.listen() (turtle.Screen)
        self.ventana.listen()
        # FUNCIÓN EXTERNA: self.ventana.onkeypress() (turtle.Screen)
        self.ventana.onkeypress(self.pala_izq.mover_arriba, "w")
        self.ventana.onkeypress(self.pala_izq.mover_abajo, "s")
        self.ventana.onkeypress(self.pala_drch.mover_arriba, "Up")
        self.ventana.onkeypress(self.pala_drch.mover_abajo, "Down")
        self.ventana.onkeypress(self.iniciar_juego, "Return")
        
    def actualizar_marcador(self):
        """Llama al método actualizar del objeto Marcador."""
        self.marcador.actualizar(self.puntos_izq, self.puntos_drch)
        
    # --- Gestión de Sonido (Encapsulado) ---
    def reproducir_sonido(self):
        """Ejecuta el sonido de rebote en un hilo secundario."""
        # FUNCIÓN EXTERNA: threading.Thread() y .start() (threading)
        # Usa lambda para llamar a playsound sin bloquear el bucle principal.
        threading.Thread(target=lambda: playsound("pong.mp3", block=False), daemon=True).start()
        
    # --- Lógica de Juego ---
    
    def iniciar_juego(self):
        """Activa el bucle de juego y oculta el mensaje de inicio."""
        self.juego_activo = True
        self.mensaje.ocultar()

    def reiniciar(self):
        """Reinicia la posición de la pelota, palas y el estado del juego."""
        self.juego_activo = False
        self.pelota.goto(0, 0)
        self.pelota.dx *= -1 # Cambia la dirección al reiniciar para alternar el saque
        self.pala_izq.goto(-350, 0)
        self.pala_drch.goto(350, 0)
        self.mensaje.mostrar("PRESS ENTER TO START")
        
    def bucle_juego(self):
        """Bucle principal recursivo del juego."""
        if self.juego_activo:
            self.pelota.mover()

            # 1. Rebote Superior e Inferior
            if abs(self.pelota.ycor()) > self.pelota.LIMITE_Y:
                self.pelota.dy *= -1
                self.reproducir_sonido()

            # 2. Punto (Fuera del límite X)
            if abs(self.pelota.xcor()) > 390:
                if self.pelota.xcor() > 0:
                    self.puntos_izq += 1
                else:
                    self.puntos_drch += 1
                
                self.actualizar_marcador()
                self.reiniciar()
                
            # 3. Rebote con Palas (Colisiones)
            
            # Rebote con pala_drch
            if (340 < self.pelota.xcor() < 350 and 
                self.pala_drch.ycor() - 50 < self.pelota.ycor() < self.pala_drch.ycor() + 50):
                self.pelota.setx(340)
                self.pelota.dx *= -1
                self.reproducir_sonido()

            # Rebote con pala_izq
            if (-350 < self.pelota.xcor() < -340 and 
                self.pala_izq.ycor() - 50 < self.pelota.ycor() < self.pala_izq.ycor() + 50):
                self.pelota.setx(-340)
                self.pelota.dx *= -1
                self.reproducir_sonido()

        # FUNCIÓN EXTERNA: self.ventana.update() (turtle.Screen)
        self.ventana.update()
        
        # FUNCIÓN EXTERNA: self.ventana.ontimer() (turtle.Screen)
        # Llama a bucle_juego después de self.VELOCIDAD_JUEGO milisegundos (Recursión del juego)
        self.ventana.ontimer(self.bucle_juego, self.VELOCIDAD_JUEGO)


# --- III. EJECUCIÓN ---

if __name__ == "__main__":
    juego = JuegoPong()