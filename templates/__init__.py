from flask import Flask
app = Flask(__name__,
 	static_folder = './public',
 	template_folder="./static")

from templates.home.views import home_blueprint
# register the blueprints
app.register_blueprint(home_blueprint)
