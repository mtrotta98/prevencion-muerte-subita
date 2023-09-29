from flask import Blueprint, render_template, request, flash, redirect, make_response, jsonify, abort
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity

from src.core import usuarios
from src.core import ddjj
from src.core import visitas
from src.web.controllers.validators import validator_ddjj, validator_permission

representante_blueprint = Blueprint("representante", __name__, url_prefix="/representante")

@representante_blueprint.route("/ddjj")
@jwt_required()
def form_ddjj():
    usuario_actual = get_jwt_identity()
    if not (validator_permission.has_permission(usuario_actual, "representante_ddjj")):
        return abort(403)
    usuario = usuarios.get_usuario(usuario_actual)
    kwargs = {
        "nombre": usuario.nombre,
        "apellido": usuario.apellido,
    }
    return render_template("representante/form_ddjj.html", **kwargs)

@representante_blueprint.post("/carga_ddjj")
@jwt_required()
def carga_ddjj():
    usuario_actual = get_jwt_identity()
    if not (validator_permission.has_permission(usuario_actual, "representante_ddjj")):
        return abort(403)
    data_ddjj = {
        "personal_capacitado": True if request.form.get("per_cap") == "si" else False,
        "dea_señalizado": True if request.form.get("dea_señalizado") == "si" else False,
        "responsable": True if request.form.get("responsable") == "si" else False,
        "protocolo_accion": True if request.form.get("prot_acc") == "si" else False,
        "sistema_emergencia": True if request.form.get("sist_emer") == "si" else False,
        "cantidad_dea": True if request.form.get("deas_necesarios") == "si" else False,
    }

    if not validator_ddjj.validator(**data_ddjj):
        flash("Todos los datos deben estar marcados con SI para cargar la declaracion jurada")
        return redirect("/representante/ddjj")
    
    declaracion = ddjj.agregar_ddjj(data_ddjj)
    visita = visitas.agregar_visita()
    return redirect("/usuarios/inicio")