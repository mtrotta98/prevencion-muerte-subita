import json

from src.core import entidades, usuarios
from flask import Blueprint, render_template, request, flash, redirect, session, abort
from src.web.controllers.validators.validator_permission import has_permission
from src.web.controllers.validators import validator_entidad_sede
from flask_jwt_extended import jwt_required, unset_jwt_cookies
from flask_jwt_extended import create_access_token, set_access_cookies, get_jwt_identity

entidad_blueprint = Blueprint("entidades", __name__, url_prefix="/entidades")

@entidad_blueprint.route("/registro")
@jwt_required()
def form_entidad():
    usuario_actual = get_jwt_identity()
    usuario = usuarios.get_usuario(usuario_actual)
    if not (has_permission(usuario_actual, "representante_alta_entidad")):
        return abort(403)
    
    kwargs = {
        "nombre": usuario.nombre,
        "apellido": usuario.apellido,
    }

    return render_template("entidades/registro_entidad.html", **kwargs)


@entidad_blueprint.route("/alta", methods=["POST"])
@jwt_required()
def agregar_entidad():
    """Esta funcion se encarga de llamar al metodo correspondiente para dar de alta una entidad"""

    usuario_actual = get_jwt_identity()
    usuario = usuarios.get_usuario(usuario_actual)
    if not (has_permission(usuario_actual, "representante_alta_entidad")):
        return abort(403)
    
    data_entidad = {
        "cuit": request.form.get("cuit"),
        "razon_social": request.form.get("razon_social").capitalize(),
        "tipo_institucion": request.form.get("tipo_institucion").capitalize(),
        "sector": request.form.get("sector").capitalize()
    }

    data_existente, mensaje = entidades.validar_datos_existentes(data_entidad["cuit"], data_entidad["razon_social"])
    inputs_validados, mensaje2 = validator_entidad_sede.validar_inputs_entidad(**data_entidad)

    if data_existente and inputs_validados:
        entidad = entidades.agregar_entidad(data_entidad)
        mensaje_exito = "La entidad se ha cargado con exito."
        flash(mensaje_exito)
        return redirect("/entidades/registro")
    else:
        flash(mensaje) if mensaje != "" else flash(mensaje2)
        return redirect("/entidades/registro")