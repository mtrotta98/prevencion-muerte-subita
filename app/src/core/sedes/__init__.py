from src.core.sedes.sedes import Sede
from src.core.db import db
from src.core.usuarios import get_usuario


def get_sedes():
    """Esta funcion devuelve todas las sedes"""
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
    
def get_sedes_asociadas(id):
    """Devuelve las sedes asociadas a una entidad"""

    id_entidad = id
    sedes = get_sedes()
    sedes_asociadas = []
    for sede in sedes:
        id_sede = sede.id_entidad
        if id_sede == id_entidad:
            sedes_asociadas.append(sede)
   
    return sedes_asociadas
def relacionar_representante_sede(id_representante, id_sede):
    """Esta funcion genera la relacione entre un administrador provincial y una sede"""
    sede = get_sede(id_sede)
    admin = get_usuario(id_representante)
    sede.usuarios.append(admin)
    db.session.commit()
