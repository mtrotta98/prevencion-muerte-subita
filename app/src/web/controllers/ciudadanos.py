from math import sin, cos, sqrt, atan2, radians
from flask import Flask, render_template, request, Blueprint
from src.core import sedes

ciudadano_blueprint = Blueprint("ciudadanos", __name__, url_prefix="/ciudadanos")

@ciudadano_blueprint.route("/inicio-ciudadano")
def inicio_ciudadano():
    return render_template("/ciudadano/index.html")

@ciudadano_blueprint.route('/enviar_notificacion', methods=["POST"])
def enviar_notificacion():
    lat_ciudadano = float(request.form["lat"])
    lon_ciudadano = float(request.form["lon"])
    lista_sedes_cercanas = []
    R = 6373.0

    sedes_posibles = sedes.get_sedes(None)

    for sede in sedes_posibles:
        lat_ciudadano_rad = radians(lat_ciudadano)
        lon_ciudadano_rad = radians(lon_ciudadano)

        lat_sede_rad = radians(sede.latitud)
        lon_sede_rad = radians(sede.longitud)

        distancia_lat_sede = lat_sede_rad - lat_ciudadano_rad
        distancia_lon_sede = lon_sede_rad - lon_ciudadano_rad

        val1 = sin(distancia_lat_sede / 2)**2 + cos(lat_ciudadano_rad) * cos(lat_sede_rad) * sin(distancia_lon_sede / 2)**2
        val2 = 2 * atan2(sqrt(val1), sqrt(1 - val1))

        distancia_real = R * val2

        lista_sedes_cercanas.append({
            "id_sede": sede.id,
            "distancia": distancia_real
        })

    lista_ordenada = sorted(lista_sedes_cercanas, key=lambda i: (i["distancia"]))


    return ""