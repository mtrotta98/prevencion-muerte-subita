from faker import Faker
from werkzeug.security import generate_password_hash
import random
import psycopg2

fake = Faker()
lista_chars = ["#", "!", "$", "%", "&", "*"]
lista_roles = []
lista_permisos = []

conexion = psycopg2.connect(host="localhost", database="prevencion_muerte_subita_db", user="postgres", password="proyecto")
cur = conexion.cursor()

for i in range(100000):
    print(i)

    id_rol =  2
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

    query_select = 'SELECT id FROM public."Usuarios" WHERE dni = %s AND usuario = %s AND email = %s AND id_publico = %s AND id_rol = %s'

    data_select = (str(dni), usuario, email, id_publico, "2")

    cur.execute(query_select, data_select)

    for data_select in cur.fetchall():
        cant_sedes = random.randint(1, 3)
        id_usuario = data_select[0]
        for i in range(cant_sedes):
            id_sede = random.randint(1, 99445)
            query_insert_user_sede = 'INSERT INTO public."Usuario_Sede" (id_usuario, id_sede) VALUES (%s, %s);'
            data_insert_user_sede = (id_usuario, id_sede)

            cur.execute(query_insert_user_sede, data_insert_user_sede)
    
    conexion.commit()

conexion.close()