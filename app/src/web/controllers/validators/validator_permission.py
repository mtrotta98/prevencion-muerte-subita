from src.core import usuarios, permisos, roles


def has_permission(id, permission):
    """Este metodo valida si el usuario posee o no el permiso enviado por parametro"""
    usuario = usuarios.get_usuario(id)
    id_rol = usuario.id_rol
    rol = roles.get_rol(id_rol)
    permiso = permisos.get_permiso(permission)
    if (permiso in rol.permisos):
        return True
    return False