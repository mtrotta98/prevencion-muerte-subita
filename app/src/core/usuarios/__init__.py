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

def validar_datos_existentes(usuario, dni):
    """Esta funcion valida que los datos de alta de usuario no existan en la base"""
    username_existente = Usuario.query.filter_by(usuario=usuario).first()
    dni_existente = Usuario.query.filter_by(dni=dni).first()
    if username_existente is not None:
        return False, "El usuario ya esta cargado en el sistema."
    elif dni_existente is not None:
        return False, "El dni ya esta cargado en el sistema."
    else:
        return True, ""

def agregar_provincia(usuario, provincia):
    """Esta funcion relaciona a un usuario con una provincia"""
    usuario.provincias.append(provincia)
    db.session.commit()

def verificar_usuario(usuario, contraseña):
    """Esta funcion verifica la existencia del usuario que intenta loguearse"""
    usuario = Usuario.query.filter(Usuario.usuario==usuario).first()
    if usuario is None:
        return None, "Datos incorrectos"
    else:
        if check_password_hash(usuario.contraseña, contraseña):
            return usuario, "Datos correctos"
        else:
            return None, "Datos incorrectos"