import requests
import unittest

from db import con


def post_test(*args, **kwargs):
	return requests.post(*args, **kwargs).json()



class RESTApiTestPost(unittest.TestCase):
	def test_null_post(self):
		response = post_test('http://localhost:5000/api/v1/users', json={}, headers={'Content-Type': 'application/json'})
		self.assertEqual(response['success'], 'OK')

	def test_post_with_data(self):
		response = post_test('http://localhost:5000/api/v1/users', json={'login': 'dudavik'}, headers={'Content-Type': 'application/json'})
		self.assertEqual(response['success'], 'OK')

	def test_post_with_many_data(self):
		response = post_test('http://localhost:5000/api/v1/users', json={'login': 'dudavik', 'ginger': 123}, headers={'Content-Type': 'application/json'})
		self.assertEqual(response['success'], 'OK')


class RESTApiTestGet(unittest.TestCase):
	def test_get(self):
		response = requests.get('http://localhost:5000/api/v1/users').json()
		self.assertTrue(response['users_count'] >= 0)

	def test_many_get(self):
		with con:
			con.execute('DELETE FROM User')	
		for _ in range(3):
			post_test('http://localhost:5000/api/v1/users', json={'login': 'dudavik', 'ginger': 123}, headers={'Content-Type': 'application/json'})
		response = requests.get('http://localhost:5000/api/v1/users').json()
		self.assertEqual(response['users_count'], 3)


if __name__ == '__main__':
	with con:
		con.execute('DELETE FROM User')
	unittest.main()
