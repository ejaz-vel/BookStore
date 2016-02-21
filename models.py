from app import application
from flask_sqlalchemy import SQLAlchemy

application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/BookStoreDatabase.db'
db = SQLAlchemy(application)

class Location:
	latitude = 0.0
	longitude = 0.0
	def __init__(self, latitude, longitude):
		self.latitude = latitude
		self.longitude = longitude

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_name = db.Column(db.String(120), index=True, unique=True)
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
		dict['id'] = self.id
		dict['user_name'] = self.user_name
		dict['email_address'] = self.email_address
		dict['address'] = self.address
		dict['phone'] = self.phone
		return dict

class Book(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	name = db.Column(db.String(120), index=True)
	author = db.Column(db.String(120), index=True)
	edition = db.Column(db.String(60))
	sold = db.Column(db.Boolean, index=True)
	bidding_allowed = db.Column(db.Boolean)
	description = db.Column(db.String(1000))
	latitude = db.Column(db.Float(10))
	longitude = db.Column(db.Float(10))

	def __repr__(self):
		return '<Book %r>' % (self.name)

	def __init__(self, user_id, name, description):
		self.user_id = user_id
		self.name = name
		self.description = description
	
	def serialize(self):
		dict = {}
		dict['user_id'] = self.user_id
		dict['name'] = self.name
		dict['edition'] = self.edition
		dict['author'] = self.author
		dict['sold'] = self.sold
		dict['bidding_allowed'] = self.bidding_allowed
		dict['description'] = self.description
		if not self.latitude is None or not self.longitude is None:
			locDict = {}
			locDict['longitude'] = self.longitude
			locDict['latitude'] = self.latitude
			dict['location'] = locDict
		return dict
