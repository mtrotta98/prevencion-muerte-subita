from src.core.entidades.entidades import Entidad
from src.core.db import db


def get_entidades(busqueda):
    """Esta funcion devuelve todas las entidades"""
    
    with db.session.no_autoflush:
        if busqueda:
            return Entidad.query.filter_by(razon_social=busqueda).all()
    return Entidad.query.all()


def get_entidad(id):
    """Devuelve una entidad buscada por su id"""
    return Entidad.query.filter_by(id=id).first()


def agregar_entidad(data):
    """Esta funcion da de alta una entidad"""
    entidad = Entidad(**data)
    db.session.add(entidad)
    db.session.commit()
    return entidad


def validar_datos_existentes(cuit, razon_social):
    """Esta funcion valida que los datos de alta de entidad no existan en la base de datos"""

    cuit_existente = Entidad.query.filter_by(cuit=cuit).first()
    razon_social_existente = Entidad.query.filter_by(razon_social=razon_social).first()
    if cuit_existente is not None:
        return False, "El cuit ya esta cargado en el sistema."
    elif razon_social_existente is not None:
        return False, "La razon social ya esta cargada en el sistema."
    else:
        return True, ""