
from flask import Blueprint, render_template, request, flash, redirect, abort
from flask import url_for
from src.web.controllers.validators.validator_permission import has_permission
from src.core import deas
from src.core import responsables
from src.core import sedes
from src.core import usuarios
from src.web.controllers.forms.newDea import NewDEAForm
from flask_jwt_extended import get_jwt_identity, jwt_required

dea_blueprint = Blueprint("deas", __name__, url_prefix="/deas")

@dea_blueprint.get("/new/<sede_id>")
@jwt_required()
def dea_new(sede_id):
    usuario_actual = get_jwt_identity()
    if not (has_permission(usuario_actual, "representante_alta_dea")):
        return abort(403)
    newDea = NewDEAForm();
    """
    newDea.marca.choices =[('1', 'Meditech'),               # Reemplazar por API
                                 ('2', 'PhisioControl'), 
                                 ('3', 'Medtronic'), 
                                 ('4', 'Mindray'), 
                                 ('5', 'HeartSine'), 
                                 ('6', 'Philips'), 
                                 ('7', 'Zoll'), 
                                 ('8', 'Schiller'), 
                                 ('9', 'Defibtech')]"""
    """
    newDea.modelo.choices =[('1', 'Mempeliece'),            # Reemplazar por API
                                 ('2', 'Accilingul'), 
                                 ('3', 'Venerthagn'), 
                                 ('4', 'Tamuligusa'), 
                                 ('5', 'Flaucebato')]"""
    return render_template("deas/new.html",form=newDea, sede_id=sede_id)

@dea_blueprint.route("/add", methods=['POST'])
@jwt_required()
def dea_create(sede_id):
    usuario_actual = get_jwt_identity()
    if not (has_permission(usuario_actual, "representante_alta_dea")):
        return abort(403)
    data = request.form     # Recupero el formulario
    dea = deas.DEA()             # Creo un DEA vacío (modelo)
    form = NewDEAForm(data)   # Creo un formulario de DEA a partir de los datos recibidos (wtforms)
    if (data and form.validate()):  # Valido la información recibida 
        form.populate_obj(dea)     # Relleno los datos del DEA (modelo) a partir de los datos recibidos
        dea.sede_id = sede_id        
        # Intentar salvar
        try:
            """resp = []
            resp.append(responsables.get_by_id(form.__dict__['responsable'].__dict__['data']))
            dea.responsables = resp"""
            deas.save(dea)        
            flash("Se creo correctamente el DEA: "+dea.denominacion, "success")
        except:
            flash("Ocurrió un error. No se pudo cargar el DEA.", "error")
    # Si no se validó el formulario, mostrar los errores
    else:
        for field in form.errors:
            for error in form.errors[field]:
                flash(error, "error")
        return redirect(url_for("deas.dea_new"))
    return redirect(url_for('usuarios.inicio'))

@dea_blueprint.get("/mod/<id>")
@jwt_required()
def dea_mod(id):
    usuario_actual = get_jwt_identity()
    if not (has_permission(usuario_actual, "representante_alta_dea")):
        return abort(403)
    dea=deas.get_by_id(id)
    if not dea:
        return redirect(url_for('usuarios.inicio'))
    newDea = NewDEAForm();
    newDea.marca.choices =[(dea.marca, dea.marca)]
    newDea.modelo.choices =[(dea.modelo, dea.modelo)]
    newDea.nSerie.data = dea.nSerie
    newDea.denominacion.data = dea.denominacion
    newDea.solidario.data = dea.solidario
    newDea.activo.data = dea.activo
    newDea.ultimoMantenimiento.data = dea.ultimoMantenimiento
    return render_template("deas/mod.html",form=newDea, id_dea=dea.id)

@dea_blueprint.route("/edit/<id>", methods = ["POST", "GET"])
@jwt_required()
def dea_edit(id, **kwargs):
    usuario_actual = get_jwt_identity()
    if not (has_permission(usuario_actual, "representante_alta_dea")):
        return abort(403)
    dea=deas.get_by_id(id)
    if not dea:
        return redirect(url_for('usuarios.inicio'))
    data = request.form     # Recupero el formulario
    form = NewDEAForm(data)   # Creo un formulario de DEA a partir de los datos recibidos (wtforms)
    #import pdb; pdb.set_trace()
    if (data and form.validate()):  # Valido la información recibida 
        form.populate_obj(dea)     # Relleno los datos del DEA (modelo) a partir de los datos recibidos
        # Intentar salvar
        try:
            deas.save(dea)        
            flash("Se modificó correctamente el DEA: "+dea.denominacion, "success")
        except:
            flash("Ocurrió un error. No se pudo cargar el DEA.", "error")
    # Si no se validó el formulario, mostrar los errores
    else:
        for field in form.errors:
            for error in form.errors[field]:
                flash(error, "error")
        return redirect(url_for("deas.dea_mod"))
    return redirect(url_for('usuarios.inicio'))