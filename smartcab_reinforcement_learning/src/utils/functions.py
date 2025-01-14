"""
functions.py

Autor: Lander Combarro Exposito
Creado: 15 enero 2025
Última modificación: 15 enero 2025

Descripción
-----------
Este archivo contiene una función de utilidad para la visualización de animaciones y manejo de frames
durante simulaciones o entrenamientos de aprendizaje por refuerzo.

Emplea librerías necesarias para limpiar la pantalla y para generar el intervalo entre frames.
"""

from time import sleep

from IPython.display import clear_output


def episode_animation(frames):
    """
    Muestra una animación basada en una secuencia de frames, representando el progreso de un episodio
    en una simulación o entrenamiento.

    Parámetros
    ----------
    frames : list
        Una lista de diccionarios, donde cada diccionario contiene información 
        sobre un frame, como estado, acción, recompensa y tiempo transcurrido.
    """
    for i, frame in enumerate(frames):  # Recorremos todo el conjunto de frames
        clear_output(wait=True)         # Limpiamos la "pantalla"
        print(frame['frame'])           # Visualizamos el "pantallazo" resultado de cada acción
        print(f"Timestep: {i + 1}")     # Aumentamos el contador de pasos/steps
        
        # Imprimimos el resto de valores correspondientes a cada frame y que hemos guardado al realizar el "aprendizaje"
        print(f"State: {frame['state']}") 
        print(f"Action: {frame['action']}")
        print(f"Reward: {frame['reward']}")
        print(f"Elapsed time (sec.): {frame['elapsed']}")
        
        # "Dormimos" el programa un tiempo para que nuestro ojo pueda ver la imagen antes de borrarla y mostrar la siguiente
        sleep(.1) 
        
