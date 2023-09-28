import uuid

from flask import Blueprint, render_template, request, flash, redirect, make_response, jsonify, abort
from flask_jwt_extended import jwt_required, unset_jwt_cookies
from flask_jwt_extended import create_access_token, set_access_cookies, get_jwt_identity

from src.core import usuarios
from src.core import provincias
from src.core import roles
from src.core import solicitudes
from src.web.controllers.validators import validator_usuario, validator_permission

usuario_blueprint = Blueprint("usuarios", __name__, url_prefix="/usuarios")


@usuario_blueprint.route("/registro")
def form_usuario():
    kwargs = {
        "provincias": provincias.get_provincias()
    }
    return render_template("usuarios/registro.html", **kwargs)

@usuario_blueprint.route("/inicio")
@jwt_required()
def inicio():
    usuario_actual = get_jwt_identity()
    usuario = usuarios.get_usuario(usuario_actual)
    rol = roles.get_rol(usuario.id_rol)
    kwargs = {
        "nombre": usuario.nombre,
        "apellido": usuario.apellido,
        "rol": rol.nombre,
    }
    return render_template("index.html", **kwargs)

@usuario_blueprint.route("/alta", methods=["POST"])
def agregar_usuario():
    """Esta funcion llama al metodo correspondiente para dar de alta un usuario."""
    nombre_rol = request.form.get("rol")
    data_provincias = request.form.getlist("prov")
    rol = roles.get_rol_por_nombre(nombre_rol)

    data_usuario = {
        "nombre": request.form.get("nombre").capitalize(),
        "apellido": request.form.get("apellido").capitalize(),
        "usuario": request.form.get("usuario"),
        "contraseña": request.form.get("pass1"),
        "contraseña2": request.form.get("pass2"),
        "dni": request.form.get("dni"),
        "id_rol": rol.id
    }

    data_existente, mensaje = usuarios.validar_datos_existentes(data_usuario["usuario"], data_usuario["dni"])
    inputs_validados, mensaje2 = validator_usuario.validar_inputs(**data_usuario)

    if data_existente and inputs_validados:
        data_usuario.pop("contraseña2")
        data_usuario["id_publico"] = str(uuid.uuid4())
        usuario = usuarios.agregar_usuario(data_usuario)
    
        if data_provincias:
            for provincia in data_provincias:
                prov = provincias.get_provincia(provincia)
                usuarios.agregar_provincia(usuario, prov)

        return redirect("/usuarios/login")
    else:
        flash(mensaje) if mensaje != "" else flash(mensaje2)
        return redirect("/usuarios/registro")
    
@usuario_blueprint.route("/login")
def form_login():
    """Esta funcion retorna el formulario para loguearse"""
    return render_template("usuarios/login.html")

@usuario_blueprint.post("/authenticate")
def authenticate():
    """Esta funcion realiza la autenticacion de usuarios"""
    params = request.form
    validacion, mensaje = validator_usuario.validar_inputs_login(usuario=params["usuario"], contraseña=params["contraseña"])

    if not validacion:
        flash(mensaje)
        return redirect("/usuarios/login")
    
    usuario, mensaje = usuarios.verificar_usuario(params["usuario"], params["contraseña"])
    
    if usuario is None:
        flash(mensaje)
        return redirect("/usuarios/login")
    
    access_token = create_access_token(identity=str(usuario.id))
    resp = make_response(redirect('/usuarios/inicio', 302))
    set_access_cookies(resp, access_token)

    return resp

@usuario_blueprint.get("/logout")
@jwt_required()
def logout():
    resp = make_response(redirect("/usuarios/login", 302))
    unset_jwt_cookies(resp)
    return resp

@usuario_blueprint.get("/solicitudes")
@jwt_required()
def listado_solicitudes():
    usuario_actual = get_jwt_identity()
    if not (validator_permission.has_permission(usuario_actual, "administrador_provincial_autorizaciones")):
        return abort(403)
    info_solicitudes = []
    usuario = usuarios.get_usuario(usuario_actual)
    rol = roles.get_rol(usuario.id_rol)
    tipo = request.args.get("tipo") if request.args.get("tipo", type=str) != "" else None
    solis = solicitudes.solicitudes(tipo)
    for soli in solis:
        data_usuario = usuarios.get_usuario(soli.id_usuario)
        dict_usuario = {"Nombre": data_usuario.nombre, "Apellido": data_usuario.apellido, "Estado": soli.estado, "Razon": soli.razon, "id_solicitud": soli.id}
        info_solicitudes.append(dict_usuario)
    kwargs = {
        "nombre": usuario.nombre,
        "apellido": usuario.apellido,
        "rol": rol.nombre,
        "solicitudes": info_solicitudes,
    }
    return render_template("usuarios/evaluar_solicitudes.html", **kwargs)

@usuario_blueprint.route("/info_solicitud/<id>")
@jwt_required()
def info_solicitud(id):
    usuario_actual = get_jwt_identity()
    if not (validator_permission.has_permission(usuario_actual, "administrador_provincial_autorizaciones")):
        return abort(403)
    usuario = usuarios.get_usuario(usuario_actual)
    solicitud = solicitudes.get_solicitud(id)
    id_admin = solicitud.id_usuario
    data_admin = usuarios.get_usuario(id_admin)
    kwargs = {
        "nombre": usuario.nombre,
        "apellido": usuario.apellido,
        "nombre_admin": data_admin.nombre + " " + data_admin.apellido,
        "id_solicitud": id,
        #"nombre_sede":,
    }
    return render_template("usuarios/info_solicitud.html", **kwargs)

@usuario_blueprint.post("/aceptar_solicitud")
@jwt_required()
def evaluacion_solicitud():
    usuario_actual = get_jwt_identity()
    if not (validator_permission.has_permission(usuario_actual, "administrador_provincial_autorizaciones")):
        return abort(403)
    data_solicitud = {
        "id": request.form.get("id"),
        "estado": request.form.get("rol"),
        "razon": request.form.get("observacion"),
    }
    
    solicitudes.actualizar_solicitud(data_solicitud)

    return redirect("/usuarios/solicitudes")
