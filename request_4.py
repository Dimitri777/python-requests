import requests

# Upload an image to the pet store

# Endpoint URL
url = "https://petstore.swagger.io/v2/pet/101/uploadImage"

# Set the api_key in the header as required by the API
headers = {
    "api_key": "special-key"
}

# Open the file and send it as multipart/form-data
with open("wolf.jpg", "rb") as image_file:
    files = {
        "file": ("wolf.jpg", image_file, "image/jpeg")
    }

    response = requests.post(
        url=url,
        headers=headers,
        files=files
    )

print(f"Status Code: {response.status_code}")
print(f"Response Body: {response.text}")
