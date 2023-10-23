from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect
from flask_jwt_extended import JWTManager
from flask_jwt_extended import jwt_required
from src.web.config import config
from src.core.db import db, init_db
from src.core import visitas, sedes, provincias
from src.web.helpers import handlers
from src.web.helpers.send_emails import enviar_email_vencimiento_certificacion

from src.web.controllers.usuarios import usuario_blueprint
from src.web.controllers.entidades import entidad_blueprint
from src.web.controllers.sedes import sede_blueprint
from src.web.controllers.solicitudes import solicitud_blueprint
from src.web.controllers.admin_provincial import admin_provincial
from src.web.controllers.superusuarios import super_usuario
from src.web.controllers.representante import representante
from src.web.controllers.deas import dea_blueprint

#from src.core.db import db, init_db

def create_app(env="development", static_folder="static"):
    # create and configure the app
    app = Flask(__name__, static_folder=static_folder)
    app.config.from_object(config[env])
    app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    app.config['JWT_SECRET_KEY'] = 'super-secret'
    app.config['JWT_ACCESS_TOKEN_EXPIRES '] = False
    app.config['JWT_COOKIE_CSRF_PROTECT'] = False
    app.config['JWT_ACCESS_CSRF_HEADER_NAME'] = "csrf_access_token"

    csrf = CSRFProtect(app)
    jwt = JWTManager(app)

    @app.route('/')
    @jwt_required()
    def hello():
        return 'Hello, World!'
    
    app.register_blueprint(usuario_blueprint)
    app.register_blueprint(entidad_blueprint)
    app.register_blueprint(sede_blueprint)
    app.register_blueprint(admin_provincial)
    app.register_blueprint(super_usuario)
    app.register_blueprint(representante)
    app.register_blueprint(solicitud_blueprint)
    app.register_blueprint(dea_blueprint)
    
    with app.app_context():
        init_db(app)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    @jwt.unauthorized_loader
    def custom_unauthorized_response(_err):
        kwargs = {
            "error_name": "403 Forbidden Error",
            "error_description": "No tiene los permisos para acceder a esta URL",
            "redirect_to": "usuarios.form_login",
            "destino": "login",
        }
        return render_template("error.html", **kwargs)
    
    @jwt.expired_token_loader
    def custom_expired_response(jwt_header, jwt_payload):
        kwargs = {
            "error_name": "403 Forbidden Error",
            "error_description": "Expiro el token, por favor loguearse nuevamente",
            "redirect_to": "usuarios.form_login",
            "destino": "login",
        }
        return render_template("error.html", **kwargs)
    
    def verificar_certificaciones():
        with app.app_context():
            visitas_aprobadas = visitas.get_visitas_aprobadas()
            for visita in visitas_aprobadas:
                sede_visitada = sedes.get_sede(visita.id_sede)
                provincia_sede = provincias.get_provincia(sede_visitada.id_provincia)
                fecha_vencimiento = visita.fecha + timedelta(days=365)
                fecha_actual = datetime.now().date()
                if fecha_vencimiento == fecha_actual:
                    visita.resultado = False
                    visita.observacion = "Certificacion vencida"
                    sede_visitada.estado = "Espacio con certificacion vencida"
                    db.session.commit()
                    for representante in sede_visitada.usuarios:
                        enviar_email_vencimiento_certificacion(representante.email, representante.nombre, representante.apellido, sede_visitada.nombre)
                        
                

    scheduler = BackgroundScheduler()
    scheduler.add_job(func=verificar_certificaciones, trigger="interval", seconds=30) # 86400
    scheduler.start()

    app.register_error_handler(403, handlers.not_authorized_error)

    return app