import json

from src.core import sedes
from src.core import provincias
from flask import Blueprint, render_template, request, flash, redirect, session, abort
from src.web.controllers.validators import validator_entidad_sede

sede_blueprint = Blueprint("sedes", __name__, url_prefix="/sedes")

@sede_blueprint.route("/registro")
def form_sede():
    kwargs = {
        "provincias" : provincias.get_provincias()
    }
    return render_template("sedes/registro_sede.html", **kwargs)

@sede_blueprint.route("/alta", methods=["POST"])
def agregar_sede():
    """Esta funcion se encarga de llamar al metodo correspondiente para dar de alta una sede"""

    data_sede = {
        "nombre": request.form.get("nombre"),
        "flujo_personas": request.form.get("flujo_personas"),
        "latitud": request.form.get("latitud"),
        "longitud": request.form.get("longitud"),
        "superficie": request.form.get("superficie"),
        "personal_estable": request.form.get("personal_estable"),
        "pisos": request.form.get("cantidad_pisos"),
        "estado": "En proceso de ser cardioasistido",
    }

    data_existente, mensaje = sedes.validar_datos_existentes(data_sede["nombre"])
    inputs_validos, mensaje2 = validator_entidad_sede.validar_inputs_sede(**data_sede)

    if data_existente and inputs_validos:
        sede = sedes.agregar_sede(data_sede)
        mensaje_exito =  "La sede se ha cargado con exito."
        flash(mensaje_exito)
        return redirect("/sedes/registro")
    else:
        flash(mensaje) if mensaje != "" else flash(mensaje2)
        return redirect("/sedes/registro")