from src.core.permisos.permisos import Permiso
from src.core.db import db

def get_permisos():
    """Esta funcion devuelve todos los permisos"""
    return Permiso.query.all()

def get_permiso(nombre):
    """Esta funcion devuelve un permiso por su nombre"""
    return Permiso.query.filter_by(nombre=nombre).first()