from flask import Blueprint, render_template, request, flash, redirect, make_response, jsonify, abort
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity

from src.core import entidades
from src.core import sedes
from src.core import usuarios
from src.web.controllers.validators import validator_usuario, validator_permission

representante = Blueprint("representante", __name__, url_prefix="/representante")

@representante.get("/entidades")
@jwt_required()
def listado_entidades_existentes():

    usuario_actual = get_jwt_identity()
    usuario = usuarios.get_usuario(usuario_actual)
    if not (validator_permission.has_permission(usuario_actual, "representante_solicitar_administracion")):
        return abort(403)
    busqueda = request.args.get("busqueda" if request.args.get("busqueda", type=str) != "" else None)
    lista_entidades = entidades.get_entidades(busqueda)
    kwargs = {
        "lista_entidades": lista_entidades,
        "nombre": usuario.nombre,
        "apellido": usuario.apellido
    }
    return render_template("representante/listado_entidades_existentes.html", **kwargs)


@representante.route("/sedes_asociadas/<id>")
@jwt_required()
def sedes_asociadas(id):
    """Esta funcion devuelve las sedes asociadas a una entidad pasada por parametro"""

    usuario_actual = get_jwt_identity()
    usuario = usuarios.get_usuario(usuario_actual)
    if not (validator_permission.has_permission(usuario_actual, "representante_solicitar_administracion")):
        return abort(403)
    busqueda = request.args.get("busquedaSede" if request.args.get("busquedaSede", type=str) != "" else None)
    id_entidad = int(id)
    sedes_asociadas = sedes.get_sedes_asociadas(id_entidad, busqueda)
    kwargs = {
        "sedes_asociadas": sedes_asociadas,
        "nombre": usuario.nombre,
        "apellido": usuario.apellido,
        "id_entidad": id_entidad
    }
    return render_template("/representante/listado_sedes_asociadas.html", **kwargs)

