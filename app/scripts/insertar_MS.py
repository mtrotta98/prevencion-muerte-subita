from faker import Faker
from werkzeug.security import generate_password_hash
import random
import psycopg2
import requests
import json 
import loremipsum

conexion = psycopg2.connect(host="localhost", database="prevencion_muerte_subita_db", user="postgres", password="proyecto")
cur = conexion.cursor()

modelos = []
modelos.append()
res = requests.get('https://api.claudioraverta.com/deas/')
marcas = json.loads(res.text)
for marca in marcas:
    res = requests.get('https://api.claudioraverta.com/deas/'+str(marca)+'/modelos/')
    modelos.append(json.loads(res.text))

def loadDea():
    marca = random.randit(1, marcas.count)
    res = requests.get('https://api.claudioraverta.com/deas/'+str(marca)+'/modelos/')
    modelos = json.loads(res.text)
    modelo = random.randit(1, modelos.count)


def loadResp():
    return None


query_select = 'SELECT id FROM public."Sedes"'
cur.execute(query_select)
for sede in cur.fetchall():
    insertDeas = False;
    id_dea=1
    id_responsable=1
    id_eventoMs=1
    for i in range(random.randit(0,10)):
        insertDeas=True
        dea = loadDea(id_dea)
        id_dea=id_dea+1
        query = 'INSERT INTO public."deas" (id, denominacion, marca, modelo, nSerie, ultimoMantenimiento, solidario, activo, sede_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);'
        data = (dea.id, dea.denominacion, dea.marca, dea.modelo, dea.nSerie, dea.ultimoMantenimiento, dea.solidario, dea.activo, dea.sede_id)
        cur.execute(query, data)
    if insertDeas:
        responsable=loadResp(id_responsable)
        id_responsable=id_responsable+1
        query = 'INSERT INTO public."Responsables" (id, nombre, apellido, dni, email, teléfono, sede_id) VALUES (%s, %s, %s, %s, %s, %s, %s, );'
        data = (responsable.id, responsable.nombre, responsable.apellido, responsable.dni, responsable.email, responsable.teléfono, responsable.sede_id)
        cur.execute(query, data)
    
    conexion.commit()

conexion.close()