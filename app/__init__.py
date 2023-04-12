from flask import Flask, session, g
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_ckeditor import CKEditor
from flask_share import Share
from flask_migrate import Migrate
from config import DevelopmentConfig

db = SQLAlchemy()
ckeditor = CKEditor()
share = Share()
migrate = Migrate()

def create_app(config=DevelopmentConfig):
	#intial flask app and load config file
	app = Flask(__name__, instance_relative_config=False)
	app.config.from_object("config.DevelopmentConfig")

	#ckeditor intialize in app
	ckeditor.init_app(app)
	
	#social share post on social media
	share.init_app(app)

	from datetime import datetime, timedelta

	#session timeout
	@app.before_request
	def before_request():
		session.permanent = True
		app.permanent_session_lifetime = timedelta(minutes=30)
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
	# migrate application database
	migrate.init_app(app, db)

	with app.app_context():
		db.create_all()

	#Blueprints register
	from .auth import auth as auth_blueprint
	app.register_blueprint(auth_blueprint)

	from .main import main as main_blueprint
	app.register_blueprint(main_blueprint)

	return app