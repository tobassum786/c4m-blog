from flask import Flask, Blueprint, render_template, url_for, request, session, redirect, send_from_directory, flash
from . import db
from .models import User, Post
from flask_login import LoginManager, current_user, login_user, logout_user, login_required, UserMixin
from flask_ckeditor import *
import os
import secrets
from PIL import Image
from werkzeug.utils import secure_filename

main = Blueprint('main', __name__)

app = Flask(__name__)
UPLOAD_DIR = os.path.join('static', 'images/upload')
app.config['UPLOAD_DIR'] = UPLOAD_DIR


#home feed page
@main.route('/')
def index():

	posts = Post.query.all()

	return render_template('index.html', posts=posts)

#new user profile image upload
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
	i.replace(image_path)

	return image_name

#profile route
@main.route('/profile', methods=['POST', 'GET'])
@login_required
def profile():
	id = current_user.id
	user_data = User.query.get_or_404(id)
	# get information from database and update with new data
	if request.method == "POST":
		user_data.username = request.form['username']
		user_data.email = request.form['email']
		image_file = request.files['file']

		filename = secure_filename(image_file.filename)
		image_file.save(app.config['UPLOAD_DIR'], filename)

		user_data.image_file = filename
		filename.save()
		db.session.commit()
		return redirect(url_for('main.profile'))
	return render_template('profile.html', title='Dashboard', user_data=user_data)

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

