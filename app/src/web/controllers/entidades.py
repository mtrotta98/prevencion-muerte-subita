import json

from src.core import entidades
from flask import Blueprint, render_template, request, flash, redirect, session, abort
from src.web.controllers.validators import validator_entidad_sede

entidad_blueprint = Blueprint("entidades", __name__, url_prefix="/entidades")

@entidad_blueprint.route("/registro")
def form_entidad():
    kwargs = {
        "entidades": entidades.get_entidades()
    }
    return render_template("entidades/registro_entidad.html", **kwargs)


@entidad_blueprint.route("/alta", methods=["POST"])
def agregar_entidad():
    """Esta funcion se encarga de llamar al metodo correspondiente para dar de alta una entidad"""
    
    data_entidad = {
        "cuit": request.form.get("cuit"),
        "razon_social": request.form.get("razon_social").capitalize(),
        "tipo_institucion": request.form.get("tipo_institucion").capitalize(),
        "sector": request.form.get("sector").capitalize()
    }

    data_existente, mensaje = entidades.validar_datos_existentes(data_entidad["cuit"], data_entidad["razon_social"])
    inputs_validados, mensaje2 = validator_entidad_sede.validar_inputs_entidad_sede(**data_entidad)

    if data_existente and inputs_validados:
        entidad = entidades.agregar_entidad(data_entidad)
        
        return 'Hello, World!'
    else:
        flash(mensaje) if mensaje != "" else flash(mensaje2)
        return redirect("/entidades/registro")