from src.core.ddjj.ddjj import Ddjj
from src.core.db import db


def get_ddjj():
    """Esta funcion devuelve todas las declaraciones juradas"""
    return Ddjj.query.all()

def verificar_ddjj_existente(id):
    """Esta funcion verifica que no existe una declaracion jurada para la sede"""
    ddjj = Ddjj.query.filter_by(id_sede=id).first()
    if ddjj is not None:
        return False
    else:
        return True

def agregar_ddjj(data):
    """Esta funcion da de alta de una declaracion jurada"""
    ddjj = Ddjj(**data)
    db.session.add(ddjj)
    db.session.commit()
    return ddjj