import numpy as np

from class_Barco import Barco
from variables import BARCOS, DIMENSION_TABLERO, VIDAS_JUGADOR

class Tablero:
    
    def __init__(self, jugador_id):
        '''
        1) Asigna el id del jugador al tablero
        2) Asigna dimensiones al tablero (inmutable) y lo inicia con agua (' ')
        3) Inicializa un diccionario de barcos para el tablero
        4) Posiciona los barcos en el tablero llamando al método Tablero.inicializar_barcos()
        '''
        self.jugador_id = jugador_id
        self.tablero = np.full((DIMENSION_TABLERO, DIMENSION_TABLERO), ' ')
        self.barcos = {}
        self.inicializar_barcos() # posiciona todos los barcos de forma aleatoria
        self.vidas_jugador = VIDAS_JUGADOR
        
        self.material = 'madera'
        self.dimension = DIMENSION_TABLERO
    
    
    def inicializar_barcos(self):
        '''
        Inicializa y posiciona los barcos definidos en la variable global "BARCOS"
        '''
        for (nombre, (eslora, cantidad)) in BARCOS.items():                         # Coge cada barco del diccionario
            for num_barco in range(cantidad):                                       # Coge cada barco del total por tipo
                colocado = False                                                    # Lo marca como no colocado
                while not colocado:             
                    fila = np.random.randint(0, DIMENSION_TABLERO)                  # Coge un valor entre 0 y la dimension del tablero
                    columna = np.random.randint(0, DIMENSION_TABLERO)               # Coge una columna entre 0 y la dimension del tablero
                    orientacion = np.random.choice(['H', 'V'])                      # Escoge una orientacion
                    if self._posicion_valida(fila, columna, eslora, orientacion):   # Comprueba si la posicion es valida
                        self._ubicar_barco(fila, columna, eslora, orientacion)      # Coloca el barco
                        id_barco = f'{nombre}_{str(num_barco)}'                     # Genera la identificacion del barco
                        self.barcos[id_barco] = Barco(id_barco, fila, columna, eslora, orientacion) # Añade el barco al diccionario de barcos
                        colocado = True


    def mostrar_tableros(self, tablero_oponente, *, ocultar_barcos = True):
        '''
        Muestra los dos tableros en paralelo.
        Si "ocultar_barcos = True" esconde los barcos del "tablero_oponente". Es decir cambiar 'O' (barco) por ' ' (agua)
        '''
        jugador_oponente = tablero_oponente.jugador_id
        
        if ocultar_barcos:
            tablero_oponente = np.where(tablero_oponente.tablero == 'O', ' ', tablero_oponente.tablero)
        else:
            tablero_oponente = tablero_oponente.tablero
        
        print(f'<< {self.jugador_id} >>{'\t'*5} << {jugador_oponente} >>')            
         
        for fila in range(DIMENSION_TABLERO):
            print(self.tablero[fila], '\t', tablero_oponente[fila])
 
 
    def disparar(self, tablero_oponente, coordenadas):
        '''
        Efectua un disparo, revisando si este ha caído sobre la posición de un barco.
        --> Return: bool
        '''
        disparo_bueno = False   # Usado para saber si hemos dado a algun barco   
        agua = False            # Usado para saber si hemos tirado al agua
        for barco in tablero_oponente.barcos.keys():                                # Para cada barco miro si ya está la tirada en el tablero
            if tablero_oponente.barcos[barco].tocado(coordenadas):
                if tablero_oponente.tablero[coordenadas[0],coordenadas[1]] == "X":  # Si ha tocado y ya estaba no es tiro con exito ni agua
                    disparo_bueno = False
                    agua = False   
                else:
                    tablero_oponente.tablero[coordenadas[0],coordenadas[1]] = "X"   # Si ha tocado y no estaba es tiro con exito y no es agua
                    disparo_bueno = True
                    agua = False
                break
            else:
                if tablero_oponente.tablero[coordenadas[0],coordenadas[1]] == "X":  # Si no ha tocado y ya estaba es tiro sin exito y no es agua
                    disparo_bueno = False
                    agua = False
                else:
                    tablero_oponente.tablero[coordenadas[0],coordenadas[1]] = "-"   # Si no ha tocado y no estaba es tiro sin exito y es agua
                    disparo_bueno = False
                    agua = True
        if agua:
            print("¡Agua!\n")
        if disparo_bueno:   # Si el disparo ha tocado o hundido puede seguir el jugador y retorno True, si no retorno False
            return True
        else:
            return False
     
     
    def _posicion_valida(self, fila, columna, eslora, orientacion):
        '''
        ### Método privado ###
        Comprueba si el barco se puede ubicar en el tablero.
            --> True  : El barco se puede ubicar en el tablero.
            --> False : El barco no se puede ubicar en el tablero (excede las dimensiones del 
                        tablero o se solapa con otro barco)
        '''
        if orientacion == 'H':
            if columna + eslora > DIMENSION_TABLERO:
                return False
            for i in range(eslora):
                if self.tablero[fila, columna + i] != ' ':
                    return False
        else:
            if fila + eslora > DIMENSION_TABLERO:
                return False
            for i in range(eslora):
                if self.tablero[fila + i, columna] != ' ':
                    return False
        return True        
      
                       
    def _ubicar_barco(self, fila, columna, eslora, orientacion):
        '''
        ### Método privado ###
        Ubica en el tablero la posición de un barco: pinta "O" en las posiciones que ocupe en barco.
        '''
        if orientacion == 'H':
            for i in range(eslora):
                self.tablero[fila, columna + i] = 'O'
        else:
            for i in range(eslora):
                self.tablero[fila + i, columna] = 'O'