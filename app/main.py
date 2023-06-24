from flask import Flask, Blueprint, render_template, url_for, request, session, redirect, send_from_directory, flash
from . import db
from .models import User, Post
from flask_login import LoginManager, current_user, login_user, logout_user, login_required, UserMixin
from flask_ckeditor import *
import os
import secrets
from PIL import Image
from werkzeug.utils import secure_filename
import uuid


main = Blueprint('main', __name__)

app = Flask(__name__)
UPLOAD_DIR = os.path.join('static', './images/upload')
app.config['UPLOAD_DIR'] = UPLOAD_DIR

#home feed page
@main.route('/')
def index():

	posts = Post.query.all()

	return render_template('index.html', posts=posts)

#profile route
@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
	if request.method == "POST":
		username = request.form['username']
		email = request.form['email']
		#Profile image upload by user
		profile_image = request.files['file']

		if profile_image:
			random_hex = secrets.token_hex(8)
			_,f_ext = os.path.splitext(profile_image.filename)
			f_name = random_hex + f_ext
			profile_image.save(os.path.join(app.config['UPLOAD_DIR'], f_name))

		user_id = current_user.id
		user.profile_image = f_name
		db.session.add(profile_image)
		db.session.commit()

		return redirect(url_for('main.profile'))
	return render_template('profile.html')

#post page
@main.route("/post/<int:post_id>")
def post(post_id):
	one_post = Post.query.filter_by(id=post_id).one()
	return render_template('post.html', title="Post", one_post=one_post)

#create a new post
@main.route("/new_post", methods=['POST', 'GET'])
@login_required
def new_post():
	if request.method == "POST":

		title = request.form['title']
		sub_title = request.form['sub_title']
		post_content = request.form['ckeditor']
		user_id = current_user.id


		post = Post(title=title, sub_title=sub_title, post_content=post_content, user_id=user_id)

		if post_content == '':
			flash("Empty content cannot be posted.")
			return redirect(url_for('main.new_post'))

		db.session.add(post)
		db.session.commit()

		return redirect(url_for('main.index'))

	return render_template('new-post.html', title="New post")


#Delete post from db and home page
@main.route("/delete-post/<int:post_id>")
def delete_post(post_id):
	pass

#Re-edit existed post
@main.route("/edit-post/<int:post_id>")
def edit_post(post_id):
	pass

