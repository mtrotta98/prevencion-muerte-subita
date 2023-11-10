from datetime import datetime, timedelta
from src.core.visitas.visitas import Visita
from src.core.db import db

def get_visitas():
    """Esta funcion devuelve todas las visitas"""
    return Visita.query.all()

def get_visita_id(id):
    """Esta funcion devuelve una visita por su id"""

    if id:
        return Visita.query.filter_by(id=id).first()
    return None

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

def modificar_visita(data):
    """ Esta funcion modifica los datos de una visita """
    visita = get_visita_id(data['id'])
    visita.resultado = data['resultado']
    visita.observacion = data['observacion']
    db.session.commit()
    return visita

def get_visita_sede(id):
    """Esta funcion devuelve las visitas de una sede"""

    if id:
        return Visita.query.filter_by(id_sede = id).all()
    return Visita.query.all()

def verificar_visita_aprobada(id_sede):
    """ Esta funcion devuelve si la sede ya tiene una visita aprobada """
    visitas = get_visita_sede(id_sede)
    if visitas:
        for visita in visitas:
            if visita.resultado is not None and not visita.resultado:
                return True
    return False

