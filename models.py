from app import application
from flask_sqlalchemy import SQLAlchemy

application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/BookStoreDatabase.db'
db = SQLAlchemy(application)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_name = db.Column(db.String(120), index=True)
	email_address = db.Column(db.String(120), index=True, unique=True)
	password_hash = db.Column(db.String(120))
	address = db.Column(db.String(300))
	phone = db.Column(db.Integer)

	def __repr__(self):
		return '<User %r>' % (self.user_name)

	def __init__(self, username, email_address, password_hash):
		self.user_name = username
		self.email_address = email_address
		self.password_hash = password_hash
	
	def serialize(self):
		dict = {}
		dict['user_name'] = self.user_name
		dict['email_address'] = self.email_address
		dict['address'] = self.address
		dict['phone'] = self.phone
		return dict
