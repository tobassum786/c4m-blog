from flask import Blueprint, render_template, url_for, request, session, redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, current_user, login_user, logout_user, login_required, UserMixin
from .models import User
from . import db

auth = Blueprint('auth', __name__)

#login route
@auth.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':

		username = request.form['username']
		password = request.form['password']


		user = User.query.filter_by(username=username).first()

		if not user or not check_password_hash(user.password, password):
			flash("username and password wrong")

			return redirect(url_for("auth.login"))

		login_user(user)
		return redirect(url_for("main.index"))


	return render_template("login.html", title='Login')

#register route
@auth.route('/register', methods=['GET', 'POST'])
def register():

	if request.method == 'POST':

		f_name = request.form['f_name']
		l_name = request.form['l_name']
		username = request.form['username']
		email = request.form['email']
		password= generate_password_hash(request.form['password'], method='sha256')

		new_user = User.query.filter_by(username=username).first()

		if new_user:
			flash("Email and username already exist")
			return redirect(url_for("auth.register"))

		new_user = User(f_name=f_name, l_name=l_name, username=username, email=email, password=password)

		db.session.add(new_user)

		db.session.commit()
		
		flash("Account successfully created")
		return redirect(url_for("auth.login"))

	return render_template("register.html", title='Register')


#logout route
@auth.route('/logout')
def logout():
	logout_user()
	return redirect(url_for("auth.login"))

