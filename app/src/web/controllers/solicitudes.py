from flask import Blueprint, render_template, request, flash, redirect, make_response, jsonify, abort, url_for
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity

from src.core import solicitudes
from src.core import usuarios
from src.core import sedes
from src.core import provincias

solicitud_blueprint = Blueprint("solicitudes", __name__, url_prefix="/solicitudes")

@solicitud_blueprint.route("/registro/<id_entidad><id_sede>")
@jwt_required()
def registrar_solicitud(id_entidad, id_sede):
    """Esta funcion registra una solicitud de administrar sede, hecha por un representante"""

    usuario_actual = get_jwt_identity()
    usuario = usuarios.get_usuario(usuario_actual)
    solicitudes.registrar_solicitud(usuario.id, id_sede)

    nombre_sede = request.args.get("busquedaSede" if request.args.get("busquedaSede", type=str) != "" else None)
    id_entidad = int(id_entidad)
    sedes_asociadas = sedes.get_sedes_asociadas(id_entidad, nombre_sede)
    solicitudes_usuario = solicitudes.solicitudes_usuario(usuario)

    return redirect(url_for("representante.sedes_asociadas", id=id_entidad))