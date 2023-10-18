

def validator(personal_capacitado, dea_señalizado, responsable, protocolo_accion, sistema_emergencia, cantidad_dea):
    if not personal_capacitado:
        return False
    if not responsable:
        return False
    if not dea_señalizado:
        return False
    if not sistema_emergencia:
        return False
    if not cantidad_dea:
        return False
    if not protocolo_accion:
        return False
    else:
        return True