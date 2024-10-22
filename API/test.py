import requests

request = requests.put('http://127.0.0.1:5000/random_image')
print(request.json())