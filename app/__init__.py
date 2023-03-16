from flask import Flask, session, g
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user

db = SQLAlchemy()

def create_app():
	#intial flask app and load config file
	app = Flask(__name__, instance_relative_config=False)
	app.config.from_object("config.DevelopmentConfig")

	from datetime import datetime, timedelta

	#session timeout
	@app.before_request
	def before_request():
		session.permanent = True
		app.permanent_session_lifetime = timedelta(minutes=3)
		session.modified = True
		g.user = current_user

	#intialize login module
	login_manager = LoginManager()
	login_manager.login_view = 'auth.login'
	login_manager.init_app(app)
	login_manager.refresh_view = 'auth.login'
	login_manager.needs_refresh_message = (u"session timeout, please Re-login")


	#load user from db if authenticated
	from .models import User

	@login_manager.user_loader
	def load_user(user_id):
		return User.query.get(user_id)


	#configure database
	from . import models

	db.init_app(app)

	with app.app_context():
		db.create_all()

	#Blueprints register
	from .auth import auth as auth_blueprint
	app.register_blueprint(auth_blueprint)

	from .main import main as main_blueprint
	app.register_blueprint(main_blueprint)

	return app