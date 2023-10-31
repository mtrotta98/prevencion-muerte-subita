from src.core.deas.deas import DEA
from src.core.db import db

def get_all():
    """Esta funcion devuelve todos los DEAS"""
    return DEA.query.order_by(db.asc(DEA.id)).all()

def get_by_id(id):
    """Retorna un DEA en específico"""
    return DEA.query.filter_by(id=id).first()

def get_by_sede(id_sede):
    """Retorna los DEA de una sede"""
    return DEA.query.filter_by(sede_id=id_sede).order_by(db.asc(DEA.id)).all()

def save(self):
    """ Salva los cambios"""
    db.session.add(self)
    db.session.commit()

def deactivate(dea):
    """Desactiva el DEA"""
    dea.activo = False
    save(dea)


@staticmethod
def destroy(dea):
    """ Elimina un DEA de la BD. """
    db.session.delete(dea)
    db.session.commit()

