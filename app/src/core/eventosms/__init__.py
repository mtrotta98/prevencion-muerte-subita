from src.core.eventosms.eventosms import eventoMS
from src.core import sedes
from src.core.db import db

def get_all():
    """Esta funcion devuelve todos los eventoMS"""
    return eventoMS.query.order_by(db.asc(eventoMS.id)).all()

def get_by_id(id):
    """Retorna un eventoMS en específico"""
    return eventoMS.query.filter_by(id=id).first()

def get_by_sede(id_sede):
    """Retorna los eventoMS de una sede"""
    return eventoMS.query.filter_by(sede_id=id_sede).order_by(db.asc(eventoMS.id)).all()

def save(self):
    """ Salva los cambios"""
    db.session.add(self)
    db.session.commit()

def destroy(evento):
    """ Elimina un eventoMS de la BD. """
    db.session.delete(evento)
    db.session.commit()