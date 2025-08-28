import requests

response = requests.post(
    url = "https://petstore.swagger.io/v2/pet",
    headers = {
        "api_key": "special-key",
    },
    json = {
          "id": 101,
          "category": {
            "id": 0,
            "name": "string"
          },
          "name": "Wolf",
          "photoUrls": [
            "string"
          ],
          "tags": [
            {
              "id": 0,
              "name": "dogs"
            }
          ],
          "status": "available"
    }
)
print(response.json())

get_pet_by_id = requests.get(
    url = "https://petstore.swagger.io/v2/pet/101",
    headers = {
        "api_key": "special-key",
    }
)
print(get_pet_by_id.json())