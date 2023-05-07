from flask import Flask, render_template
from flask_restful import Api

from user_resources import UserListResource
from db import db_init, con

app = Flask(__name__)
app.config['DEBUG'] = True

api = Api(app)
api.add_resource(UserListResource, '/api/v1/users')


@app.route('/')
def index():
	return render_template('index.html')


if __name__ == '__main__':
	db_init('db.sqlite')
	print(con)
	app.run('127.0.0.1', 5000)