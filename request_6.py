import requests

session = requests.Session()

response = session.get("http://httpbin.org/cookies/set?freedom=1234567")
print(response.json())

response = session.get("http://httpbin.org/cookies")
print(response.json())