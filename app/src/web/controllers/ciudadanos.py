import pandas as pd
import numpy as np
from geopy.geocoders import Nominatim
from flask import Flask, render_template, request, Blueprint
from src.core import sedes, responsables, deas
from src.web.helpers.send_emails import enviar_mail_alerta_asistencia


ciudadano_blueprint = Blueprint("ciudadanos", __name__, url_prefix="/ciudadanos")

LAT_ACTUAL = 0
LON_ACTUAL = 0

@ciudadano_blueprint.route("/inicio-ciudadano")
def inicio_ciudadano():
    return render_template("/ciudadano/index.html")

@ciudadano_blueprint.route('/enviar_notificacion', methods=["POST"])
def enviar_notificacion():
    global LAT_ACTUAL
    global LON_ACTUAL
    LAT_ACTUAL = float(request.form["lat"])
    LON_ACTUAL = float(request.form["lon"])
    lista_sedes_cercanas = []
    R = 6371
    geoLoc = Nominatim(user_agent="GetLoc")

    sedes_posibles = deas.get_sedes_solidarias()

    for sede in sedes_posibles:
        lat_ciudadano_rad = np.radians(LAT_ACTUAL)
        lon_ciudadano_rad = np.radians(LON_ACTUAL)

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

    sedes_notificar = []
    lista_coordenadas = []

    for i in range(3):
        sedes_notificar.append(sedes.get_sede(lista_ordenada[i]["id_sede"]))

    for sede in sedes_notificar:
        lista_coordenadas.append((sede.latitud, sede.longitud, sede.nombre, sede.cantidad_DEA, "si"))
    
    responsables_deas = responsables.get_responsables_aviso(sedes_notificar)

    for responsable in responsables_deas:
        coords = str(LAT_ACTUAL) + ", " + str(LON_ACTUAL)
        direccion = str(geoLoc.reverse(coords))
        lista = direccion.split(", ") 
        direccion_asistencia = lista[1] + ", " + lista[0] + ", " + lista[2]
        enviar_mail_alerta_asistencia(responsable.email, responsable.nombre, responsable.apellido, direccion_asistencia)

    return ""

@ciudadano_blueprint.route("/ver_mapa")
def ver_mapa():

    lista_coordenadas = []
    lista_sedes = sedes.get_sedes("")
    for sede in lista_sedes:
        solidario = "No"
        deas_sede = deas.get_by_sede(sede.id)
        if deas_sede:
            for dea in deas_sede:
                if dea.solidario:
                    solidario = "Si"
                    break
        lista_coordenadas.append((sede.latitud, sede.longitud, sede.nombre, sede.cantidad_DEA, solidario, "http://maps.google.com/mapfiles/ms/icons/red-dot.png"))

    kwgars = {
        "lista_coordenadas": lista_coordenadas
    }

    return render_template("/ciudadano/ver_mapa.html", **kwgars)

@ciudadano_blueprint.route("/mapa_alerta")
def mapa_alerta():
    global LAT_ACTUAL
    global LON_ACTUAL
    
    lista_coordenadas = []
    lista_sedes_cercanas = []
    R = 6371

    sedes_posibles = deas.get_sedes_solidarias()

    for sede in sedes_posibles:
        lat_ciudadano_rad = np.radians(LAT_ACTUAL)
        lon_ciudadano_rad = np.radians(LON_ACTUAL)

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

    sedes_notificar = []
    lista_coordenadas = []

    for i in range(3):
        sedes_notificar.append(sedes.get_sede(lista_ordenada[i]["id_sede"]))

    for sede in sedes_notificar:
        lista_coordenadas.append((sede.latitud, sede.longitud, sede.nombre, sede.cantidad_DEA, "si", "http://maps.google.com/mapfiles/ms/icons/blue-dot.png"))

    kwgars = {
        "lista_coordenadas": lista_coordenadas
    }

    return render_template("/ciudadano/ver_mapa.html", **kwgars)