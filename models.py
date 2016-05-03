from app import application
from flask_sqlalchemy import SQLAlchemy
import time

application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/BookStoreDatabase.db'
# sqlite:///data/BookStoreDatabase.db this is a file in the data folder
db = SQLAlchemy(application)

class User(db.Model):
	# primary key is by default unique and index= true.
	# index means it becomes easier to search using that field. for eg, for username and email address we are searching based
	# on these 2 fields, means we will do index = true for these fields.
	id = db.Column(db.Integer, primary_key=True)
	user_name = db.Column(db.String(120), index=True, unique=True)
	email_address = db.Column(db.String(120), index=True, unique=True)
	password_hash = db.Column(db.String(120))
	address = db.Column(db.String(300))
	phone = db.Column(db.Integer)

	# this will print the object in python with just user name. we can written anything we want.
	def __repr__(self):
		return '<User %r>' % (self.user_name)

	# init is the name of the constructor in python

	# usernmae emailid and pssword are the necessary parameters which needs to be passed while creating an object
	# self in python is like : this in java.
	def __init__(self, username, email_address, password_hash):
		self.user_name = username
		self.email_address = email_address
		self.password_hash = password_hash

	# for each of the function that we call in python, we need to pass the parameter self.
	# defining the dictionary here.
	def serialize(self):
		dict = {}
		dict['id'] = self.id
		dict['user_name'] = self.user_name
		dict['email_address'] = self.email_address
		dict['address'] = self.address
		dict['phone'] = self.phone
		return dict


class Orders(db.Model):
	orderId = db.Column(db.Integer, primary_key=True)
	dateOrder = db.Column(db.Integer)
	book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	price = db.Column(db.Float)

	def __repr__(self):
		return '<Orders %r>' % (self.orderId)

	def __init__(self, book_id, user_id, price):
		self.book_id = book_id
		self.user_id = user_id
		self.price = price
		self.dateOrder = time.strftime("%d/%m/%Y")

	# the date order is generated in string format. it gets initialisd automatically. we dont need to pass this detail.

	def serialize(self):
		dict = {}
		dict['orderId'] = self.orderId
		dict['dateOrder'] = self.dateOrder
		dict['book_id'] = self.book_id
		dict['user_id'] = self.user_id
		dict['price'] = self.price
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
	price = db.Column(db.Float(10))
	rent = db.Column(db.Boolean, index=True)
	sell = db.Column(db.Boolean, index=True)
	minimum_period = db.Column(db.Integer)
	maximum_period = db.Column(db.Integer)
        condition = db.Column(db.Float(10))

	def __repr__(self):
		return '<Book %r>' % (self.name)

	def __init__(self, user_id, name, description, price):
		self.user_id = user_id
		self.name = name.lower()
		self.description = description
		self.price = price

	def serialize(self):
		dict = {}
		dict['user_id'] = self.user_id
		dict['name'] = self.name
		dict['edition'] = self.edition
		dict['author'] = self.author
		dict['sold'] = self.sold
		dict['bidding_allowed'] = self.bidding_allowed
		dict['description'] = self.description
		dict['rent'] = self.rent
		dict['sell'] = self.sell
                dict['price'] = self.price
                dict['condition'] = self.condition

		if not self.latitude is None and not self.longitude is None:
			dict['longitude'] = self.longitude
			dict['latitude'] = self.latitude
		if not self.rent is None and self.rent is True:
			dict['minimum_period'] = self.minimum_period
			dict['maximum_period'] = self.maximum_period
		return dict


class Bids(db.Model):
	bid_id = db.Column(db.Integer, primary_key=True)
	book_id = db.Column(db.Integer, db.ForeignKey('book.id'),index = True)
	user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
	bid_value = db.Column(db.Float)

	def __repr__(self):
		return '<Bid %r : %r>' % (self.bid_id, self.bid_value)

	def __init__(self, book_id, user_id, bid_value):
		book_id = self.book_id
		user_id = self.user_id
		bid_value = self.bid_value

	def serialize(self):
		dict = {}
		dict['user_id'] = self.user_id

# to create the db. Create models.py and use the following commands:
# from models import db
# db.create_all()
# tihs creates all the tables from models into db.
