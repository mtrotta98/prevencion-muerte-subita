import uuid
import smtplib
import psycopg2
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
import json
from datetime import datetime

from flask import Blueprint, render_template, request, flash, redirect, make_response, jsonify, abort
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity

from src.core import sedes
from src.core import eventosms
from src.core import usuarios
from src.core import provincias
from src.core import roles
from src.core import sedes
from src.core import entidades
from src.core import solicitudes
from src.core import deas
from src.web.controllers.validators import validator_usuario, validator_permission
from src.web.helpers.send_emails import enviar_email_alta_admin_prov

super_usuario = Blueprint("super_usuario", __name__, url_prefix="/super_usuario")


@super_usuario.route("/form_alta")
@jwt_required()
def form_usuario():
    """Esta funcion devuelve el formulario para dar de alta un admin provincial"""
    usuario_actual = get_jwt_identity()
    if not (validator_permission.has_permission(usuario_actual, "super_usuario_alta_admins_prov")):
        return abort(403)
    usuario = usuarios.get_usuario(usuario_actual)
    rol = roles.get_rol(usuario.id_rol)
    kwargs = {
        "nombre": usuario.nombre,
        "apellido": usuario.apellido,
        "provincias": provincias.get_provincias(),
        "rol": rol.nombre,
    }
    return render_template("super_usuario/alta_admin_provincial.html", **kwargs)

@super_usuario.route("/alta_admin", methods=["POST"])
@jwt_required()
def alta_admin():
    """Esta funcion llama al metodo correspondiente para dar de alta un admin provincial."""
    usuario_actual = get_jwt_identity()
    if not (validator_permission.has_permission(usuario_actual, "super_usuario_alta_admins_prov")):
        return abort(403)
    nombre_rol = "Administrador Provincial"
    data_provincias = request.form.getlist("prov")
    rol = roles.get_rol_por_nombre(nombre_rol)

    data_usuario = {
        "nombre": request.form.get("nombre").capitalize(),
        "apellido": request.form.get("apellido").capitalize(),
        "usuario": request.form.get("usuario"),
        "contraseña": request.form.get("pass1"),
        "contraseña2": request.form.get("pass2"),
        "dni": request.form.get("dni"),
        "email": request.form.get("email"),
        "id_rol": rol.id
    }

    data_existente, mensaje = usuarios.validar_datos_existentes(data_usuario["usuario"], data_usuario["dni"], data_usuario["email"])
    inputs_validados, mensaje2 = validator_usuario.validar_inputs(**data_usuario)

    if data_existente and inputs_validados:
        data_usuario.pop("contraseña2")
        data_usuario["id_publico"] = str(uuid.uuid4())
        usuario = usuarios.agregar_usuario(data_usuario)
    
        if data_provincias:
            for provincia in data_provincias:
                prov = provincias.get_provincia(provincia)
                usuarios.agregar_provincia(usuario, prov)

        enviar_email_alta_admin_prov(data_usuario)

        return redirect("/usuarios/inicio")
    else:
        flash(mensaje) if mensaje != "" else flash(mensaje2)
        return redirect("/super_usuario/form_alta")

@super_usuario.route("/ETL_EMS")   
def ejecucion_etl_EMS():
    conexion = psycopg2.connect(host="localhost", database="warehouse", user="postgres", password="proyecto")
    cur = conexion.cursor()
    sexos={
        1: 'Masculino',
        2: 'Femenino',
        3: 'Otro'}

    # Recupero las marcas
    res = requests.get('https://api.claudioraverta.com/deas/')
    marcas = json.loads(res.text)

    sedesms = sedes.get_sedes("")
    for sedems in sedesms:
        eventos = eventosms.get_by_sede(sedems.id)
        emsprovincia = provincias.get_provincia(sedems.id_provincia).nombre
        emslocalidad = sedems.localidad # sedes.get_localidad(sedems)
        for evento in eventos:
            emsAño = evento.fecha.year
            emsMes = evento.fecha.month
            emssexo = sexos[evento.sexo]
            if evento.usodea:
                emsmarcadea = marcas[evento.marca-1]["marca"]   # Extraigo el string
                emsmodelo = evento.modelo
                usosdea = evento.usosdea
            else:
                emsmarcadea = "None"
                emsmodelo = "None"
                usosdea = 0
            if evento.usorcp:
                tiemporcp = evento.tiemporcp
            else:
                tiemporcp = 0
            query_ems = 'INSERT INTO public."Evento_muerte_subita" (fecha, año, mes, nombre_provincia, localidad, sexo_aparente, edad_aparente, uso_dea, cantidad_descargas, rcp, tiempo_rcp, modelo_dea, marca_dea, sobrevive) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'
            data_ems = (evento.fecha, emsAño, emsMes, emsprovincia, emslocalidad, emssexo, evento.edad, evento.usodea, usosdea, evento.usorcp, tiemporcp, emsmodelo, emsmarcadea, evento.sobrevive)
            cur.execute(query_ems, data_ems)
        conexion.commit()
    conexion.close()

