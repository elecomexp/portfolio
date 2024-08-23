class Barco:

    def __init__(self, id_barco, fila, columna, eslora, orientacion):
        '''
        Constructor de un barco.
        '''
        self.id_barco = id_barco
        self.fila = fila
        self.columna = columna
        self.eslora = eslora
        self.orientacion = orientacion
        self.tocadas = []           # Guarda las celdas tocadas para saber si está hundido o no.
        self.vida = eslora

    
    def hundido(self):
        '''
        Comprueba si un barco se ha hundido completamente. Es decir si ha perdido todas sus vidas
        --> True : El barco tiene 0 vidas.
        --> False : Cualquier otro caso.
        '''
        self.vida -= 1
        return self.vida == 0       # True si el barco se ha hundido. 


    def tirada_repetida(self, coordenadas):  
        '''
        Comprueba si las coordenadas escogidas (típicamente sobre las que se efectua un disparo) ya habían sido seleccionadas.
        '''                                         
        for tocada in self.tocadas:
            if tocada[0] == coordenadas[0] and tocada[1] == coordenadas[1]:
                print("Ya se había disparado a esta posición.")
                return True
            return False


    def tocado(self,coordenadas):
        '''
        Vamos a mirar si el disparo ha tocado al barco.
        '''
        repetida = self.tirada_repetida(coordenadas)                             # Compruebo que no esté repetida la tirada
    
        lista_posiciones = self.posiciones_barco()                               # Se crea la lista con las posiciones del barco

        for posicion in lista_posiciones:                                        # Ahora comprobamos si da en alguna
            if (coordenadas[0]==posicion[0]) and (coordenadas[1]==posicion[1]):  # Si la tirada ha tocado alguna posicion la guardo en la lista de tocadas              
                self.tocadas.append([coordenadas[0],coordenadas[1]])                
                if (not repetida):                                               # Si la tirada no está repetida miro a ver si está hundido
                    if self.hundido():
                        print(f"{self.id_barco} ¡TOCADO Y HUNDIDO!")
                    else:                                                        # Si no está hundido y no está repetida imprimo "Tocado"
                        if not repetida:
                            print("¡Tocado!")
                    return True                                                  # Devuelvo True si ha sido tirada con éxito y False si no
                else:
                    return False
        return False
    
    
    def posiciones_barco(self):
        '''
        Genera una lista con todas las posiciones que ocupa un barco.
        '''
        lista_posiciones = []
                               
        if self.orientacion == 'H':
            posicionX = self.fila
            for zona in range(self.eslora):
                posicionY = zona+self.columna
                lista_posiciones.append([posicionX,posicionY])
        elif self.orientacion == 'V':           
            posicionY = self.columna
            for zona in range(self.eslora):
                posicionX = zona+self.fila
                lista_posiciones.append([posicionX,posicionY])
                
        return lista_posiciones