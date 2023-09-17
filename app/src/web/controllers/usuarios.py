import json

from flask import Blueprint, render_template, request, flash, redirect, session, abort

from src.core import usuarios
from src.core import provincias
from src.core import roles

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
        "dni": request.form.get("dni"),
        "id_rol": rol.id
    }

    usuario = usuarios.agregar_usuario(data_usuario)
    
    if provincia is not None:
        prov = provincias.get_provincia(provincia)
        usuarios.agregar_provincia(usuario, prov)
    return 'Hello, World!'