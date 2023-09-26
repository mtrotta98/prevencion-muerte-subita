from flask import render_template

def not_authorized_error(e):
    kwargs = {
        "error_name": "403 Forbidden Error",
        "error_description": "No tiene los permisos para acceder a esta URL",
        "redirect_to": "usuarios.inicio",
        "destino": "Inicio",
    }
    return render_template("error.html", **kwargs), 403