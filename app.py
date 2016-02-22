from flask import Flask, jsonify, request, abort
from flask import make_response

import models

application = Flask(__name__)

@application.route('/BookStore/v1.0/User/<int:user_id>', methods=['GET'])
def get_user(user_id):
	user = models.User.query.filter_by(id=user_id).first()
	if user is None:
		abort(404)
	else:
		return jsonify({'user': user.serialize()}), 200


@application.route('/BookStore/v1.0/User/Recommend/<int:user_id>', methods=['GET'])
def get_recommended_books(user_id):
	user = models.User.query.filter_by(id=user_id).first()
	if user is None:
		abort(404)
	else:
		books = models.Book.query.all()
		recommendedBooks = []
		count = 0
		for book in books:
			if count > 5:
				break;
			recommendedBooks.append(book.serialize())
			count += 1

		return jsonify({'List': recommendedBooks}), 200

@application.route('/BookStore/v1.0/User/', methods=['GET'])
def login():
	if not 'password_hash' in request.args:
		abort(400)

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

	if not user is None and user.password_hash == passwordHash:
		return jsonify({'user': user.serialize()}), 200
	else:
		abort(401)

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
		user = models.User(request.json['user_name'], request.json['email_address'], request.json['password_hash'])
		if 'address' in request.json:
			user.address = request.json['address']
		if 'phone' in request.json:
			user.phone = int(request.json['phone'])
		models.db.session.add(user)
		models.db.session.commit()
		return jsonify({'user': user.serialize()}), 201

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
	else:
		book = models.Book(int(request.json['user_id']), request.json['name'], request.json['description'], request.json['price'])
		book.sold = False

		if 'author' in request.json:
			book.author = request.json['author'].lower()

		if 'edition' in request.json:
			book.edition = request.json['edition'].lower()

		if 'bidding_allowed' in request.json:
			book.bidding_allowed = request.json['bidding_allowed']
		else:
			book.bidding_allowed = False

		if 'rent' in request.json:
			book.rent = request.json['rent']
			book.minimum_period = int(request.json['minimum_period'])
			book.maximum_period = int(request.json['maximum_period'])

		if 'sell' in request.json:
			book.sell = request.json['sell']

		if 'latitude' in request.json and 'longitude' in request.json:
			book.latitude = float(request.json['latitude'])
			book.longitude = float(request.json['longitude'])

		models.db.session.add(book)
		models.db.session.commit()
		return jsonify({'book': book.serialize()}), 201

@application.route('/BookStore/v1.0/Book/', methods=['GET'])
def get_books():
	books = []
	if 'name' in request.args:
		book_name = request.args['name'].lower()
		books = models.Book.query.filter_by(name=book_name).all()
	elif 'author' in request.args:
		book_author = request.args['author'].lower()
		books = models.Book.query.filter_by(author=book_author).all()
	else:
		abort(404)

	if len(books) == 0:
		abort(404)
	else:
		result = []
		for book in books:
			result.append(book.serialize())
		return jsonify(List = result), 200

@application.errorhandler(404)
def not_found(error):
	    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
	application.run(host='0.0.0.0', port=80, debug=True)
