from faker import Faker
import random
import psycopg2

fake = Faker()

conexion = psycopg2.connect(host="localhost", database="prevencion_muerte_subita_db", user="postgres", password="proyecto")
cur = conexion.cursor()
ids_certificantes = []

query_select_certificantes = 'SELECT id FROM public."Usuarios" WHERE id_rol = %s'
data_select_certificantes = ('3')

cur.execute(query_select_certificantes, data_select_certificantes)

for data_select in cur.fetchall():
    ids_certificantes.append(data_select[0])

estado = "\'Espacio cardioasistico certificado\'"

query_select_sedes_certificadas = 'SELECT id FROM public."Sedes" WHERE estado = {0}'.format(estado)

cur.execute(query_select_sedes_certificadas)

for data_select in cur.fetchall():
    id_sede = data_select[0]
    id_usuario = random.choice(ids_certificantes)

    query_insert_ddjj = 'INSERT INTO public."Ddjj" (personal_capacitado, dea_señalizado, responsable, protocolo_accion, sistema_emergencia, cantidad_dea, id_sede) VALUES (%s, %s, %s, %s, %s, %s, %s);'
    data_insert_ddjj = ("1", "1", "1", "1", "1", "1", id_sede)

    cur.execute(query_insert_ddjj, data_insert_ddjj)

    query_insert_visita = 'INSERT INTO public."Visitas" (fecha, resultado, id_sede, id_certificante) VALUES (%s, %s, %s, %s);'
    fecha = fake.date_between(start_date="-3y", end_date="-1y")
    data_insert_visita = (fecha, "1", id_sede, id_usuario)

    cur.execute(query_insert_visita, data_insert_visita)

    conexion.commit()

conexion.close()