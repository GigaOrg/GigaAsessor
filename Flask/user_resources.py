from flask import jsonify
from flask_restful import reqparse, abort, Resource
from db import con
from loguru import logger

def abort_if_user_not_found(user_id):
	abort(404, message=f'User {user_id} not found')

class UserResource(Resource):
	pass


class UserListResource(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('login')

	def get(self):
		with con:
			users_count = con.execute('SELECT COUNT(*) FROM User').fetchone()[0]
		return jsonify({
			'success': 'OK',
			'users_count': users_count
		})

	def post(self):
		args = self.parser.parse_args()
		with con:
			sql = 'INSERT INTO User (login) VALUES (?)'
			data = (args['login'], )
			con.execute(sql, data)
		return jsonify({
			'success': 'OK'
		})
			