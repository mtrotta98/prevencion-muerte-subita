from src.core.roles.roles import Rol

def get_roles():
    return Rol.query.all()

def get_rol(nombre):
    return Rol.query.filter_by(nombre=nombre).first()