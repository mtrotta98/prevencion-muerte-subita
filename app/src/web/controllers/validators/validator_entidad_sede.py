import re

def validar_inputs_entidad_sede(cuit, razon_social, tipo_institucion, sector):
    """Esta funcion valida que los inputs sean del tipo correcto."""

    regex_campo = "^[a-zA-ZáéíóúÁÉÍÓÚüÜñÑ]+$"
    if not (cuit != "" and razon_social != "" and tipo_institucion != "" and sector != ""):
        return False, "Todos los datos deben estar completos"
    elif not (re.search(regex_campo, razon_social)):
        return False, "La razon social debe ser valida"
    elif not (re.search(regex_campo, tipo_institucion)):
        return False, "El tipo de institucion debe ser valido"
    elif not (len(cuit) == 11):
        return False, "El cuit deben ser solo 11 digitos"
    elif not (cuit.isnumeric()):
        return False, "El cuit deben ser numeros"
    else:
        return True, ""