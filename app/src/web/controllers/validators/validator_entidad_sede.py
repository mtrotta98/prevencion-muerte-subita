import re

def validar_inputs_entidad(cuit, razon_social, tipo_institucion, sector):
    """Esta funcion valida que los inputs de la entidad sean del tipo correcto."""

    regex_campo = "^[a-zA-ZáéíóúÁÉÍÓÚüÜñÑ0-9 ]+$"
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
    

def validar_inputs_sede(nombre, flujo_personas, latitud, longitud, superficie, personal_estable, pisos, estado, id_provincia, id_entidad):
    """Esta funcion valida quqe los inputs de la sede sean del tipo correcto"""

    regex_campo = "^[a-zA-ZáéíóúÁÉÍÓÚüÜñÑ0-9 ]+$"
    if not (nombre != "" and flujo_personas != "" and latitud != "" and longitud != "" and superficie != "" and personal_estable != "" and pisos != "" and id_provincia != "" and id_entidad != ""):
        return False, "Todos los datos deben estar completos"
    elif not (re.search(regex_campo, nombre)):
        return False, "El nombre debe ser valido"
    elif not (flujo_personas.isnumeric()):
        return False, "El flujo de personas debe ser un numero entero"
    elif not (latitud.strip("-").replace(".","").isnumeric()):
        return False, "La latitud debe ser un numero"
    elif not (longitud.strip("-").replace(".","").isnumeric()):
        return False, "La longitud debe ser un numero"
    elif not (superficie.isnumeric()):
        return False, "La superficie debe ser un numero"
    elif not (personal_estable.isnumeric()):
        return False, "La cantidad de personal estaba debe ser un numero entero"
    elif not (pisos.isnumeric()):
        return False, "La cantidad de pisos debe ser un numero entero"
    elif not (estado):
        return False, "El estado debe ser valido"
    elif not (id_provincia.isnumeric()):
        return False, "El id de la provincia no es numero"
    elif not (id_entidad.isnumeric()):
        return False, "El id de la entidad no es numerico"
    else:
        return True, ""


def validar_inputs_editar_sede(id_sede, nombre, flujo_personas, latitud, longitud, superficie, personal_estable, pisos, cantidad_DEA):
    """Esta funcion valida que los datos de la edicion de una sede sean validos"""

    regex_campo = "^[a-zA-ZáéíóúÁÉÍÓÚüÜñÑ0-9 ]+$"
    if not (id_sede != "" and nombre != "" and flujo_personas != "" and latitud != "" and longitud != "" and superficie != "" and personal_estable != "" and pisos != "" and cantidad_DEA != ""):
        return False, "Todos los datos deben estar completos"
    elif not (re.search(regex_campo, nombre)):
        return False, "El nombre debe ser valido"
    elif not (flujo_personas.isnumeric()):
        return False, "El flujo de personas debe ser un numero entero"
    elif not (latitud.strip("-").replace(".","").isnumeric()):
        return False, "La latitud debe ser un numero"
    elif not (longitud.strip("-").replace(".","").isnumeric()):
        return False, "La longitud debe ser un numero"
    elif not (superficie.replace(".","").isnumeric()):
        return False, "La superficie debe ser un numero"
    elif not (personal_estable.isnumeric()):
        return False, "La cantidad de personal estaba debe ser un numero entero"
    elif not (pisos.isnumeric()):
        return False, "La cantidad de pisos debe ser un numero entero"
    elif not (cantidad_DEA.isnumeric()):
        return False, "La cantidad de DEA debe ser un numero entero"
    else:
        return True, ""