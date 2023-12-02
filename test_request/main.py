import requests

url = 'http://localhost:8000/api-users/users'
response = requests.get(url)
print(response)