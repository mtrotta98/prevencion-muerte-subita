import uuid

from flask import Blueprint, render_template, request, flash, redirect, make_response, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, unset_jwt_cookies
from flask_jwt_extended import create_access_token, set_access_cookies
from datetime import datetime, timedelta

from src.core import usuarios
from src.core import provincias
from src.core import roles
from src.web.controllers.validators import validator_usuario

usuario_blueprint = Blueprint("usuarios", __name__, url_prefix="/usuarios")


@usuario_blueprint.route("/registro")
def form_usuario():
    kwargs = {
        "provincias": provincias.get_provincias()
    }
    return render_template("usuarios/registro.html", **kwargs)

@usuario_blueprint.route("/alta", methods=["POST"])
def agregar_usuario():
    """Esta funcion llama al metodo correspondiente para dar de alta un usuario."""
    nombre_rol = request.form.get("rol")
    provincia = request.form.get("prov")
    rol = roles.get_rol(nombre_rol)

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
    
        if provincia != "":
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
    
    access_token = create_access_token(identity=usuario.id_publico)
    response = jsonify(access_token)
    set_access_cookies(response, access_token)
    return "Te logueaste!"

@usuario_blueprint.get("/logout_publico")
@jwt_required()
def logout_publico():
    """Esta funcion desloguea a un socio de la app publica"""
    response = jsonify()
    unset_jwt_cookies(response)
    return redirect("/usuarios/login")