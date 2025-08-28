import requests

from requests.auth import HTTPBasicAuth

response = requests.get(
    url = "https://petstore.swagger.io/v2/store/inventory",
    headers = {
        "api-key": "special-key"
    }
)

print("Status code:", response.status_code)
response = response.json()
print("JSON response:", response)
print(response["sold"])

responseOfStatus = requests.get(
    url="https://petstore.swagger.io/v2/pet/findByStatus",
    headers={
        "api-key": "special-key"
    },
    params = {
        "status": "sold"
    }
)
print(responseOfStatus.json())
