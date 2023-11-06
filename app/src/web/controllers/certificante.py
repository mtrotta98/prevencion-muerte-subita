from flask import Blueprint, render_template, request, flash, redirect, make_response, jsonify, abort, url_for
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity

from src.core import usuarios
from src.core import sedes
from src.core import visitas
from src.web.controllers.validators import validator_usuario, validator_permission

certificante_blueprint = Blueprint("certificante", __name__, url_prefix="/certificante")

@certificante_blueprint.get("/visitas")
@jwt_required()
def listado_visitas():

    usuario_actual = get_jwt_identity()
    usuario = usuarios.get_usuario(usuario_actual)
    if not (validator_permission.has_permission(usuario_actual, "usuario_certificante_listado_visitas")):
        return abort(403)
    
    listado_visitas = []
    provincias_usuario = usuario.provincias
    for provincia in provincias_usuario:
        sedes_provincias = sedes.get_sedes_provincia(provincia.id)
        for sede in sedes_provincias:
            visita_sede = visitas.get_visita_sede(sede.id)
            if visita_sede:
                listado_visitas.append(visita_sede)
    kwargs = {
        "visitas": listado_visitas,
        "nombre": usuario.nombre,
        "apellido": usuario.apellido
    }
    return render_template("certificante/listado_visitas.html", **kwargs)