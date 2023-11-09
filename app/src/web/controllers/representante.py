from flask import Blueprint, render_template, request, flash, redirect, make_response, jsonify, abort, url_for
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity

from src.core import entidades
from src.core import sedes
from src.core import usuarios
from src.core import provincias
from src.core import solicitudes
from src.web.controllers.validators import validator_usuario, validator_permission, validator_ddjj
from src.core import ddjj
from src.core import visitas

representante = Blueprint("representante", __name__, url_prefix="/representante")

@representante.get("/entidades")
@jwt_required()
def listado_entidades_existentes():

    usuario_actual = get_jwt_identity()
    usuario = usuarios.get_usuario(usuario_actual)
    if not (validator_permission.has_permission(usuario_actual, "representante_solicitar_administracion")):
        return abort(403)
    busqueda = request.args.get("busqueda" if request.args.get("busqueda", type=str) != "" else None)
    lista_entidades = entidades.get_entidades(busqueda)
    kwargs = {
        "lista_entidades": lista_entidades,
        "nombre": usuario.nombre,
        "apellido": usuario.apellido
    }
    return render_template("representante/listado_entidades_existentes.html", **kwargs)


@representante.route("/sedes_asociadas/<id>")
@jwt_required()
def sedes_asociadas(id):
    """Esta funcion devuelve las sedes asociadas a una entidad pasada por parametro"""

    usuario_actual = get_jwt_identity()
    usuario = usuarios.get_usuario(usuario_actual)
    if not (validator_permission.has_permission(usuario_actual, "representante_solicitar_administracion")):
        return abort(403)
    
    nombre_sede = request.args.get("busquedaSede" if request.args.get("busquedaSede", type=str) != "" else None)
    id_entidad = int(id)
    sedes_asociadas = sedes.get_sedes_asociadas(id_entidad, nombre_sede)
    solicitudes_usuario = solicitudes.solicitudes_usuario(usuario)

    kwargs = {
        "sedes_asociadas": sedes_asociadas,
        "nombre": usuario.nombre,
        "apellido": usuario.apellido,
        "id_usuario": usuario.id,
        "id_entidad": id_entidad,
        "provincias": provincias.get_provincias(),
        "solicitudes_usuario": solicitudes_usuario
    }
    return render_template("/representante/listado_sedes_asociadas.html", **kwargs)


@representante.route("/listado_sedes_solicitadas/<tipo>")
@jwt_required()
def listado_sedes_solicitadas(tipo):
    """Esta funcion devuelve las sedes asociadas al representante (administradas/pendientes/rechazadas)"""

    usuario_actual = get_jwt_identity()
    usuario = usuarios.get_usuario(usuario_actual)
    usuario_solicitudes = solicitudes.usuario_tipo_solicitudes(usuario, tipo)
    info_sedes = sedes.informacion_sede(usuario_solicitudes)
    direcciones = sedes.get_direccion(info_sedes)
    kwargs = {
        "solicitudes":  usuario_solicitudes,
        "info_sedes": info_sedes,
        "direcciones": direcciones,
        "tipo": tipo
    }
    return render_template("/representante/listado_sedes_solicitadas.html", **kwargs)


@representante.route("/ddjj/<id_sede>")
@jwt_required()
def form_ddjj(id_sede):
    usuario_actual = get_jwt_identity()
    if not (validator_permission.has_permission(usuario_actual, "representante_ddjj")):
        return abort(403)
    usuario = usuarios.get_usuario(usuario_actual)
    kwargs = {
        "nombre": usuario.nombre,
        "apellido": usuario.apellido,
        "id_sede": id_sede,
    }
    return render_template("representante/form_ddjj.html", **kwargs)

@representante.post("/carga_ddjj")
@jwt_required()
def carga_ddjj():
    usuario_actual = get_jwt_identity()
    if not (validator_permission.has_permission(usuario_actual, "representante_ddjj")):
        return abort(403)
    data_ddjj = {
        "personal_capacitado": True if request.form.get("per_cap") == "si" else False,
        "dea_señalizado": True if request.form.get("dea_señalizado") == "si" else False,
        "responsable": True if request.form.get("responsable") == "si" else False,
        "protocolo_accion": True if request.form.get("prot_acc") == "si" else False,
        "sistema_emergencia": True if request.form.get("sist_emer") == "si" else False,
        "cantidad_dea": request.form.get("cant_deas") if request.form.get("cant_deas") else None,
    }

    if not validator_ddjj.validator(**data_ddjj):
        flash("Todos los datos deben estar marcados con SI para cargar la declaracion jurada")
        return redirect("/representante/ddjj")
    
    id_sede = request.form.get("id_sede") if request.form.get("id_sede") else None
    data_ddjj["id_sede"] = id_sede
    
    if not ddjj.verificar_ddjj_existente(id_sede):
        flash("Ya existen una declaracion jurada para la sede seleccionada")
        return redirect(url_for("representante.form_ddjj", id_sede=id_sede))
    
    declaracion = ddjj.agregar_ddjj(data_ddjj)
    visita = visitas.agregar_visita(id_sede)
    return redirect("/usuarios/inicio")
