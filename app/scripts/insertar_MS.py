from faker import Faker
import random
import psycopg2
import requests
import json

# marcas [0..n-1]
# cant_marcas = len(marcas)
# modelos [1..9] [0..n-1]
# cant_modelos = len(modelos[x])
# modelo = str(modelos[x][y-1]["nombre"])
random.seed()
fake = Faker('es_ES')

modelos = {}
res = requests.get('https://api.claudioraverta.com/deas/')
marcas = json.loads(res.text)

for marca in marcas:
    res = requests.get('https://api.claudioraverta.com/deas/'+str(marca["id"])+'/modelos/')
    modelos [marca["id"]] = json.loads(res.text)

def loadDea(cur,sede_id):
    deaMarca = random.randint(1, len(marcas))
    # nModeloDea = random.randint(1, len(modelos[deaMarca]))
    deaDenominacion = fake.sentence()
    deaModelo = str(modelos[deaMarca][random.randint(1, len(modelos[deaMarca]))-1]["nombre"])
    deaNSerie = str(fake.uuid4())
    deaSolidario = bool(random.getrandbits(1))
    deaActivo = bool(random.getrandbits(2))  # Mas activos que inactivos
    deaMantenimiento = fake.date_this_year()
    query = 'INSERT INTO public."deas" (denominacion, marca, modelo, nserie, ultimoMantenimiento, solidario, activo, sede_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);'
    data = (deaDenominacion, deaMarca, deaModelo, deaNSerie, deaMantenimiento, deaSolidario, deaActivo, sede_id)
    cur.execute(query, data)

def loadResp(cur,sede_id):
    resNombre = fake.first_name();
    resApellido = fake.last_name()
    resDNI = random.randint(10000000, 99999999)
    resEmail = fake.email()
    resTelefono = fake.phone_number()
    query = 'INSERT INTO public."Responsables" (nombre, apellido, dni, email, teléfono, sede_id) VALUES (%s, %s, %s, %s, %s, %s );'
    data = (resNombre, resApellido, resDNI, resEmail, resTelefono, sede_id)
    cur.execute(query, data)

def loadEventMS(cur,sede_id):
    emsDescripcion = fake.text(max_nb_chars=250)
    emsFecha = fake.date_time_this_year()
    emsSexo = random.randint(1,3)
    emsEdad = random.randint(1,99)
    emsSobrevive = bool(random.getrandbits(2))  # Mas supervivientes que muertos
    emsUsoDea = bool(random.getrandbits(1))
    if emsUsoDea:
        emsUsosDea = random.randint(1,5)
        emsMarca = random.randint(1, len(marcas))
        emsModelo = modelos[emsMarca][random.randint(1, len(modelos[emsMarca]))-1]["nombre"]
    else:
        emsUsosDea = 0
        emsMarca=None
        emsModelo=None
    emsUsoRCP = bool(random.getrandbits(1))
    if emsUsoRCP:
        emsTiempoRCP = random.randint(1,5)
    else:
        emsTiempoRCP = 0
    if (bool(random.getrandbits(3))):   # 7 de cada 8 casos se identifica a la persona
        emsNombre = fake.first_name()
        emsApellido = fake.last_name()
    else:
        emsNombre = "Desconocido"
        emsApellido = "Desconocido"
    query = 'INSERT INTO public."eventosms" (sede_id, fecha, sexo, edad, sobrevive, usoDea, usosDEA, usoRCP, tiempoRCP, modelo, marca, descripcion, nombre, apellido) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'
    data = (sede_id, emsFecha, emsSexo, emsEdad, emsSobrevive, emsUsoDea, emsUsosDea, emsUsoRCP, emsTiempoRCP, emsModelo, emsMarca, emsDescripcion, emsNombre, emsApellido)
    cur.execute(query, data)

conexion = psycopg2.connect(host="localhost", database="prevencion_muerte_subita_db", user="postgres", password="proyecto")
cur = conexion.cursor()
query_select = 'SELECT id FROM public."Sedes"'
cur.execute(query_select)
sedes = cur.fetchall()
for sede in sedes:
    print(sede[0])
    insertDeas = bool(random.getrandbits(2))  # Mas activos que inactivos;
    for i in range(random.randint(0,5)):
        insertDeas=True
        loadDea(cur,sede)
    if insertDeas:
        for i in range(random.randint(1,2)):
            loadResp(cur,sede)
        if not bool(random.getrandbits(2)):
            for i in range(random.randint(1,3)):
                loadEventMS(cur,sede)
    conexion.commit()
conexion.close()
