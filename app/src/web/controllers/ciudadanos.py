import pandas as pd
import numpy as np
from geopy.geocoders import Nominatim
from flask import Flask, render_template, request, Blueprint
from src.core import sedes, usuarios
from src.web.helpers.send_emails import enviar_mail_alerta_asistencia


ciudadano_blueprint = Blueprint("ciudadanos", __name__, url_prefix="/ciudadanos")

@ciudadano_blueprint.route("/inicio-ciudadano")
def inicio_ciudadano():
    return render_template("/ciudadano/index.html")

@ciudadano_blueprint.route('/enviar_notificacion', methods=["POST"])
def enviar_notificacion():
    lat_ciudadano = float(request.form["lat"])
    lon_ciudadano = float(request.form["lon"])
    lista_sedes_cercanas = []
    R = 6371
    geoLoc = Nominatim(user_agent="GetLoc")

    sedes_posibles = sedes.get_sedes(None)

    for sede in sedes_posibles:
        lat_ciudadano_rad = np.radians(lat_ciudadano)
        lon_ciudadano_rad = np.radians(lon_ciudadano)

        lat_sede_rad = np.radians(float(sede.latitud))
        lon_sede_rad = np.radians(float(sede.longitud))

        distancia_lat = np.subtract(lat_ciudadano_rad, lat_sede_rad)
        distancia_lon = np.subtract(lon_ciudadano_rad, lon_sede_rad)

        a = np.add(np.power(np.sin(np.divide(distancia_lat, 2)), 2),
                   np.multiply(np.cos(lat_sede_rad),
                               np.multiply(np.cos(lat_ciudadano_rad),
                                           np.power(np.sin(np.divide(distancia_lon, 2)), 2))))
        
        c = np.multiply(2, np.arcsin(np.sqrt(a)))

        distancia_real = c*R

        lista_sedes_cercanas.append({
            "id_sede": sede.id,
            "distancia": distancia_real
        })

    lista_ordenada = sorted(lista_sedes_cercanas, key=lambda i: (i["distancia"]))

    sede_notificar = sedes.get_sede(lista_ordenada[0]["id_sede"])
    representantes = usuarios.get_usuarios_representantes()

    for representante in representantes:
        for sede in representante.sedes:
            if sede.id == sede_notificar.id:
                coords = str(lat_ciudadano) + ", " + str(lon_ciudadano)
                direccion = str(geoLoc.reverse(coords))
                lista = direccion.split(", ")
                direccion_asistencia = lista[1] + ", " + lista[0] + ", " + lista[2]
                enviar_mail_alerta_asistencia(representante.email, representante.nombre, representante.apellido, direccion_asistencia)

    return ""