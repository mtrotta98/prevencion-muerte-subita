from src.core.responsables.responsables import Responsable
from src.core.db import db

def get_all():
    """Esta funcion devuelve todos los responsables"""
    return Responsable.query.all()

def get_by_id(id):
    """Retorna un responsable en específico"""
    return Responsable.query.filter_by(id=id).first()

def get_by_sede(id_sede):
    """Retorna los responsables de una sede"""
    return Responsable.query.filter_by(sede_id=id_sede).all()

def save(self):
    """ Salva los cambios"""
    db.session.add(self)
    db.session.commit()

def destroy(Responsable):
    """ Elimina un Responsable de la BD. """
    db.session.delete(Responsable)
    db.session.commit()

def get_responsables_aviso(lista_sedes):
    """ Devuelve los responsables de un grupo de sedes """
    lista_id_sedes = []
    responsables_aviso = []
    for sede in lista_sedes:
        lista_id_sedes.append(sede.id)
    all_responsables = get_all()
    for responsable in all_responsables:
        if responsable.sede_id in lista_id_sedes:
            responsables_aviso.append(responsable)
    return responsables_aviso

