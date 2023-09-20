from flask import Flask
from flask_jwt_extended import JWTManager
from src.web.config import config
from src.core.db import db, init_db

from src.web.controllers.usuarios import usuario_blueprint

#from src.core.db import db, init_db

def create_app(env="development", static_folder="static"):
    # create and configure the app
    app = Flask(__name__, static_folder=static_folder)
    jwt = JWTManager(app)
    app.config.from_object(config[env])

    @app.route('/')
    def hello():
        return 'Hello, World!'
    
    app.register_blueprint(usuario_blueprint)
    
    with app.app_context():
        init_db(app)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    return app