from flask import Flask, jsonify, request, abort
from flask import make_response
import math
from collections import Counter
# flask is a package, and Flask, jsonify, request etc are all the classes inside this package.

import models

# imoorting the package models.
application = Flask(__name__)


# creating the get api for the user.
# this is to retrieve the details of the user when the user id is inputted.
@application.route('/BookStore/v1.0/User/<int:user_id>', methods=['GET'])
def get_user(user_id):
	user = models.User.query.filter_by(id=user_id).first()
	if user is None:
		abort(404)
	else:
		return jsonify({'user': user.serialize()}), 200

# api to login.
@application.route('/BookStore/v1.0/User/', methods=['GET'])
def login():
	if not 'password_hash' in request.args:
		abort(400)
	# means if the password is not provided by the user then abort the operation.

	passwordHash = request.args['password_hash']
	user = None
	if 'email_address' in request.args:
		emailAddress = request.args['email_address']
		user = models.User.query.filter_by(email_address=emailAddress).first()
	elif 'phone' in request.args:
		phone = request.args['phone']
		user = models.User.query.filter_by(phone=phone).first()
	else:
		abort(400)

	# if user name exist and the password matches means return the json form of the user with status = 200 ie OK.
	if not user is None and user.password_hash == passwordHash:
		return jsonify({'user': user.serialize()}), 200
	else:
		abort(401)

# api which will give the list of recommended books.
@application.route('/BookStore/v1.0/User/Recommend/<int:user_id>', methods=['GET'])
def get_recommended_books(user_id):
	user = models.User.query.filter_by(id=user_id).first()
	if user is None:
		abort(404)
	else:
		books = models.Book.query.all()
		recommendedBooks = []
		count = 0
                if 'latitude' in request.args and 'longitude' in request.args:
                    locDic = {}
                    for book in books:
                        if book.latitude is None and book.longitude is None:
                            continue
                        curLat = float(request.args['latitude'])
                        curLong = float(request.args['longitude'])
                        bookLat = book.latitude
                        bookLong = book.longitude
                        locDic[book] = abs(curLat - bookLat) * abs(curLong - bookLong)
                    for book, dist in reversed(Counter(locDic).most_common(len(locDic))):
                        if count > 5:
                            break;
                        recommendedBooks.append(book.serialize())
                        count += 1
                else:
                    for book in books:
                        if count > 5:
                            break;
			recommendedBooks.append(book.serialize())
			count += 1
		return jsonify({'List': recommendedBooks}), 200

# api to retrieve the details from the orders table:
@application.route('/BookStore/v1.0/Orders/<int:order_id>', methods=['GET'])
def get_orders(order_id):
	orders = models.Orders.query.filter_by(orderId=order_id).first()
	if orders is None:
		abort(400)
	else:
		return jsonify({'order': orders.serialize()}), 200

# api to create a orders entry
@application.route('/BookStore/v1.0/Orders/', methods=['POST'])
def create_orders():
	# the below 2 if conditions means that if these necessary parameters are not present then abort
	if not request.json:
		abort(400)
	elif not 'book_id' in request.json:
		abort(400)
	elif not 'user_id' in request.json:
		abort(400)
	elif not 'price' in request.json:
		abort(400)
	else:
		# the order in which the elements are added like order id, date order , book id all these must be the same as how the schema is established.
		orders = models.Orders(int(request.json['book_id']), int(request.json['user_id']), float(request.json['price']))

		# updating the sold field of the books table.
		book = models.Book.query.filter_by(id=int(request.json['book_id'])).update(dict(sold=True))
		models.db.session.add(orders)
		models.db.session.commit()
		return jsonify({'order': orders.serialize()}), 201

