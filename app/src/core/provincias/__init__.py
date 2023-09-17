from src.core.provincias.provincias import Provincia

def get_provincias():
    """Esta funcion devuelve todas las provincias"""
    return Provincia.query.all()

def get_provincia(id):
    return Provincia.query.filter_by(id=id).first()