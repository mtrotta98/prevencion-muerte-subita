import re


def validar_inputs(nombre, apellido, usuario, contraseña, contraseña2, dni, id_rol):
    """Esta funcion valida que los inputs sean del tipo correcto."""
    regex_nombre_apellido = "^[a-zA-ZáéíóúÁÉÍÓÚüÜñÑ]+$"
    if not (nombre != "" and contraseña != "" and apellido != "" and dni != "" and usuario != ""):
        return False, "Todos los datos deben estar completos"
    elif not (re.search(regex_nombre_apellido, nombre)):
        return False, "El nombre debe ser valido"
    elif not (re.search(regex_nombre_apellido, apellido)):
        return False, "El apellido debe ser valido"
    elif not (len(dni) == 8):
        return False, "El dni deben ser solo 8 digitos"
    elif not (dni.isnumeric()):
        return False, "El dni deben ser numeros"
    elif not (id_rol):
        return False, "El rol debe ser valido"
    elif not contraseña == contraseña2:
        return False, "Las contraseñas deben coincidir"
    elif not (len(contraseña) >= 6 and len(contraseña) <= 10):
        return False, "La contraseña debe contener entre 6 y 10 caracteres."
    else:
        return True, ""
    
def validar_inputs_login(usuario, contraseña):
    """Esta funcion valida los inputs del login"""
    if not (contraseña != "" and usuario != ""):
        return False, "Todos los datos deben estar completos"
    elif not (len(contraseña) >= 6 and len(contraseña) <= 10):
        return False, "La contraseña debe contener entre 6 y 10 caracteres."
    else:
        return True, ""