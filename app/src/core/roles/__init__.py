from src.core.roles.roles import Rol

def get_roles():
    return Rol.query.all()

def get_rol(id):
    """Esta funcion devuelve un rol por su id"""
    return Rol.query.filter_by(id=id).first()