from src.core.deas.deas import DEA
from src.core.db import db

def get_all():
    """Esta funcion devuelve todos los DEAS"""
    return DEA.query.all()

def get_by_id(id):
    return DEA.query.filter_by(id=id).first()

def save(self):
    """ Salva los cambios"""
    db.session.add(self)
    db.session.commit()

@staticmethod
def destroy(Responsable):
    """ Elimina un DEA de la BD. """
    db.session.delete(Responsable)
    db.session.commit()

