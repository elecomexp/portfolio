# Definición de los barcos
# str(nombre_barco) : tuple(eslora, numero_de_barcos_en_el_juego)
BARCOS = {
    'Portaaviones' : (4, 1),
    'Acorazado'    : (3, 2),
    'Submarino'    : (2, 3),
    'Destructor'   : (1, 4)
    }

# Diccionario con menos barcos para entrenar
# BARCOS = {
#     'Submarino'  : (2, 1),
#     'Destructor' : (1, 1)
#     }

# Dimension del tablero: (DIMENSION_TABLERO x DIMENSION_TABLERO)
DIMENSION_TABLERO = 10

# Vidas del jugador
VIDAS_JUGADOR = 0
for barco in BARCOS.keys():
    VIDAS_JUGADOR += BARCOS[barco][0] * BARCOS[barco][1]