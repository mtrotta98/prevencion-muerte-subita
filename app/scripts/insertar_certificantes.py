from faker import Faker
from werkzeug.security import generate_password_hash
import random
import psycopg2

fake = Faker()
lista_chars = ["#", "!", "$", "%", "&", "*"]
lista_provincias = []
lista_roles = []
lista_permisos = []

conexion = psycopg2.connect(host="localhost", database="prevencion_muerte_subita_db", user="postgres", password="proyecto")
cur = conexion.cursor()

cur.execute('SELECT id, nombre FROM public."Provincias"')

for data_prov in cur.fetchall():
    lista_provincias.append(data_prov)

for i in range(100000):

    id_rol =  3
    nombre = fake.first_name()
    apellido = fake.last_name()
    email = fake.email()
    usuario = fake.first_name() + "." + fake.last_name() + str(random.randint(0, 10000))
    fecha_nacimiento = fake.date_between(start_date="-40y", end_date="-20y")
    id_publico = fake.uuid4()
    contraseña = generate_password_hash(fake.word() + "." + fake.word() + random.choice(lista_chars), method="sha256")
    dni = random.randint(10000000, 99999999)

    query_insert = 'INSERT INTO public."Usuarios" (id_publico, nombre, apellido, usuario, "contraseña", dni, email, fecha_nacimiento, id_rol) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);'

    data_usuario = (id_publico, nombre, apellido, usuario, contraseña, dni, email, fecha_nacimiento, id_rol)

    cur.execute(query_insert, data_usuario)

    query_select = 'SELECT id FROM public."Usuarios" WHERE dni = %s AND usuario = %s'

    data_select = (str(dni), usuario)

    cur.execute(query_select, data_select)

    for data_select in cur.fetchall():
        id_usuario = data_select[0]

    id_provincia = random.choice(lista_provincias)[0]
    query_insert_user_prov = 'INSERT INTO public."Usuario_Provincia" (id_usuario, id_provincia) VALUES (%s, %s);'
    data_insert_user_prov = (id_usuario, id_provincia)

    cur.execute(query_insert_user_prov, data_insert_user_prov)
    
    conexion.commit()

conexion.close()