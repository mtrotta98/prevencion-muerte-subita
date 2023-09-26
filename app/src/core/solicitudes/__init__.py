from src.core.solicitudes.solicitudes import Solicitud
from src.core.db import db

def solicitudes():
    """Esta funcion devuelve todas las solicitudes existentes"""
    return Solicitud.query.all()

def get_solicitud(id):
    """Esta funcion devuelve una solicitud por su id"""
    return Solicitud.query.filter_by(id=id).first()

def actualizar_solicitud(data):
    """Esta funcion actualiza la informacion de la solicitud"""
    solicitud = Solicitud.query.get(data["id"])
    solicitud.estado = data["estado"]
    solicitud.razon = data["razon"]
    db.session.commit()
    return solicitud