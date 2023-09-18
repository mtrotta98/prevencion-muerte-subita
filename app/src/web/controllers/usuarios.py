import json

from flask import Blueprint, render_template, request, flash, redirect, session, abort

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
        usuario = usuarios.agregar_usuario(data_usuario)
    
        if provincia != "":
            prov = provincias.get_provincia(provincia)
            usuarios.agregar_provincia(usuario, prov)

        return 'Hello, World!'
    else:
        flash(mensaje) if mensaje != "" else flash(mensaje2)
        return redirect("/usuarios/registro")