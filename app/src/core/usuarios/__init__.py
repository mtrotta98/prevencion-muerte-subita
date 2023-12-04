from werkzeug.security import check_password_hash, generate_password_hash
from src.core.usuarios.usuarios import Usuario
from src.core.db import db

def get_usuarios_admin_provincial():
    """Esta funcion devuelve todos los usuarios administradores provinciales"""
    return Usuario.query.filter_by(id_rol=1).all()

def get_usuarios_representantes():
    """Esta funcion devuelve todos los usuarios representantes"""
    return Usuario.query.filter_by(id_rol=2).all()

def get_usuarios_certificantes():
    """ Esta funcion devuelve los usuarios certificantes """
    return Usuario.query.filter_by(id_rol=3).all()

def get_usuario(id):
    """Esta funcion devuelve un usuario por su id"""
    return Usuario.query.filter_by(id=id).first()

def agregar_usuario(data):
    """Esta funcion da de alta un usuario"""
    usuario = Usuario(**data)
    usuario.contraseña = generate_password_hash(usuario.contraseña, method="sha256")
    db.session.add(usuario)
    db.session.commit()
    return usuario

def validar_datos_existentes(usuario, dni, email):
    """Esta funcion valida que los datos de alta de usuario no existan en la base"""
    username_existente = Usuario.query.filter_by(usuario=usuario).first()
    dni_existente = Usuario.query.filter_by(dni=dni).first()
    email_existente = Usuario.query.filter_by(email=email).first()
    if username_existente is not None:
        return False, "El usuario ya esta cargado en el sistema."
    elif dni_existente is not None:
        return False, "El dni ya esta cargado en el sistema."
    elif email_existente is not None:
        return False, "El email ya esta cargado en el sistema."
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