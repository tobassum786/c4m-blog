from flask_login import UserMixin
import datetime
from . import db


class User(db.Model, UserMixin):
	id = db.Column(db.Integer(), primary_key=True)
	f_name = db.Column(db.String(30), nullable=False)
	l_name = db.Column(db.String(30), nullable=False)
	username = db.Column(db.String(50), unique=True, nullable=False)
	email = db.Column(db.String(100), unique=True, nullable=False)
	password = db.Column(db.String(256), unique=True, nullable=False)
	image_file = db.Column(db.String(50), nullable=True, default='default.jpg')
	user_active = db.Column(db.DateTime, default=datetime.datetime.utcnow)

	#link with other tables
	posts = db.relationship("Post", backref="author", lazy=True)
	comments = db.relationship("Comment", backref="user_comments", lazy=True)


	def __repr__(self):
		return f"User('{self.username}','{self.email}', '{self.password}')"

	# Generate and check the hash password function
	def generate_password(self, password):
		return generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password, password)

  

class Post(db.Model):
	id = db.Column(db.Integer(), primary_key=True)
	title = db.Column(db.String(200), nullable=False)
	sub_title = db.Column(db.String(150), nullable=False)
	posted_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
	image_file = db.Column(db.String(50), nullable=True, default='default.jpg')
	post_content = db.Column(db.VARCHAR, nullable=False)
	# relation with user table
	user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
	comments = db.relationship("Comment", backref="post_comments", lazy=True)

	def __repr__(self):
		return f"('{self.title}', '{self.sub_title}', '{self.posted_date}')"

class Comment(db.Model):
	id = db.Column(db.Integer(), primary_key=True)
	posted_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
	content = db.Column(db.VARCHAR, nullable=False)

	# referecing
	post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

	def __repr__(self):
		return f"('{self.content}')"



