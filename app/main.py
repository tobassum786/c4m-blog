from flask import Flask, Blueprint, render_template, url_for, request, session, redirect
from . import db
from .models import User, Post
from flask_login import LoginManager, current_user, login_user, logout_user, login_required, UserMixin


main = Blueprint('main', __name__)

#home feed page
@main.route('/')
def index():

	posts = Post.query.all()

	return render_template('index.html', posts=posts)

#profile route
@main.route('/profile')
@login_required
def profile():


	return render_template('profile.html', title='Profile')

#post page
@main.route("/post/<int:post_id>")
def post(post_id):
	one_post = Post.query.filter_by(id=post_id).one()
	return render_template('post.html', title="Post", one_post=one_post)

#create a new post
@main.route("/new_post", methods=['POST', 'GET'])
def new_post():
	if request.method == "POST":

		title = request.form['title']
		sub_title = request.form['sub_title']
		post_content = request.form['post_content']
		user_id = current_user.id

		post = Post(title=title, sub_title=sub_title, post_content=post_content, user_id=user_id)

		db.session.add(post)
		db.session.commit()

		return redirect(url_for('main.post'))

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