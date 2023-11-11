from flask import Blueprint, render_template, request, flash, redirect, make_response, jsonify, abort, url_for
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity

from src.core import usuarios
from src.core import sedes
from src.core import visitas
from src.core import provincias
from src.core import roles
from src.web.controllers.validators import validator_usuario, validator_permission

certificante_blueprint = Blueprint("certificante", __name__, url_prefix="/certificante")

@certificante_blueprint.get("/visitas")
@jwt_required()
def listado_visitas():

    usuario_actual = get_jwt_identity()
    usuario = usuarios.get_usuario(usuario_actual)
    if not (validator_permission.has_permission(usuario_actual, "usuario_certificante_listado_visitas")):
        return abort(403)
    rol = roles.get_rol(usuario.id_rol)
    listado_visitas = []
    provincias_usuario = usuario.provincias
    sedes_provincias = []
    direcciones = []
    provincia = request.args.get("provincia") if request.args.get("provincia", type=str) != "" else None
    if provincia is None:
        id_provincia = provincias_usuario[0].id
    else:
        id_provincia = provincia
    if id_provincia != None:
        sedes_provincias = sedes.get_sedes_provincia(id_provincia)
        direcciones = sedes.get_direcciones(sedes_provincias)
        for sede in sedes_provincias:
            visita_sede = visitas.get_visita_sede(sede.id)
            if visita_sede and visita_sede[0].resultado is None:
                listado_visitas.append(visita_sede)
    kwargs = {
        "visitas": listado_visitas,
        "provincias": provincias_usuario,
        "info_sedes": sedes_provincias,
        "direcciones": direcciones,
        "nombre": usuario.nombre,
        "apellido": usuario.apellido,
        "rol": rol.nombre
    }
    return render_template("certificante/listado_visitas.html", **kwargs)