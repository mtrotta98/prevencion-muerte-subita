from flask import Blueprint, render_template, request, flash, redirect, make_response, jsonify, abort, url_for
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity

from src.core import usuarios
from src.core import sedes
from src.core import visitas
from src.core import provincias
from src.web.controllers.validators import validator_usuario, validator_permission

visitas_blueprint = Blueprint("visitas", __name__, url_prefix="/visitas")

@visitas_blueprint.route("/formulario/<id_visita>")
@jwt_required()
def form_cargar_visita(id_visita):
    """Esta funcion carga una visita a una sede de un usuario certificante"""

    info_visita = visitas.get_visita_id(id_visita)

    kwargs = {
        "visita": info_visita
    }
    return render_template("visitas/form_cargar_visita.html", **kwargs)


@visitas_blueprint.route("/registro/<id_visita>", methods=["POST"])
@jwt_required()
def registrar_visita(id_visita):
    """Esta funcion registra una visita del usuario certificado sobre una sede"""

    resultado = request.form.get("resultado")
    if resultado == "true":
        data = {
            "id": id_visita,
            "resultado": True,
            "observacion": request.form.get("observacion")
        }
    elif resultado == "false":
        data = {
            "id": id_visita,
            "resultado": False,
            "observacion": request.form.get("observacion")
        }
    visita_actual = visitas.get_visita_id(id_visita)
    if resultado == "true":
        estado = sedes.sede_a_cardioasistida_certificada(visita_actual.id_sede)
    visita = visitas.agregar_visita(data)
    mensaje_exito =  "La visita se ha cargado con exito."
    flash(mensaje_exito, "success")
    return redirect(url_for("certificante.listado_visitas"))