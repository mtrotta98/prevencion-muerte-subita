import json

from src.core import sedes
from src.core import provincias
from flask import Blueprint, render_template, request, flash, redirect, session, abort, url_for
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity
from src.web.controllers.validators import validator_entidad_sede

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
    

@sede_blueprint.route("/form_editar/<id_sede>")
@jwt_required()
def form_editar_sede(id_sede):
     """Esta funcion trae la informacion de la sede a editar"""
     
     sede = sedes.get_sede(id_sede)
     provincia = provincias.get_provincia(sede.id_provincia)
     kwgars = {
         "sede": sede,
         "provincia": provincia 
     }
     return render_template("sedes/editar_sede.html", **kwgars)

@sede_blueprint.route("/editar/<id_sede>", methods=["POST"])
@jwt_required()
def editar_sede(id_sede):
    
    id = id_sede
    data_sede = {
        "id_sede": id,
        "nombre": request.form.get("nombre"),
        "flujo_personas": request.form.get("flujo_personas"),
        "latitud": request.form.get("latitud"),
        "longitud": request.form.get("longitud"),
        "superficie": request.form.get("superficie"),
        "personal_estable": request.form.get("personal_estable"),
        "pisos": request.form.get("cantidad_pisos"),
    }

    data_existente, mensaje = sedes.validar_nombre_existente(data_sede["nombre"])
    inputs_validos, mensaje2 = validator_entidad_sede.validar_inputs_editar_sede(**data_sede)

    if data_existente and inputs_validos:
        sede = sedes.editar_sede(data_sede)
        mensaje_exito =  "La sede se ha editado con exito."
        flash(mensaje_exito)
        return redirect(url_for("sedes.form_editar_sede", id_sede=id_sede))
    else:
        flash(mensaje) if mensaje != "" else flash(mensaje2)
        return redirect(url_for("sedes.form_editar_sede", id_sede=id_sede))