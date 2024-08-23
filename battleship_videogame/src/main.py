import numpy as np
import time

from class_Tablero import Tablero
from functions import solicitar_coordenadas

def juego():
    '''
    Función principal del juego.
    '''
    
    print('\n~~~~~~~~~~~~~~~~~ Bienvenidx a Hundir la Flota ~~~~~~~~~~~~~~~')
    print('--> Escriba "exit" en cualquier momento para terminar el juego.\n')
    
    tablero_jugador = Tablero(jugador_id = 'Jugador') 
    tablero_maquina = Tablero(jugador_id = 'Máquina')

    tablero_jugador.mostrar_tableros(tablero_maquina, ocultar_barcos=True)  # ocultar_barcos = False para ver la ubicación de los barcos en ambos tableros

    turno = 1
    juego_terminado = False
    
    while not juego_terminado: 
             
        turno_jugador = True
        turno_maquina = True
        
        while turno_jugador:
            
            print(f'\n------------ Turno: {turno} ------------')
            
            coordenadas = solicitar_coordenadas()
            
            # --------------- Descomentar esta parte si se quiere hacer una partida automática ---------------
            # time.sleep(3)                                                                 # Dejamos 3 segundos para que la respuesta no sea inmediata
            # coordenadas = tuple(np.random.randint(0,tablero_maquina.dimension,2))         # Generamos el disparo random de para el jugador
            # print(f"El JUGADOR dispara a: ({str(coordenadas[0])},{str(coordenadas[1])})") # Indica el disparo
            # ------------------------------------------------------------------------------------------------
            
            turno_jugador = tablero_jugador.disparar(tablero_maquina, coordenadas)            
            
            if turno_jugador:
                tablero_maquina.vidas_jugador -= 1
                if tablero_maquina.vidas_jugador == 0:
                    print('Fin de partida: ¡GANASTE!\n')
                    turno_jugador = False
                    turno_maquina = False
                    juego_terminado = True
                else:
                    print("Continúas jugando...\n")
            

            
            tablero_jugador.mostrar_tableros(tablero_maquina)  
            turno += 1
            
        while turno_maquina:
            print(f'\n------------ TURNO: {turno}. ------------')
            print("Turno de la máquina. Pensando...")
            
            time.sleep(2)                                                                 # Dejamos 3 segundos para que la respuesta no sea inmediata
            coordenadas = tuple(np.random.randint(0,tablero_maquina.dimension,2))         # Generamos el disparo random de la máquina
            print(f"La máquina dispara a: ({str(coordenadas[0])},{str(coordenadas[1])})") # Indica el disparo
            
            turno_maquina = tablero_maquina.disparar(tablero_jugador, coordenadas)        # Realizamos el disparo de la máquina
            
            if turno_maquina:
                tablero_jugador.vidas_jugador -= 1
                if tablero_jugador.vidas_jugador == 0:
                    print('FIN DE PARTIDA: Ganó la máquina.\n')
                    turno_maquina = False
                    juego_terminado = True   
                else:
                    print("La maquina acertó, sigue ella...\n")                    
            
                                        
            
            tablero_jugador.mostrar_tableros(tablero_maquina)       
            turno += 1


if __name__ == "__main__":
    juego()  