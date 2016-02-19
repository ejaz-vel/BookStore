from flask import Flask, jsonify, request, abort
from flask import make_response

import models

application = Flask(__name__)

@application.route('/BookStore/v1.0/User/<int:user_id>', methods=['GET'])
def index(user_id):
	user = models.User.query.filter_by(id=user_id).first()
	if user is None:
		abort(404)
	else:
		return jsonify({'users': user.serialize()}), 200

@application.route('/BookStore/v1.0/User', methods=['POST'])
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
		user.address = request.json['address']
		user.phone = int(request.json['phone'])
		models.db.session.add(user)
		models.db.session.commit()
		return jsonify({'users': user.serialize()}), 201

@application.errorhandler(404)
def not_found(error):
	    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
	application.run(host='0.0.0.0', port=80, debug=True)
