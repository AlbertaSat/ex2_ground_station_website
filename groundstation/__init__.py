import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()

def create_app(script_info=None):
    app = Flask(__name__,
 	static_folder = './public',
 	template_folder="./templates")

    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    from groundstation.views import home_blueprint
    from groundstation.backend_api.housekeeping import housekeeping_blueprint
    from groundstation.backend_api.flightschedule import flightschedule_blueprint
    from groundstation.backend_api.passover import passover_blueprint
    from groundstation.backend_api.user import user_blueprint
    from groundstation.backend_api.auth import auth_blueprint
    from groundstation.backend_api.communications import communications_blueprint
    from groundstation.backend_api.telecommand import telecommand_blueprint
    # register the blueprints
    app.register_blueprint(home_blueprint)
    app.register_blueprint(housekeeping_blueprint)
    app.register_blueprint(flightschedule_blueprint)
    app.register_blueprint(passover_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(communications_blueprint)
    app.register_blueprint(telecommand_blueprint)

    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': db}

    return app
