from flask import Flask, render_template, request, Blueprint
from src.core import sedes

ciudadano_blueprint = Blueprint("ciudadanos", __name__, url_prefix="/ciudadanos")

@ciudadano_blueprint.route("/inicio-ciudadano")
def inicio_ciudadano():
    return render_template("/ciudadano/index.html")

@ciudadano_blueprint.route('/enviar_notificacion', methods=["POST"])
def enviar_notificacion():
    lat = request.form["lat"]
    lon = request.form["lon"]

    return ""