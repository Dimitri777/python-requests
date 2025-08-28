import requests


response1 = requests.put(
    url = "https://jsonplaceholder.typicode.com/posts/1",
    json = {
        "title": "TEST TITLE"
    }

)

print(response1.json())

response2 = requests.patch(
    url = "https://jsonplaceholder.typicode.com/posts/2",
    json = {
        "title": "Hey!!!"
    }

)

print(response2.json())