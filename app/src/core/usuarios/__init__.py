from werkzeug.security import check_password_hash, generate_password_hash
from src.core.usuarios.usuarios import Usuario
from src.core.db import db

def get_usuarios():
    """Esta funcion devuelve todos los usuarios"""
    return Usuario.query.all()

def agregar_usuario(data):
    """Esta funcion da de alta un usuario"""
    usuario = Usuario(**data)
    usuario.contraseña = generate_password_hash(usuario.contraseña, method="sha256")
    db.session.add(usuario)
    db.session.commit()
    return usuario

def agregar_provincia(usuario, provincia):
    """Esta funcion relaciona a un usuario con una provincia"""
    usuario.provincias.append(provincia)
    db.session.commit()