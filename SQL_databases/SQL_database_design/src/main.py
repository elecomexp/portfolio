import pandas as pd
import sqlite3

from functions import intro_datos


##########################################################################################
# CREACIÓN BBDD
##########################################################################################

nombre_db = "./data/suministros.db"

try:
    connection = sqlite3.connect(nombre_db)
    error = False
except sqlite3.Error as e:
    print(e)
finally:
    if connection and error:
        connection.close()

cursor = connection.cursor()


##########################################################################################
# CREACIÓN DE TABLAS
##########################################################################################

# TABLA COLORES
query  = '''
  CREATE TABLE IF NOT EXISTS colores (
    color_id INTEGER PRIMARY KEY, 
    color text NOT NULL
    )
  '''
cursor.execute(query)

# TABLA CATEGORIAS
query  = '''
  CREATE TABLE IF NOT EXISTS categorias (
    categoria_id INTEGER PRIMARY KEY, 
    nombre text NOT NULL
  )
  '''
cursor.execute(query)

# TABLA CIUDADES
query  = '''
  CREATE TABLE IF NOT EXISTS ciudades (
  ciudad text PRIMARY KEY, 
  provincia text NOT NULL
  )
  '''
cursor.execute(query)

# TABLA PROVEEDORES
query  = '''
  CREATE TABLE IF NOT EXISTS proveedores (
    proveedor_id INTEGER PRIMARY KEY, 
    nombre text NOT NULL,
    direccion text NOT NULL,
    ciudad text NOT NULL,
    
    FOREIGN KEY(ciudad)
    REFERENCES ciudades(ciudad)
    )
  '''
cursor.execute(query)

# TABLA PIEZAS
query  = '''
  CREATE TABLE IF NOT EXISTS piezas (
    pieza_id INTEGER PRIMARY KEY, 
    nombre text NOT NULL,
    color_id INTEGER NOT NULL,
    precio REAL NOT NULL,
    categoria_id INTEGER NOT NULL,
    
    FOREIGN KEY(color_id)
    REFERENCES colores(color_id)
    FOREIGN KEY(categoria_id)
    REFERENCES categorias(categoria_id)
    )
  '''
cursor.execute(query)

# TABLA SUMINISTROS
query  = '''
  CREATE TABLE IF NOT EXISTS suministros (
    suministro_id INTEGER PRIMARY KEY, 
    pieza_id INTEGER NOT NULL,
    proveedor_id INTEGER NOT NULL,    
    cantidad INTEGER NOT NULL,
    fecha DATETIME NOT NULL,
    
    FOREIGN KEY(pieza_id)
    REFERENCES piezas(pieza_ids)
    FOREIGN KEY(proveedor_id)
    REFERENCES proveedores(proveedor_id)
    )
  '''
cursor.execute(query)


##########################################################################################
# NOMBRE DE LAS TABLAS CREADAS
##########################################################################################

print("\n"*1)
print("NOMBRE DE LAS TABLAS DE LA BASE DE DATOS")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")  
print(cursor.fetchall())
print("\n"*1)


##########################################################################################
# INSERTAMOS VALORES
##########################################################################################

# TABLA CATEGORIAS #
ruta = "./data/categorias.csv"
tabla = "categorias"
intro_datos(tabla, ruta, cursor)

# TABLA CIUDADES #
ruta = "./data/ciudades.csv"
tabla = "ciudades"
intro_datos(tabla, ruta, cursor)

# TABLA COLORES #
ruta = "./data/colores.csv"
tabla = "colores"
intro_datos(tabla, ruta, cursor)

# TABLA PIEZAS #
ruta = "./data/piezas.csv"
tabla = "piezas"
intro_datos(tabla, ruta, cursor)

# TABLA PROVEEDORES #
ruta = "./data/proveedores.csv"
tabla = "proveedores"
intro_datos(tabla, ruta, cursor)


# TABLA SUMINISTROS #
ruta = "./data/suministros.csv"
tabla = "suministros"
intro_datos(tabla, ruta, cursor)


##########################################################################################
# COMPROBAMOS QUE SE HAN INTRODUCIDO LOS VALORES 
##########################################################################################

print("COLORES")
query = '''
  SELECT *
  FROM colores
  '''
print(pd.read_sql(query, connection))
print("\n"*2)

print("CATEGORIAS")
query = '''
  SELECT *
  FROM categorias
  '''
print(pd.read_sql(query, connection))
print("\n"*2)

print("PIEZAS")
query = '''
  SELECT *
  FROM piezas
  '''
print(pd.read_sql(query, connection))
print("\n"*2)

print("SUMINISTROS")
query = '''
  SELECT *
  FROM suministros
  '''
print(pd.read_sql(query, connection))
print("\n"*2)

print("PROVEEDORES")
query = '''
  SELECT *
  FROM proveedores
  '''
print(pd.read_sql(query, connection))
print("\n"*2)

print("CIUDADES")
query = '''
  SELECT *
  FROM ciudades
  '''
print(pd.read_sql(query, connection))


##########################################################################################
# GUARDAR Y CERRAR
##########################################################################################

connection.commit()
connection.close()