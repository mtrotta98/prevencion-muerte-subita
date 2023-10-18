from src.core.responsables.responsables import Responsable
from src.core.db import db

def get_all():
    """Esta funcion devuelve todos los responsables"""
    return Responsable.query.all()

def get_by_id(id):
    return Responsable.query.filter_by(id=id).first()

def save(self):
    """ Salva los cambios"""
    db.session.add(self)
    db.session.commit()

@staticmethod
def destroy(Responsable):
    """ Elimina un Responsable de la BD. """
    db.session.delete(Responsable)
    db.session.commit()

