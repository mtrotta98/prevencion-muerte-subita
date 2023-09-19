import json

from src.core import entidades
from flask import Blueprint, render_template, request, flash, redirect, session, abort

entidad_blueprint = Blueprint("entidades", __name__, url_prefix="/entidades")

@entidad_blueprint.route("/registro")
def form_entidad():
    kwargs = {
        "lista_entidades" : entidades.get_entidades() 
    }
    return render_template("entidades/registro_entidad.html", **kwargs)