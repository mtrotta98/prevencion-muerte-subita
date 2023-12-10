
from flask import Blueprint, render_template, request, flash, redirect, abort
from flask import url_for
from src.web.controllers.validators.validator_permission import has_permission
from src.core import deas
from src.core import responsables
from src.core import sedes
from src.core import eventosmant
from src.core import usuarios
from src.core import roles
from src.web.controllers.forms.newEventoMant import NewEventoMantForm
from flask_jwt_extended import get_jwt_identity, jwt_required

eventosMant_blueprint = Blueprint("eventosMant", __name__, url_prefix="/eventosMant")

@eventosMant_blueprint.get("/list/<dea_id>")
@jwt_required()
def eventos_dea(dea_id):
    usuario_actual = get_jwt_identity()
    usuario = usuarios.get_usuario(usuario_actual)
    rol = roles.get_rol(usuario.id_rol)
    if not (has_permission(usuario_actual, "mantenimiento_dea")):
        return abort(403)
    dea=deas.get_by_id(dea_id)
    if not sedes.is_representante(dea.sede_id,usuario_actual):
        return abort(403)
    eventos_list=eventosmant.get_by_dea(dea_id)    
    return render_template("eventosMant/lista_mant.html", eventos=eventos_list, sede_id=dea.sede_id , dea=dea, nombre=usuario.nombre, apellido=usuario.apellido, rol=rol.nombre)


@eventosMant_blueprint.get("/new/<dea_id>")
@jwt_required()
def evento_new(dea_id):
    usuario_actual = get_jwt_identity()
    usuario = usuarios.get_usuario(usuario_actual)
    rol = roles.get_rol(usuario.id_rol)
    if not (has_permission(usuario_actual, "mantenimiento_dea")):
        return abort(403)
    dea=deas.get_by_id(dea_id)
    newEvento = NewEventoMantForm();
    newEvento.dea_id.data = dea_id
    return render_template("eventosMant/new.html",form=newEvento, dea=dea, nombre=usuario.nombre, apellido=usuario.apellido, rol=rol.nombre)

@eventosMant_blueprint.route("/add", methods=['POST'])
@jwt_required()
def evento_create():
    usuario_actual = get_jwt_identity()
    if not (has_permission(usuario_actual, "mantenimiento_dea")):
        return abort(403)
    data = request.form     # Recupero el formulario
    evento = eventosmant.eventoMant()  # Creo un Registro vacío (modelo)
    form = NewEventoMantForm(data)   # Creo un formulario a partir de los datos recibidos (wtforms)
    dea =  deas.get_by_id(data['dea_id'])
    if not sedes.is_representante(dea.sede_id,usuario_actual):
        return abort(403)
    if (data and form.validate()):  # Valido la información recibida 
        form.populate_obj(evento)     # Relleno los datos recibidos       
        # Intentar salvar
        try:
            eventosmant.save(evento)        
            flash("Se registró correctamente el evento", "success")
        except:
            flash("Ocurrió un error. No se pudo cargar el evento.", "error")
    # Si no se validó el formulario, mostrar los errores
    else:
        for field in form.errors:
            for error in form.errors[field]:
                flash(field + ": " + error, "error")
        return redirect(url_for('eventosMant.evento_new', dea_id=data['dea_id']))
    # Actualizo el DEA (no es la manera correcta)
    dea.ultimomantenimiento = evento.fecha
    deas.save(dea)
    return redirect(url_for('eventosMant.eventos_dea', dea_id=evento.dea_id))

@eventosMant_blueprint.get("/delete/<id>")
@jwt_required()
def evento_delete(id):
    """Elimina un evento, si este existe """
    usuario_actual = get_jwt_identity()
    if not (has_permission(usuario_actual, "mantenimiento_dea")):
        return abort(403)
    evento=eventosmant.get_by_id(id)
    dea=evento.dea_id
    if evento:
        eventosmant.destroy(evento);
    return redirect(url_for('eventosMant.eventos_dea', dea_id=dea))

