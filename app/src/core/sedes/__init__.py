from src.core.sedes.sedes import Sede
from src.core.db import db


def get_sedes(busqueda):
    """Esta funcion devuelve todas las sedes"""

    with db.session.no_autoflush:
        if busqueda:
            return Sede.query.filter_by(nombre=busqueda).all()
    return Sede.query.all()

def get_sedes_provincia(id_provincia):
    """Esta funcion devuelve todas las sedes asociadas a una provincia"""

    with db.session.no_autoflush:
        if id_provincia:
            return Sede.query.fiter_by(id_provincia=id_provincia).all()
    return Sede.query.all()


def get_sede(id):
    """Devuelve una sede buscada por su id"""
    return Sede.query.filter_by(id=id).first()


def agregar_sede(data):
    """Esta funcion da de alta una sede"""

    sede = Sede(**data)
    db.session.add(sede)
    db.session.commit()
    return sede


def validar_datos_existentes(nombre):
    """Esta funcion valida que los datos de alta de sede no existan en la base de datos"""

    nombre_existente = Sede.query.filter_by(nombre=nombre).first()
    if nombre_existente is not None:
        return False, "La sede ya esta cargada en el sistema."
    else:
        return True, ""
    
def get_sedes_asociadas(id, busqueda):
    """Devuelve las sedes asociadas a una entidad"""

    id_entidad = id
    sedes = get_sedes(busqueda)
    sedes_asociadas = []
    for sede in sedes:
        id_sede = sede.id_entidad
        if id_sede == id_entidad:
            sedes_asociadas.append(sede)
   
    return sedes_asociadas

def get_sedes_por_provincia(id, id_provincia):
    """Devuelve las sedes asociadas a una entidad y provincia"""

    id_entidad = id
    sedes = get_sedes_provincia(id_provincia)
    sedes_provincia = []
    for sede in sedes:
        id_sede = sede.id_entidad
        if id_sede == id_entidad:
            sedes_provincia.append(sede)
    
    return sedes_provincia

