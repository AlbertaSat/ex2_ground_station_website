from flask import render_template, Blueprint

home_blueprint = Blueprint('home',__name__)

@home_blueprint.route('/')
@home_blueprint.route('/home')
@home_blueprint.route('/flightschedule')
@home_blueprint.route('/livecommands')
@home_blueprint.route('/housekeeping')
@home_blueprint.route('/automatedcommandsequence')
@home_blueprint.route('/login')
@home_blueprint.route('/logs')
@home_blueprint.route('/logout')
@home_blueprint.route('/help')
@home_blueprint.route('/adduser')
@home_blueprint.route('/manageusers')
@home_blueprint.route('/resetpassword')
def index():
	return render_template("index.html")

