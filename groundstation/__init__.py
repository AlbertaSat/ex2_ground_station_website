import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(script_info=None):
	app = Flask(__name__,
 	static_folder = './public',
 	template_folder="./templates")

	app_settings = os.getenv('APP_SETTINGS')
	app.config.from_object(app_settings)

	db.init_app(app)

	from groundstation.views import home_blueprint
	# register the blueprints
	app.register_blueprint(home_blueprint)

	@app.shell_context_processor
	def ctx():
		return {'app': app, 'db': db}

	return app