from datetime import datetime, timedelta
from src.core.visitas.visitas import Visita
from src.core.db import db

def get_visitas():
    """Esta funcion devuelve todas las visitas"""
    return Visita.query.all()

def agregar_visita():
    """Esta funcion agrega una visita a una sede"""
    fecha = datetime.now().date() + timedelta(days=7)
    data = {
        "fecha": fecha
    }

    visita = Visita(**data)
    db.session.add(visita)
    db.session.commit()
    return visita