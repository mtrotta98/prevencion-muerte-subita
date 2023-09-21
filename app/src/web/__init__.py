from flask import Flask, render_template
from flask_jwt_extended import JWTManager
from flask_jwt_extended import jwt_required
from src.web.config import config
from src.core.db import db, init_db

from src.web.controllers.usuarios import usuario_blueprint

#from src.core.db import db, init_db

def create_app(env="development", static_folder="static"):
    # create and configure the app
    app = Flask(__name__, static_folder=static_folder)
    app.config.from_object(config[env])
    app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    app.config['JWT_SECRET_KEY'] = 'super-secret'

    jwt = JWTManager(app)

    @app.route('/')
    @jwt_required()
    def hello():
        return 'Hello, World!'
    
    app.register_blueprint(usuario_blueprint)
    
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

    return app