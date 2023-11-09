
from flask import Blueprint, render_template, request, flash, redirect, abort
from flask import url_for
from src.web.controllers.validators.validator_permission import has_permission
from src.core import responsables
from src.core import sedes
from src.web.controllers.forms.newResp import NewRespForm
from flask_jwt_extended import get_jwt_identity, jwt_required

responsable_blueprint = Blueprint("responsables", __name__, url_prefix="/responsables")

@responsable_blueprint.get("/list/<sede_id>")
@jwt_required()
def responsable_list(sede_id):
    usuario_actual = get_jwt_identity()
    if not (has_permission(usuario_actual, "representante_alta_dea")):
        return abort(403)
    responsable_list=responsables.get_by_sede(sede_id)
    sede=sedes.get_sede(sede_id)
    return render_template("responsables/lista_resp_sede.html", responsables=responsable_list, sede=sede)


@responsable_blueprint.get("/new/<sede_id>")
@jwt_required()
def responsable_new(sede_id):
    usuario_actual = get_jwt_identity()
    if not (has_permission(usuario_actual, "representante_alta_dea")):
        return abort(403)
    newResp = NewRespForm();
    newResp.sede_id.data = sede_id
    return render_template("responsables/new.html",form=newResp)

@responsable_blueprint.route("/add", methods = ["POST"])
@jwt_required()
def responsable_create():
    usuario_actual = get_jwt_identity()
    if not (has_permission(usuario_actual, "representante_alta_dea")):
        return abort(403)
    data = request.form     # Recupero el formulario
    responsable = responsables.Responsable()             
    form = NewRespForm(data)   # Creo un formulario a partir de los datos recibidos (wtforms)
    if (data and form.validate()):  # Valido la información recibida 
        form.populate_obj(responsable)     # Relleno a partir de los datos recibidos
        # Intentar salvar
        try:
            responsables.save(responsable)        
            flash("Se añadió el responsable: "+responsable.Nombre + " " + responsable.Apellido, "success")
        except:
            flash("Ocurrió un error. No se pudo cargar el registro.", "error")
    # Si no se validó el formulario, mostrar los errores
    else:
        for field in form.errors:
            for error in form.errors[field]:
                flash(error, "error")
        return redirect(url_for("responsables.responsable_new"))
    return redirect(url_for('responsables.responsable_list', sede_id=responsable.sede_id))

@responsable_blueprint.get("/mod/<id>")
@jwt_required()
def responsable_mod(id):
    usuario_actual = get_jwt_identity()
    if not (has_permission(usuario_actual, "representante_alta_dea")):
        return abort(403)
    responsable=responsables.get_by_id(id)
    if not responsable:
        return redirect(url_for('usuarios.inicio'))
    newResp = NewRespForm();
    newResp.nombre.data = responsable.nombre
    newResp.apellido.data = responsable.apellido
    newResp.teléfono.data = responsable.teléfono
    newResp.email.data = responsable.email
    newResp.dni.data = responsable.dni
    newResp.sede_id.data = responsable.sede_id
    return render_template("responsables/mod.html",form=newResp, id_responsable=responsable.id)

@responsable_blueprint.route("/edit/<id>", methods = ["POST", "GET"])
@jwt_required()
def responsable_edit(id, **kwargs):
    usuario_actual = get_jwt_identity()
    if not (has_permission(usuario_actual, "representante_alta_dea")):
        return abort(403)
    responsable=responsables.get_by_id(id)
    sede = responsable.sede_id
    if not sede:
        sede = 1
    if not responsable:
        return redirect(url_for('usuarios.inicio'))
    data = request.form     # Recupero el formulario
    form = NewRespForm(data)   # Creo un formulario a partir de los datos recibidos (wtforms)
    if (data and form.validate()):  # Valido la información recibida 
        form.populate_obj(responsable)     # Relleno a partir de los datos recibidos
        try:
            responsables.save(responsable)        
            flash("Se modificó el responsable: "+responsable.Nombre + " " + responsable.Apellido, "success")
        except:
            flash("Ocurrió un error. No se pudo cargar el registro.", "error")
    # Si no se validó el formulario, mostrar los errores
    else:
        for field in form.errors:
            for error in form.errors[field]:
                flash(error, "error")
        return redirect(url_for("responsables.responsable_mod"))
    return redirect(url_for('responsables.responsable_list', sede_id=sede))


@responsable_blueprint.get("/delete/<id>")
@jwt_required()
def responsable_delete(id):
    usuario_actual = get_jwt_identity()
    if not (has_permission(usuario_actual, "representante_alta_dea")):
        return abort(403)
    responsable=responsables.get_by_id(id)
    sede=responsable.sede_id
    if responsable:
        responsables.destroy(responsable);
    return redirect(url_for('responsables.responsable_list', sede_id=sede))

