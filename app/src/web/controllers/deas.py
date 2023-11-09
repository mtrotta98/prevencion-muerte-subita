
from flask import Blueprint, render_template, request, flash, redirect, abort
from flask import url_for
from src.web.controllers.validators.validator_permission import has_permission
from src.core import deas
from src.core import sedes
from src.core import usuarios
from src.core import roles
from src.web.controllers.forms.newDea import NewDEAForm
from flask_jwt_extended import get_jwt_identity, jwt_required

dea_blueprint = Blueprint("deas", __name__, url_prefix="/deas")

@dea_blueprint.get("/list/<sede_id>")
@jwt_required()
def dea_list(sede_id):
    usuario_actual = get_jwt_identity()
    usuario = usuarios.get_usuario(usuario_actual)
    rol = roles.get_rol(usuario.id_rol)
    if not (has_permission(usuario_actual, "representante_alta_dea")):
        return abort(403)
    dea_list=deas.get_by_sede(sede_id)
    sede=sedes.get_sede(sede_id)
    return render_template("deas/lista_deas_sede.html", deas=dea_list, sede=sede, nombre=usuario.nombre, apellido=usuario.apellido, rol=rol.nombre)

@dea_blueprint.get("/new/<sede_id>")
@jwt_required()
def dea_new(sede_id):
    usuario_actual = get_jwt_identity()
    usuario = usuarios.get_usuario(usuario_actual)
    rol = roles.get_rol(usuario.id_rol)
    if not (has_permission(usuario_actual, "representante_alta_dea")):
        return abort(403)
    newDea = NewDEAForm();
    newDea.sede_id.data = sede_id
    return render_template("deas/new.html",form=newDea, sede_id=sede_id, nombre=usuario.nombre, apellido=usuario.apellido, rol=rol.nombre)

@dea_blueprint.route("/add", methods=['POST'])
@jwt_required()
def dea_create():
    usuario_actual = get_jwt_identity()
    if not (has_permission(usuario_actual, "representante_alta_dea")):
        return abort(403)
    data = request.form     # Recupero el formulario
    dea = deas.DEA()             # Creo un DEA vacío (modelo)
    form = NewDEAForm(data)   # Creo un formulario de DEA a partir de los datos recibidos (wtforms)
    if (data and form.validate()):  # Valido la información recibida 
        form.populate_obj(dea)     # Relleno los datos del DEA (modelo) a partir de los datos recibidos       
        # Intentar salvar
        try:
            deas.save(dea)        
            flash("Se creo correctamente el DEA: "+dea.denominacion, "success")
        except:
            flash("Ocurrió un error. No se pudo cargar el DEA.", "error")
    # Si no se validó el formulario, mostrar los errores
    else:
        for field in form.errors:
            for error in form.errors[field]:
                flash(field + ": " + error, "error")
        return redirect(url_for('deas.dea_new', sede_id=data['sede_id']))
    return redirect(url_for('deas.dea_list', sede_id=dea.sede_id))

@dea_blueprint.get("/mod/<id>")
@jwt_required()
def dea_mod(id):
    usuario_actual = get_jwt_identity()
    usuario = usuarios.get_usuario(usuario_actual)
    rol = roles.get_rol(usuario.id_rol)
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
    newDea.sede_id.data = dea.sede_id
    return render_template("deas/mod.html",form=newDea, id_dea=dea.id, nombre=usuario.nombre, apellido=usuario.apellido, rol=rol.nombre)

@dea_blueprint.route("/edit/<id>", methods = ["POST", "GET"])
@jwt_required()
def dea_edit(id, **kwargs):
    usuario_actual = get_jwt_identity()
    if not (has_permission(usuario_actual, "representante_alta_dea")):
        return abort(403)
    dea=deas.get_by_id(id)
    sede = dea.sede_id
    if not sede:
        sede = 1
    if not dea:
        return redirect(url_for('usuarios.inicio'))
    data = request.form     # Recupero el formulario
    form = NewDEAForm(data)   # Creo un formulario de DEA a partir de los datos recibidos (wtforms)
    if (data and form.validate()):  # Valido la información recibida 
        form.populate_obj(dea)     # Relleno los datos del DEA (modelo) a partir de los datos recibidos
        try:
            deas.save(dea)        
            flash("Se modificó correctamente el DEA: "+dea.denominacion, "success")
        except:
            flash("Ocurrió un error. No se pudo cargar el DEA.", "error")
    # Si no se validó el formulario, mostrar los errores
    else:
        for field in form.errors:
            for error in form.errors[field]:
                flash(field + ": " + error, "error")
        return redirect(url_for('deas.dea_mod', sede_id=data['sede_id']))
    return redirect(url_for('deas.dea_list', sede_id=sede))
    

@dea_blueprint.get("/delete/<id>")
@jwt_required()
def dea_delete(id):
    """Elimina un DEA, si este existe (baja logica, lo desactiva)"""
    usuario_actual = get_jwt_identity()
    if not (has_permission(usuario_actual, "representante_alta_dea")):
        return abort(403)
    dea=deas.get_by_id(id)
    sede=dea.sede_id
    if dea:
        #deas.destroy(dea);
        deas.deactivate(dea);
    return redirect(url_for('deas.dea_list', sede_id=sede))

