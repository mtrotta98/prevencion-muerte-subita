from src.core.solicitudes.solicitudes import Solicitud
from src.core.db import db

def solicitudes(tipo):
    """Esta funcion devuelve todas las solicitudes existentes"""
    if tipo:
        return Solicitud.query.filter_by(estado=tipo).all()
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

def solicitudes_usuario(usuario):
    """Esta funcion devuelve las solicitudes que hizo un usuario"""
    
    if usuario:
        return Solicitud.query.filter_by(id_usuario=usuario.id).all()
    return None

def usuario_tipo_solicitudes(usuario, tipo):
    """Esta funcion devuelve las solicitudes de cierto tipo de un solo usuario"""

    solicitudes = solicitudes_usuario(usuario)
    if solicitudes:
        solicitudes_tipo = []
        for solicitud in solicitudes:
            if solicitud.estado == tipo:
                solicitudes_tipo.append(solicitud)
        return solicitudes_tipo
    return None    
