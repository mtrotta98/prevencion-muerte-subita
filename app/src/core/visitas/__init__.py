from datetime import datetime, timedelta
from src.core.visitas.visitas import Visita
from src.core.db import db

def get_visitas():
    """Esta funcion devuelve todas las visitas"""
    return Visita.query.all()

def get_visitas_aprobadas():
    """Esta funcion devuelve todas las visitas que fueron aprobadas"""
    return Visita.query.filter_by(resultado=True).all()

def agregar_visita(id_sede):
    """Esta funcion agrega una visita a una sede"""
    fecha = datetime.now().date() + timedelta(days=7)
    data = {
        "fecha": fecha,
        "id_sede": id_sede,
    }

    visita = Visita(**data)
    db.session.add(visita)
    db.session.commit()
    return visita

def get_visita_sede(id):
    """Esta funcion devuelve las visitas de una sede"""

    if id:
        return Visita.query.filter_by(id_sede = id).all()
    return Visita.query.all()

