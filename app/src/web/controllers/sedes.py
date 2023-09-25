import json

from src.core import sedes
from flask import Blueprint, render_template, request, flash, redirect, session, abort

sede_blueprint = Blueprint("sedes", __name__, url_prefix="/sedes")

@sede_blueprint.route("/registro")
def form_sede():
    kwargs = {
        "lista_sedes" : sedes.get_sedes()
    }
    return render_template("sedes/registro_sede.html", **kwargs)