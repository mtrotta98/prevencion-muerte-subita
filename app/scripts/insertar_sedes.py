from faker import Faker
import random
import psycopg2
import pandas as pd
import os


fake = Faker('es_ES')

conexion = psycopg2.connect(host="localhost", database="prevencion_muerte_subita_db", user="postgres", password="proyecto")
cur = conexion.cursor()

lista_provincias = []

cur.execute('SELECT id, nombre FROM public."Provincias"')

for data_prov in cur.fetchall():
    lista_provincias.append(data_prov)

file_path = str(os.getcwd()) + "\localidades.xlsx"

df = pd.read_excel(file_path,engine='openpyxl',dtype=object,header=None)

print(df.head())

complete_list = df.values.tolist()

for row in complete_list:
    latitud = row[3]
    logintud = row[4]
    nombre_provincia = row[7]
    print(f"""
            Latitud: {latitud},
            Longitud: {logintud},
            Provincia: {nombre_provincia}
            """)
    
    id_provincia = None
    for provincia in lista_provincias:
        if provincia[1].upper() == nombre_provincia.upper():
            id_provincia = provincia[0]
            break


def generar_datos():

    nombre = fake.company()
    flujo_personas = random.randint(200, 5000)
    superficie = random.random()
    personal_estable = random.randint(20, 2000)
    pisos = random.randint(1, 10)
    estado = 'En proceso de ser cardioasistido'
    id_entidad = random.randint(1, 100000)
    
    return nombre, flujo_personas, superficie, personal_estable, pisos, estado, id_entidad

def buscar_nombre_provincia(numero):
    diccionario_provincias = {1: 'Buenos Aires', 2: 'Catamarca', 3: 'Chaco', 4: 'Chubut', 5: 'Cordoba', 6: 'Corrientes', 7: 'Entre Rios', 8: 'Formosa', 9: 'Jujuy', 10: 'La Pampa', 11: 'La Rioja', 12: 'Mendoza', 13: 'Misiones', 14: 'Neuquen', 15: 'Rio Negro', 16: 'Salta', 17: 'San Juan', 18: 'San Luis', 19: 'Santa Cruz', 20: 'Santa Fe', 21: 'Santiago del Estero', 22: 'Tierra del Fuego', 23: 'Tucuman'}
    nombre_provincia = diccionario_provincias.get(numero)
    return nombre_provincia

for i in range(1000000):
    row = complete_list[i % len(complete_list)]
    latitud = row[3]
    longitud = row[4]
    nombre_provincia = row[7]

    print(latitud)
    print(longitud)
    print(nombre_provincia)

    if isinstance(nombre_provincia, float):
        # Maneja el caso en el que nombre_provincia es un número de punto flotante
        # Por ejemplo, podrías buscar el nombre de la provincia usando el número de punto flotante
        nombre_provincia = buscar_nombre_provincia(nombre_provincia)

    if nombre_provincia is not None:
        nombre_provincia = str(nombre_provincia)
        # print(str(nombre_provincia).upper())
        # print(str(provincia[1].upper()))
        id_provincia = next((provincia[0] for provincia in lista_provincias if provincia[1] is not None and str(provincia[1]).upper() == nombre_provincia.upper()), None)
        print(f"id_provincia: {id_provincia}")  # Imprime el valor de id_provincia
    
    if id_provincia is not None:
        nombre, flujo_personas, superficie, personal_estable, pisos, estado, id_entidad = generar_datos()
        
        query_insert = 'INSERT INTO public."Sedes" (latitud, longitud, nombre, flujo_personas, superficie, personal_estable, pisos, estado, id_provincia, id_entidad) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'

        data_sede = (latitud, longitud, nombre, flujo_personas, superficie, personal_estable, pisos, estado, id_provincia, id_entidad)
    
        cur.execute(query_insert, data_sede)

        conexion.commit()
    

conexion.close()