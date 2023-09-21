from src.core.permisos.permisos import Permiso
from src.core.db import db

def get_permisos():
    """Esta funcion devuelve todos los usuarios"""
    return Permiso.query.all()