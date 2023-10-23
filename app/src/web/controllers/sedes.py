import json

from src.core import sedes
from src.core import provincias
from flask import Blueprint, render_template, request, flash, redirect, session, abort
from src.web.controllers.validators import validator_entidad_sede
from flask_jwt_extended import jwt_required, unset_jwt_cookies
from flask_jwt_extended import create_access_token, set_access_cookies, get_jwt_identity

sede_blueprint = Blueprint("sedes", __name__, url_prefix="/sedes")

@sede_blueprint.route("/registro/<id_entidad>")
@jwt_required()
def form_sede(id_entidad):
    kwargs = {
        "provincias" : provincias.get_provincias(),
        "id_entidad": id_entidad
    }
    return render_template("sedes/registro_sede.html", **kwargs)

@sede_blueprint.route("/alta/<id_entidad>", methods=["POST"])
@jwt_required()
def agregar_sede(id_entidad):
    """Esta funcion se encarga de llamar al metodo correspondiente para dar de alta una sede"""

    data_provincias = request.form.getlist("prov")
    if data_provincias:
            for provincia in data_provincias:
                id_provincia = provincia

    data_sede = {
        "nombre": request.form.get("nombre"),
        "flujo_personas": request.form.get("flujo_personas"),
        "latitud": request.form.get("latitud"),
        "longitud": request.form.get("longitud"),
        "superficie": request.form.get("superficie"),
        "personal_estable": request.form.get("personal_estable"),
        "pisos": request.form.get("cantidad_pisos"),
        "estado": "En proceso de ser cardioasistido",
        "id_provincia": id_provincia,
        "id_entidad": id_entidad
    }

    data_existente, mensaje = sedes.validar_datos_existentes(data_sede["nombre"])
    inputs_validos, mensaje2 = validator_entidad_sede.validar_inputs_sede(**data_sede)

    if data_existente and inputs_validos:
        sede = sedes.agregar_sede(data_sede)
        mensaje_exito =  "La sede se ha cargado con exito."
        flash(mensaje_exito)
        return redirect("/sedes/registro/<id_entidad>")
    else:
        flash(mensaje) if mensaje != "" else flash(mensaje2)
        return redirect("/sedes/registro/<id_entidad>")