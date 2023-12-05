from faker import Faker
import random
import psycopg2

fake = Faker('es_ES')

conexion = psycopg2.connect(host="localhost", database="prevencion_muerte_subita_db", user="postgres", password="proyecto")
cur = conexion.cursor()

# Lista de tipos de instituciones
tipos_institucion = ['Universidad', 'Hospital', 'Biblioteca', 'Museo', 'Gimnasio', 'Centro Comercial', 'Estadio', 'Teatro', 'Restaurante', 'Parque', 'Cine', 'Escuela', 'Jardin', 'Guarderia', 'Bar', 'Discoteca']

for _ in range(100000):
        
    cuit=fake.unique.random_number(digits=11),
    razon_social=fake.company(),
    tipo_institucion=random.choice(tipos_institucion),
    sector=random.choice(['privado', 'publico'])

    query_insert = 'INSERT INTO public."Entidades" (cuit, razon_social, tipo_institucion, sector) VALUES (%s, %s, %s, %s);'

    data_entidad = (cuit, razon_social, tipo_institucion, sector)

    cur.execute(query_insert, data_entidad)

    conexion.commit()

conexion.close()