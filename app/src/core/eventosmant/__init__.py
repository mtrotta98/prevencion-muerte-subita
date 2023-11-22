from src.core.eventosmant.eventosmant import eventoMant
from src.core import deas
from src.core.db import db

def get_all():
    """Esta funcion devuelve todos los eventos"""
    return eventoMant.query.order_by(db.asc(eventoMant.id)).all()

def get_by_id(id):
    """Retorna un evento en específico"""
    return eventoMant.query.filter_by(id=id).first()

def get_by_dea(dea_id):
    """Retorna los evento de un DEA"""
    return eventoMant.query.filter_by(dea_id=dea_id).order_by(db.asc(eventoMant.id)).all()

def save(self):
    """ Salva los cambios"""
    db.session.add(self)
    db.session.commit()

def destroy(evento):
    """ Elimina un evento de la BD. """
    db.session.delete(evento)
    db.session.commit()