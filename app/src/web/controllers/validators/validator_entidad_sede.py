import re

def validar_inputs_entidad(cuit, razon_social, tipo_institucion, sector):
    """Esta funcion valida que los inputs de la entidad sean del tipo correcto."""

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
    

def validar_inputs_sede(nombre, flujo_personas, latitud, longitud, superficie, personal_estable, pisos, estado):
    """Esta funcion valida quqe los inputs de la sede sean del tipo correcto"""

    regex_campo = "^[a-zA-ZáéíóúÁÉÍÓÚüÜñÑ]+$"
    if not (nombre != "" and flujo_personas != "" and latitud != "" and longitud != "" and superficie != "" and personal_estable != "" and pisos != ""):
        return False, "Todos los datos deben estar completos"
    elif not (re.search(regex_campo, nombre)):
        return False, "El nombre debe ser valido"
    elif not (flujo_personas.isnumeric()):
        return False, "El flujo de personas debe ser un numero entero"
    elif not (latitud.isnumeric()):
        return False, "La latitud debe ser un numero"
    elif not (longitud.isnumeric()):
        return False, "La longitud debe ser un numero"
    elif not (superficie.isnumeric()):
        return False, "La superficie debe ser un numero"
    elif not (personal_estable.isnumeric()):
        return False, "La cantidad de personal estaba debe ser un numero entero"
    elif not (pisos.isnumeric()):
        return False, "La cantidad de pisos debe ser un numero entero"
    elif not (estado):
        return False, "El estado debe ser valido"
    else:
        return True, ""
