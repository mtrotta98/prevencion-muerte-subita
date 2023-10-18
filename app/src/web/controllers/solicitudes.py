from flask import Blueprint, render_template, request, flash, redirect, make_response, jsonify, abort
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity

from src.core import solicitudes
from src.core import usuarios

solicitud_blueprint = Blueprint("solicitudes", __name__, url_prefix="/solicitudes")

@solicitud_blueprint.route("/registro/<id_entidad>")
def registrar_solicitud(id_entidad):
    """Esta funcion registra una solicitud de administrar sede, hecha por un representante"""

    usuario_actual = get_jwt_identity()
    usuario = usuarios.get_usuario(usuario_actual)
    solicitudes.registrar_solicitud(usuario.id, "pendiente")
    kwargs = {
        "id_entidad": id_entidad
    }
    return render_template("/representante/listado_sedes_asociadas.html", **kwargs)