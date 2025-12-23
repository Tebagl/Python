# 🏓 Arcade Pong: POO Edition

Recreación moderna del clásico videojuego de Arcade. Este proyecto no es solo un juego funcional, sino un ejercicio de refactorización de código: se ha pasado de una programación lineal a una arquitectura basada en **Programación Orientada a Objetos (POO)** para mejorar la escalabilidad, legibilidad y el mantenimiento del software.


## 🛠️ Tecnologías Utilizadas
* **Python 3:** Lenguaje base.
* **Turtle Graphics:** Motor gráfico para el renderizado vectorial.
* **Threading:** Gestión de procesos ligeros para audio asíncrono.
* **Playsound:** Reproducción de efectos de sonido.

## 📋 Características
* **Modo 2 Jugadores:** Control simultáneo en el mismo teclado.
* **Sistema de Puntuación:** Marcador dinámico en pantalla.
* **Audio Reactivo:** Efectos de sonido al rebotar (sin bloquear el juego).
* **Física Básica:** Detección de colisiones y rebotes angulares simples.

## 🎮 Controles

| Acción | Jugador 1 (Izquierda) | Jugador 2 (Derecha) |
| :--- | :---: | :---: |
| **Mover Arriba** | Tecla `W` | Flecha `⬆️` |
| **Mover Abajo** | Tecla `S` | Flecha `⬇️` |
| **Iniciar / Pausa** | `Enter` | `Enter` |


## ⚙️ Instalación y Ejecución

1.  Asegúrate de tener Python instalado.
2.  Verifica que el archivo de audio `pong.mp3` esté en la **misma carpeta** que el script (es necesario para evitar errores de ejecución).
3.  Ejecuta el juego:
    ```bash
    python arcade_pong_poo_4.py
    ```


## 🚀 Competencias Técnicas Demostradas

Este proyecto evidencia el dominio de los siguientes conceptos de ingeniería de software:

### 1. Programación Orientada a Objetos (POO)
En lugar de usar funciones globales dispersas, el código encapsula la lógica en clases coherentes:
* **Herencia:** Las clases `Pala`, `Pelota` y `Marcador` heredan directamente de `turtle.Turtle`, extendiendo sus capacidades gráficas nativas.
* **Encapsulamiento:** La clase `JuegoPong` actúa como controlador principal, gestionando el estado del juego y la interacción entre objetos.

### 2. Optimización del Bucle de Juego (Game Loop)
Se ha desactivado el refresco automático de pantalla (`tracer(0)`) para controlar manualmente el renderizado con `update()`. Esto:
* Elimina el parpadeo de la pantalla.
* Aumenta significativamente los FPS (cuadros por segundo).
* Permite comprender cómo funcionan los motores de videojuegos a bajo nivel.

### 3. Programación Concurrente (Threading)
Uno de los retos comunes en Python es que reproducir sonido suele detener el programa hasta que el audio termina.
* **Solución aplicada:** Se implementó el módulo `threading` para ejecutar la función de sonido en un hilo secundario (`daemon=True`).
* **Resultado:** El juego mantiene su fluidez visual mientras el audio se reproduce en paralelo.

### 4. Arquitectura Event-Driven
El juego no es lineal, sino que reacciona a eventos. Se utiliza el patrón de escucha (`listen`) para vincular interrupciones de teclado con métodos específicos de las instancias de los objetos (`onkeypress`), permitiendo una respuesta en tiempo real.
