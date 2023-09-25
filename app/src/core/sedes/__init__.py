from src.core.sedes.sedes import Sede


def get_sedes():
    """Esta funcion devuelve todas las sedes"""
    return Sede.query.all()

def get_sede(id):
    """Devuelve una sede buscada por su id"""
    return Sede.query.filter_by(id=id).first()