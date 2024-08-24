import pandas as pd
import sqlite3


def intro_datos(tabla, ruta, cursor, sep=';'):
    '''
    Inserta datos de un archivo CSV en una tabla de una base de datos SQLite.

    Args:
        tabla (str): Nombre de la tabla de destino en la base de datos.
        ruta (str): Ruta del archivo CSV a cargar.
        cursor (sqlite3.Cursor): Cursor de la conexión a la base de datos SQLite.
        sep (str, optional): Delimitador utilizado en el archivo CSV. Por defecto, ';'.

    Esta función realiza los siguientes pasos:
        1. Carga el archivo CSV en un DataFrame de pandas.
        2. Establece las columnas del DataFrame como índice.
        3. Itera sobre cada fila del DataFrame y construye una consulta SQL para insertar los datos.
        4. Ejecuta la consulta utilizando el cursor proporcionado.

    Nota:
        * Los valores numéricos en el CSV se convierten a cadenas para evitar problemas de compatibilidad con SQLite.
        * Esta función asume que la estructura del CSV coincide con la estructura de la tabla en la base de datos.
    '''
    # cargar .csv
    df_csv = pd.read_csv(ruta, sep=sep)

    # quitamos el indice implicito y dejamos solo las columnas
    df_csv.set_index(list(df_csv.keys()), inplace=True)   
    
    # tupla con los nombres de las columnas para poder ser usado directamente en la query
    columnas = tuple(df_csv.index.names)    

    for i in range(0, len(df_csv.index)):
        # Convertir los valores numéricos a cadenas para evitar problemas con la representación de numpy
        row_values = tuple(str(val) for val in df_csv.index[i])
        query = f"INSERT INTO {tabla} {columnas} VALUES {row_values}"
        cursor.execute(query)
