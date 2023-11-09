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

    sede_id = int(id_sede)
    usuario_actual = get_jwt_identity()
    usuario = usuarios.get_usuario(usuario_actual)
    solicitudes_usuario = solicitudes.solicitudes_usuario(usuario)
    print(solicitudes_usuario)
    ok = True
    if solicitudes_usuario:
        for solicitud in solicitudes_usuario:
            if solicitud.id_sede == sede_id:
                ok = False
                break
    
    if ok:
        solicitudes.registrar_solicitud(usuario.id, id_sede)
        mensaje_exito =  "La solicitud se cargo con exito."
        flash(mensaje_exito, "success")
        return redirect(url_for("representante.sedes_asociadas", id=id_entidad))
    else:
        mensaje_error = "Ya existe un solicitud creada por este usuario para la sede"
        flash(mensaje_error, "error")
        return redirect(url_for("representante.sedes_asociadas", id=id_entidad))

    