# api to create a user entry.
@application.route('/BookStore/v1.0/User/', methods=['POST'])
def create_user():
	if not request.json:
		abort(400)
	elif not 'user_name' in request.json:
		abort(400)
	elif not 'email_address' in request.json:
		abort(400)
	elif not 'password_hash' in request.json:
		abort(400)
	else:
		# if all the criteria pass, then adddig the field into the user table.
		# these are the compulsory fields: user name , email add, pasword hash
		user = models.User(request.json['user_name'], request.json['email_address'], request.json['password_hash'])
		# the above line is defining the object called "user" of the User class.

		# these fields are optional: address and phone. so if the user is giving these fields also in
		# the request, then we need to set these fields up.
		if 'address' in request.json:
			user.address = request.json['address']
		if 'phone' in request.json:
			# since the json value is string, so typecasting it to integer.
			user.phone = int(request.json['phone'])
		models.db.session.add(user)

		# after every query which updates something in the database, be it add or delete, do commit.
		models.db.session.commit()
		return jsonify({'user': user.serialize()}), 201
	# 201 is the http code for created. always use 201 while doing post method.

# api to create a book entry
@application.route('/BookStore/v1.0/Book/', methods=['POST'])
def create_book():
	if not request.json:
		abort(400)
	elif not 'name' in request.json:
		abort(400)
	elif not 'user_id' in request.json:
		abort(400)
	elif not 'description' in request.json:
		abort(400)
	elif not 'price' in request.json:
		abort(400)
	else:
		book = models.Book(int(request.json['user_id']), request.json['name'], request.json['description'], float(request.json['price']))
		book.sold = False
	# first time the book is added, its sold condition is false.

		if 'author' in request.json:
			book.author = request.json['author'].lower()
	# convertng everything to lower case, so that its a standard while searching or while adding.

		if 'edition' in request.json:
			book.edition = request.json['edition'].lower()

		if 'bidding_allowed' in request.json:
			book.bidding_allowed = bool(request.json['bidding_allowed'])
		else:
			book.bidding_allowed = False

		if 'rent' in request.json:
			book.rent = bool(request.json['rent'])
			book.minimum_period = int(request.json['minimum_period'])
			book.maximum_period = int(request.json['maximum_period'])

		if 'sell' in request.json:
			book.sell = bool(request.json['sell'])

		if 'latitude' in request.json and 'longitude' in request.json:
			book.latitude = float(request.json['latitude'])
			book.longitude = float(request.json['longitude'])

		models.db.session.add(book)
		models.db.session.commit()
		return jsonify({'book': book.serialize()}), 201

# searching a book by a string name which could be author name or book name.
# we want to design search in such a way that we dont want the user to specify whether the string he is typing is the
# name of the book or the name of the author.

# functionalities implemented for search are:
# 1. sort the searched books based on something ( in the below case, we are appending names of book first and then the author names, so while displaying also the book names appear first. the top 10 only are shown
# 2. retrieve only the books which are not sold
# 3. retrieve books even if the string representing the name is misplled(spelling checkers) or have spaces. dont do exact search. do like.(very advanced feature, not implemented currently).

@application.route('/BookStore/v1.0/Book/', methods=['GET'])
def get_books():
	searchString = request.args['queryString'].lower()
	books = []
	# books is a list.

	bookNames = models.Book.query.filter_by(name=searchString, sold=False).all()
	bookAuthor = models.Book.query.filter_by(author=searchString, sold=False).all()
	# filter by query here means that a select statement. sold = false means that only if the book is not sold, then retrieve those books.

	# appending booknames before book author names means that all the booknames will appear first because its a list.
	books.extend(bookNames)
	books.extend(bookAuthor)

	if len(books) == 0:
		abort(404)
	else:
		# result is another list. which containts the maps for each book
		result = []

		# looping over all the books which are there in the books list means having the author name or book name that matches the queryString
		for book in books:
			result.append(book.serialize())

		# finding the number of books in the books list
		numBooks = min(10, len(books))
		# this will retrieve the minimum of the numebr which is there out of 10 znd the number of books retrievd.
		# if the number is more thn 10 then we need to show just the top 10 books retrieved.
		return jsonify(List=result[0:numBooks]), 200

#  that we always respond with JSON, so we need to improve our 404 error handler:
@application.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
	application.run(host='0.0.0.0', port=80, debug=True)
