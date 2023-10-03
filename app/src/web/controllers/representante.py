from flask import Blueprint, render_template, request, flash, redirect, make_response, jsonify, abort
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity

from src.core import usuarios
from src.core import provincias
from src.core import roles
from src.core import solicitudes
from src.core import entidades
from src.core import sedes
from src.web.controllers.validators import validator_usuario, validator_permission

representante = Blueprint("representante", __name__, url_prefix="/representante")

@representante.get("/entidades")
@jwt_required()
def listado_entidades_existentes():
    usuario_actual = get_jwt_identity()
    if not (validator_permission.has_permission(usuario_actual, "representante_solicitar_administracion")):
        return abort(403)
    lista_entidades = entidades.get_entidades()
    kwargs = {
        "lista_entidades": lista_entidades
    }
    return render_template("representante/listado_entidades_existentes.html", **kwargs)