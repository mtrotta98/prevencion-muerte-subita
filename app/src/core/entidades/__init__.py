from src.core.entidades.entidades import Entidad

def get_entidades():
    """Esta funcion devuelve todas las entidades"""
    return Entidad.query.all()

def get_entidad(id):
    return Entidad.query.filter_by(id=id).first()