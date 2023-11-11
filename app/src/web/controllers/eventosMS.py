
from flask import Blueprint, render_template, request, flash, redirect, abort
from flask import url_for
from src.web.controllers.validators.validator_permission import has_permission
from src.core import provincias
from src.core import deas
from src.core import responsables
from src.core import sedes
from src.core import eventosms
from src.core import usuarios
from src.core import roles
from src.web.controllers.forms.newEventoMS import NewEventoMSForm
from flask_jwt_extended import get_jwt_identity, jwt_required

eventosMS_blueprint = Blueprint("eventosMS", __name__, url_prefix="/eventosMS")

@eventosMS_blueprint.get("/list/<sede_id>")
@jwt_required()
def eventos_sede(sede_id):
    usuario_actual = get_jwt_identity()
    usuario = usuarios.get_usuario(usuario_actual)
    rol = roles.get_rol(usuario.id_rol)
    if not (has_permission(usuario_actual, "representante_eventos")):
        return abort(403)
    if not sedes.is_representante(sede_id,usuario_actual):
        return abort(403)
    eventos_list=eventosms.get_by_sede(sede_id)
    sede=sedes.get_sede(sede_id)
    return render_template("eventosMS/lista_eventos_sede.html", eventos=eventos_list, sede=sede, nombre=usuario.nombre, apellido=usuario.apellido, rol=rol.nombre)

@eventosMS_blueprint.get("/prov")
@jwt_required()
def eventos_provincia():
    usuario_actual = get_jwt_identity()
    usuario = usuarios.get_usuario(usuario_actual)
    rol = roles.get_rol(usuario.id_rol)
    if not (has_permission(usuario_actual, "admin_eventos")):
        return abort(403)
    eventos_list =[]
    for provincia in usuario.provincias:
        for sede in sedes.get_sedes_provincia(provincia.id):
            for evento in eventosms.get_by_sede(sede.id):
                eventos_list.append(evento)
    return render_template("eventosMS/lista_eventos_provincia.html", eventos=eventos_list, nombre=usuario.nombre, apellido=usuario.apellido, rol=rol.nombre)


@eventosMS_blueprint.get("/new/<sede_id>")
@jwt_required()
def evento_new(sede_id):
    usuario_actual = get_jwt_identity()
    usuario = usuarios.get_usuario(usuario_actual)
    rol = roles.get_rol(usuario.id_rol)
    if not (has_permission(usuario_actual, "representante_eventos")):
        return abort(403)
    newEvento = NewEventoMSForm();
    newEvento.sede_id.data = sede_id
    return render_template("eventosMS/new.html",form=newEvento, sede_id=sede_id, nombre=usuario.nombre, apellido=usuario.apellido, rol=rol.nombre)

@eventosMS_blueprint.route("/add", methods=['POST'])
@jwt_required()
def evento_create():
    usuario_actual = get_jwt_identity()
    if not (has_permission(usuario_actual, "representante_eventos")):
        return abort(403)
    data = request.form     # Recupero el formulario
    evento = eventosms.eventoMS()  # Creo un Registro vacío (modelo)
    form = NewEventoMSForm(data)   # Creo un formulario a partir de los datos recibidos (wtforms)
    if not sedes.is_representante(data['sede_id'],usuario_actual):
        return abort(403)
    if not (deas.get_by_sede(data['sede_id']) and responsables.get_by_sede(data['sede_id'])):
        flash("Error. Se debe contar con, al menos, un DEA y un Responsable en la sede para cargar eventos." , "error")
        return redirect(url_for('eventosMS.eventos_sede', sede_id=data['sede_id']))
    if (data and form.validate()):  # Valido la información recibida 
        form.populate_obj(evento)     # Relleno los datos recibidos       
        # Intentar salvar
        try:
            eventosms.save(evento)        
            flash("Se registró correctamente el evento", "success")
        except:
            flash("Ocurrió un error. No se pudo cargar el evento.", "error")
    # Si no se validó el formulario, mostrar los errores
    else:
        for field in form.errors:
            for error in form.errors[field]:
                flash(field + ": " + error, "error")
        return redirect(url_for('eventosMS.evento_new', sede_id=data['sede_id']))
    return redirect(url_for('eventosMS.eventos_sede', sede_id=evento.sede_id))

@eventosMS_blueprint.get("/detail/<id>")
@jwt_required()
def evento_detail(id):
    usuario_actual = get_jwt_identity()
    usuario = usuarios.get_usuario(usuario_actual)
    rol = roles.get_rol(usuario.id_rol)
    if not ((has_permission(usuario_actual, "representante_eventos")) or (has_permission(usuario_actual, "admin_eventos"))):
        return abort(403)
    evento=eventosms.get_by_id(id)
    if not evento:
        return redirect(url_for('usuarios.inicio'))
    if ((has_permission(usuario_actual, "representante_eventos")) and not (sedes.is_representante(evento.sede_id,usuario_actual))):
        return abort(403)
    eventoForm = NewEventoMSForm();
    eventoForm.marca.data = evento.marca
    eventoForm.modelo.data = evento.modelo
    eventoForm.fecha.data = evento.fecha
    eventoForm.edad.data = evento.edad
    eventoForm.sexo.data = eventoForm.sexo.choices[evento.sexo-1][1]
    eventoForm.sobrevive.data = evento.sobrevive
    eventoForm.usoDea.data = evento.usoDea
    eventoForm.usoRCP.data = evento.usoRCP
    eventoForm.usosDEA.data = evento.usosDEA
    eventoForm.tiempoRCP.data = evento.tiempoRCP
    eventoForm.descripcion.data = evento.descripcion
    eventoForm.sede_id.data = evento.sede_id    
    return render_template("eventosMS/detail.html",form=eventoForm, nombre=usuario.nombre, apellido=usuario.apellido, rol=rol.nombre)
   

@eventosMS_blueprint.get("/delete/<id>")
@jwt_required()
def evento_delete(id):
    """Elimina un evento, si este existe """
    usuario_actual = get_jwt_identity()
    if not (has_permission(usuario_actual, "representante_eventos")):
        return abort(403)
    evento=eventosms.get_by_id(id)
    sede=evento.sede_id
    if evento:
        eventosms.destroy(evento);
    return redirect(url_for('eventosMS.eventos_sede', sede_id=sede))

