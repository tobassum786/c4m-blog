from flask import Flask, Blueprint, render_template, url_for, request, session, redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, current_user, login_user, logout_user, login_required, UserMixin
from .models import User
from . import db
from datetime import timedelta
import secrets
from PIL import Image
import os
from werkzeug.utils import secure_filename
from config import DevelopmentConfig


auth = Blueprint('auth', __name__)

app = Flask(__name__)
UPLOAD_DIR=os.path.join('static', 'image/upload')
app.config['UPLOAD_DIR'] = UPLOAD_DIR


#login route
@auth.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':

		username = request.form['username']
		password = request.form['password']


		user = User.query.filter_by(username=username).first()

		if not user or not check_password_hash(user.password, password):
			flash("username and password wrong")
			return redirect(request.url)

		login_user(user)
		return redirect(url_for("main.profile"))

		session.permanent = True

	return render_template("login.html", title='Login')

#save profile images
def save_pic(form_picture):
	random_hex = secrets.token_hex(8)
	_,f_ext = os.path.splitext(form_picture.filename)
	image_name = random_hex + f_ext
	image_path = os.path.join(app.config['UPLOAD_DIR'], image_name)

	# using pillow for resize the image file
	output_size = (125, 125)
	i = Image.open(form_picture)
	i.thumbnail(output_size)
	i.save(image_path)

	return image_name


#register route
@auth.route('/register', methods=['GET', 'POST'])
def register():

	if request.method == 'POST':

		f_name = request.form['f_name']
		l_name = request.form['l_name']
		username = request.form['username']
		email = request.form['email']
		password= generate_password_hash(request.form['password'], method='sha256')
		image_file = save_pic(request.files['file'])


		new_user = User.query.filter_by(username=username).first()

		if new_user:
			flash("Email and username already exist")
			return redirect(url_for("auth.register"))

		new_user = User(f_name=f_name, l_name=l_name, username=username, email=email, password=password, image_file=image_file)

		db.session.add(new_user)

		db.session.commit()
		
		flash("Account successfully created")
		return redirect(url_for("auth.login"))

	return render_template("register.html", title='Register', image_file=image_path)


#logout route
@auth.route('/logout')
def logout():
	logout_user()
	return redirect(url_for("auth.login"))

