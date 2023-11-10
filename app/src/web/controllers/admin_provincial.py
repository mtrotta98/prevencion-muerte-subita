from flask import Blueprint, render_template, request, flash, redirect, make_response, jsonify, abort
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity

from src.core import usuarios
from src.core import sedes
from src.core import provincias
from src.core import roles
from src.core import solicitudes
from src.core import entidades
from src.web.controllers.validators import validator_usuario, validator_permission

admin_provincial = Blueprint("admin_provincial", __name__, url_prefix="/admin_provincial")


@admin_provincial.get("/solicitudes")
@jwt_required()
def listado_solicitudes():
    usuario_actual = get_jwt_identity()
    if not (validator_permission.has_permission(usuario_actual, "administrador_provincial_autorizaciones")):
        return abort(403)
    info_solicitudes = []
    usuario = usuarios.get_usuario(usuario_actual)
    rol = roles.get_rol(usuario.id_rol)
    tipo = request.args.get("tipo") if request.args.get("tipo", type=str) != "" else None
    solis = solicitudes.solicitudes(tipo)
    for soli in solis:
        data_usuario = usuarios.get_usuario(soli.id_usuario)
        data_sede = sedes.get_sede(soli.id_sede)
        provincia = provincias.get_provincia(data_sede.id_provincia)
        if provincia in usuario.provincias:
            dict_usuario = {"Nombre": data_usuario.nombre, "Apellido": data_usuario.apellido, "Estado": soli.estado, "Razon": soli.razon, "id_solicitud": soli.id, "sede": data_sede.nombre}
            info_solicitudes.append(dict_usuario)
    kwargs = {
        "nombre": usuario.nombre,
        "apellido": usuario.apellido,
        "rol": rol.nombre,
        "solicitudes": info_solicitudes,
    }
    return render_template("admin_provincial/evaluar_solicitudes.html", **kwargs)

@admin_provincial.route("/info_solicitud/<id>")
@jwt_required()
def info_solicitud(id):
    usuario_actual = get_jwt_identity()
    if not (validator_permission.has_permission(usuario_actual, "administrador_provincial_autorizaciones")):
        return abort(403)
    usuario = usuarios.get_usuario(usuario_actual)
    rol = roles.get_rol(usuario.id_rol)
    solicitud = solicitudes.get_solicitud(id)
    id_admin = solicitud.id_usuario
    id_sede = solicitud.id_sede
    data_admin = usuarios.get_usuario(id_admin)
    data_sede = sedes.get_sede(id_sede)
    data_entidad = entidades.get_entidad(data_sede.id_entidad)
    kwargs = {
        "nombre": usuario.nombre,
        "apellido": usuario.apellido,
        "nombre_admin": data_admin.nombre + " " + data_admin.apellido,
        "id_solicitud": id,
        "nombre_sede":data_sede.nombre,
        "rs_entidad": data_entidad.razon_social,
        "cuit_entidad": data_entidad.cuit,
        "rol": rol.nombre
    }
    return render_template("admin_provincial/info_solicitud.html", **kwargs)

@admin_provincial.post("/aceptar_solicitud")
@jwt_required()
def evaluacion_solicitud():
    usuario_actual = get_jwt_identity()
    if not (validator_permission.has_permission(usuario_actual, "administrador_provincial_autorizaciones")):
        return abort(403)
    id_soli = request.form.get("id")
    estado = request.form.get("estado")
    data_solicitud = {
        "id": id_soli,
        "estado": estado,
        "razon": request.form.get("observacion"),
    }
    
    solicitudes.actualizar_solicitud(data_solicitud)

    solicitud = solicitudes.get_solicitud(id_soli)
    if estado == "Aprobada":
        id_admin = solicitud.id_usuario
        id_sede = solicitud.id_sede
        sedes.relacionar_representante_sede(id_admin, id_sede)

    return redirect("/admin_provincial/solicitudes")
