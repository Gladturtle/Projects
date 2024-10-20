import requests

request = requests.post('http://127.0.0.1:5000/random_image')
print(request.json())