@super_usuario.route("/ETL_representantes")
def ejecucion_etl_representantes():
    """ Esta funcion realiza la ejecucion del ETL para migrar los datos al datawarehouse """
    conexion = psycopg2.connect(host="localhost", database="warehouse", user="postgres", password="proyecto")
    cur = conexion.cursor()

    usuarios_representantes = usuarios.get_usuarios_representantes()

    for us_repre in usuarios_representantes:
        if len(us_repre.sedes) > 0:
            query_insert_user_prov = 'INSERT INTO public."Representantes" (nombre, apellido, fecha_nacimiento, año_nacimiento, mes_nacimiento, id_sede) VALUES (%s, %s, %s, %s, %s, %s);'
            data_insert_user_prov = (us_repre.nombre, us_repre.apellido, us_repre.fecha_nacimiento, us_repre.fecha_nacimiento.year, us_repre.fecha_nacimiento.month, us_repre.sedes[0].id)

            cur.execute(query_insert_user_prov, data_insert_user_prov)

    conexion.commit()

    conexion.close()

    return redirect("/usuarios/inicio")

@super_usuario.route("/ETL_certificantes")
def ejecucion_etl_certificantes():
    """ Esta funcion realiza la ejecucion del ETL para migrar los datos al datawarehouse """
    conexion = psycopg2.connect(host="localhost", database="warehouse", user="postgres", password="proyecto")
    cur = conexion.cursor()

    usuarios_certificantes = usuarios.get_usuarios_certificantes()

    for us_cert in usuarios_certificantes:
        query_insert_user_prov = 'INSERT INTO public."Certificantes" (nombre, apellido, fecha_nacimiento, nombre_provincia) VALUES (%s, %s, %s, %s);'
        data_insert_user_prov = (us_cert.nombre, us_cert.apellido, us_cert.fecha_nacimiento, us_cert.provincias[0].nombre)

        cur.execute(query_insert_user_prov, data_insert_user_prov)

    conexion.commit()

    conexion.close()

    return redirect("/usuarios/inicio")

@super_usuario.route("/ETL_sedes")
def ejecucion_etl_sedes():
    """ Esta funcion realiza la ejecucion del ETL para migrar los datos al datawarehouse """
    conexion = psycopg2.connect(host="localhost", database="warehouse", user="postgres", password="proyecto")
    cur = conexion.cursor()
    sedes_all = sedes.get_sedes("")

    for sede in sedes_all:
        print(sede.id)
        ok = "0"
        entidad = entidades.get_entidad(id=sede.id_entidad)
        nombre_prov = provincias.get_provincia(sede.id_provincia)
        cant_deas = deas.get_by_sede(sede.id)
        if len(cant_deas) > 0 and cant_deas[0].solidario:
            ok = "1"
        if entidad:
            query_insert_entidad_sede = 'INSERT INTO public."Entidad_Sede" (id, fecha_creacion, localidad, año_creacion, mes_creacion, nombre_provincia, id_entidad, estado, tipo_institucion, sector, cant_deas, deas_solidarios) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'
            data_insert_entidad_sede = (sede.id, sede.fecha_creacion, sede.localidad, sede.fecha_creacion.year, sede.fecha_creacion.month, nombre_prov.nombre, entidad.id, sede.estado, entidad.tipo_institucion, entidad.sector, len(cant_deas), ok)  # Asume que todos los DEA son solidarios

            cur.execute(query_insert_entidad_sede, data_insert_entidad_sede)

    conexion.commit()

    conexion.close()

    return redirect("/usuarios/inicio")