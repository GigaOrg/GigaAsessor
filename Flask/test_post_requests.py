import requests

for _ in range(3):
	requests.post('http://localhost:5000/api/v1/users', json={'login': 'dudavik', 'ginger': 123}, headers={'Content-Type': 'application/json'}).json()
response = requests.get('http://localhost:5000/api/v1/users').json()
print(response)