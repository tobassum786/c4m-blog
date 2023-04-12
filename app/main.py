from flask import Flask, Blueprint, render_template, url_for, request, session, redirect, send_from_directory, flash
from . import db
from .models import User, Post
from flask_login import LoginManager, current_user, login_user, logout_user, login_required, UserMixin
from flask_ckeditor import *
import os
import secrets

main = Blueprint('main', __name__)

app = Flask(__name__)
upload_path = os.path.join('static', 'images/upload')


#home feed page
@main.route('/')
def index():

	posts = Post.query.all()

	return render_template('index.html', posts=posts)


#profile route
@main.route('/profile', methods=['POST', 'GET'])
@login_required
def profile():
	user_data = User.query.all()
	# get information from profile
	if request.method == "POST":
		current_user.username = request.form['username']
		current_user.email = request.form['email']
		current_user.image_file = request.files['file']
		db.session.commit()
		flash("update successfully")

		return redirect(url_for('main.profile'))
	profile_file = os.path.join(upload_path, current_user.image_file)
	return render_template('profile.html', title='Dashboard', user_data=user_data, image=profile_file)

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

		if post == '':
			flash("Empty content cannot be postes.")
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


#user setting manage profile pictures and password updation
@main.route("/setting")
@login_required
def user_setting():
	pass