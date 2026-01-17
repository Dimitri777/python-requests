"""
Tests for Pet API endpoints
Covers CRUD operations for pets
"""
import requests
import random


def generate_pet_data(pet_id=None, name=None, status="available"):
    """Generate data for creating a pet"""
    if pet_id is None:
        pet_id = random.randint(1000, 999999)
    if name is None:
        name = f"TestPet_{pet_id}"
    
    return {
        "id": pet_id,
        "name": name,
        "category": {
            "id": 1,
            "name": "Dogs"
        },
        "photoUrls": [
            "http://example.com/photo1.jpg",
            "http://example.com/photo2.jpg"
        ],
        "tags": [
            {"id": 1, "name": "tag1"},
            {"id": 2, "name": "tag2"}
        ],
        "status": status
    }


class TestPetCreation:
    """Tests for creating pets"""
    
    def test_create_pet_success(self, base_url, headers):
        """Test successful pet creation"""
        pet_data = generate_pet_data()
        
        response = requests.post(
            f"{base_url}/pet",
            headers=headers,
            json=pet_data
        )
        
        assert response.status_code == 200, f"Expected status 200, got {response.status_code}: {response.text}"
        response_data = response.json()
        assert response_data["id"] == pet_data["id"]
        assert response_data["name"] == pet_data["name"]
        assert response_data["status"] == pet_data["status"]
        assert response_data["category"]["name"] == pet_data["category"]["name"]
    
    def test_create_pet_with_minimal_data(self, base_url, headers):
        """Test creating a pet with minimal data"""
        minimal_pet = {
            "id": random.randint(1000, 999999),
            "name": "MinimalPet",
            "photoUrls": []
        }
        
        response = requests.post(
            f"{base_url}/pet",
            headers=headers,
            json=minimal_pet
        )
        
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["name"] == minimal_pet["name"]


class TestPetRetrieval:
    """Tests for retrieving pet information"""
    
    def test_get_pet_by_id_success(self, base_url, headers, cleanup_pets):
        """Test successful pet retrieval by ID"""
        # Create a pet
        pet_data = generate_pet_data()
        create_response = requests.post(
            f"{base_url}/pet",
            headers=headers,
            json=pet_data
        )
        assert create_response.status_code == 200
        cleanup_pets.append(pet_data["id"])
        
        # Get the pet
        response = requests.get(
            f"{base_url}/pet/{pet_data['id']}",
            headers=headers
        )
        
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["id"] == pet_data["id"]
        assert response_data["name"] == pet_data["name"]
    
    def test_get_pet_by_id_not_found(self, base_url, headers):
        """Test retrieving a non-existent pet"""
        nonexistent_id = 9999999991
        
        response = requests.get(
            f"{base_url}/pet/{nonexistent_id}",
            headers=headers
        )
        
        assert response.status_code == 404
    
    def test_find_pets_by_status_available(self, base_url, headers):
        """Test finding pets with available status"""
        params = {"status": "available"}
        
        response = requests.get(
            f"{base_url}/pet/findByStatus",
            headers=headers,
            params=params
        )
        
        assert response.status_code == 200
        pets = response.json()
        assert isinstance(pets, list)
        if len(pets) > 0:
            for pet in pets:
                assert pet["status"] == "available"
    
    def test_find_pets_by_status_pending(self, base_url, headers):
        """Test finding pets with pending status"""
        params = {"status": "pending"}
        
        response = requests.get(
            f"{base_url}/pet/findByStatus",
            headers=headers,
            params=params
        )
        
        assert response.status_code == 200
        pets = response.json()
        assert isinstance(pets, list)
        if len(pets) > 0:
            for pet in pets:
                assert pet["status"] == "pending"
    
    def test_find_pets_by_status_sold(self, base_url, headers):
        """Test finding pets with sold status"""
        params = {"status": "sold"}
        
        response = requests.get(
            f"{base_url}/pet/findByStatus",
            headers=headers,
            params=params
        )
        
        assert response.status_code == 200
        pets = response.json()
        assert isinstance(pets, list)
        if len(pets) > 0:
            for pet in pets:
                assert pet["status"] == "sold"
    
    def test_find_pets_by_status_invalid(self, base_url, headers):
        """Test finding pets with invalid status"""
        params = {"status": "invalid_status"}
        
        response = requests.get(
            f"{base_url}/pet/findByStatus",
            headers=headers,
            params=params
        )
        
        # API may return 200 with empty list or 400
        assert response.status_code in [200, 400]
    
    def test_find_pets_by_tags(self, base_url, headers):
        """Test finding pets by tags"""
        params = {"tags": "tag1"}
        
        response = requests.get(
            f"{base_url}/pet/findByTags",
            headers=headers,
            params=params
        )
        
        assert response.status_code == 200
        pets = response.json()
        assert isinstance(pets, list)


class TestPetUpdate:
    """Tests for updating pets"""
    
    def test_update_pet_success(self, base_url, headers, cleanup_pets):
        """Test successful pet update"""
        # Create a pet
        pet_data = generate_pet_data(status="available")
        create_response = requests.post(
            f"{base_url}/pet",
            headers=headers,
            json=pet_data
        )
        assert create_response.status_code == 200
        cleanup_pets.append(pet_data["id"])
        
        # Update the pet
        pet_data["name"] = "UpdatedPetName"
        pet_data["status"] = "sold"
        
        update_response = requests.put(
            f"{base_url}/pet",
            headers=headers,
            json=pet_data
        )
        
        assert update_response.status_code == 200
        updated_pet = update_response.json()
        assert updated_pet["name"] == "UpdatedPetName"
        assert updated_pet["status"] == "sold"
    
    def test_update_pet_with_form_data(self, base_url, headers, cleanup_pets):
        """Test updating pet via form data"""
        # Create a pet
        pet_data = generate_pet_data()
        create_response = requests.post(
            f"{base_url}/pet",
            headers=headers,
            json=pet_data
        )
        assert create_response.status_code == 200
        cleanup_pets.append(pet_data["id"])
        
        # Update via form data
        form_data = {
            "name": "FormUpdatedName",
            "status": "pending"
        }
        
        response = requests.post(
            f"{base_url}/pet/{pet_data['id']}",
            data=form_data
        )
        
        assert response.status_code == 200
        
        # Verify the update
        get_response = requests.get(
            f"{base_url}/pet/{pet_data['id']}",
            headers=headers
        )
        assert get_response.status_code == 200
        updated_pet = get_response.json()
        assert updated_pet["name"] == "FormUpdatedName"
        assert updated_pet["status"] == "pending"


class TestPetDeletion:
    """Tests for deleting pets"""
    
    def test_delete_pet_success(self, base_url, headers, api_key_headers):
        """Test successful pet deletion"""
        # Create a pet
        pet_data = generate_pet_data()
        create_response = requests.post(
            f"{base_url}/pet",
            headers=headers,
            json=pet_data
        )
        assert create_response.status_code == 200
        
        # Delete the pet
        delete_response = requests.delete(
            f"{base_url}/pet/{pet_data['id']}",
            headers=api_key_headers
        )
        
        assert delete_response.status_code == 200
        
        # Verify that the pet is deleted
        get_response = requests.get(
            f"{base_url}/pet/{pet_data['id']}",
            headers=headers
        )
        assert get_response.status_code == 404
    
    def test_delete_nonexistent_pet(self, base_url, api_key_headers):
        """Test deleting a non-existent pet"""
        nonexistent_id = 9999999991
        
        response = requests.delete(
            f"{base_url}/pet/{nonexistent_id}",
            headers=api_key_headers
        )
        
        # API may return 404 or 400
        assert response.status_code in [400, 404]
    
    def test_delete_pet_without_api_key(self, base_url, headers, cleanup_pets):
        """Test deleting a pet without API key"""
        # Create a pet
        pet_data = generate_pet_data()
        create_response = requests.post(
            f"{base_url}/pet",
            headers=headers,
            json=pet_data
        )
        assert create_response.status_code == 200
        cleanup_pets.append(pet_data["id"])
        
        # Try to delete without API key
        response = requests.delete(
            f"{base_url}/pet/{pet_data['id']}",
            headers=headers
        )
        
        # Some API versions require API key
        assert response.status_code in [200, 400, 401]


class TestPetNegativeCases:
    """Negative tests for Pet API"""


    def test_get_pet_with_invalid_id_format(self, base_url, headers):
        """Test retrieving a pet with invalid ID format"""
        response = requests.get(
            f"{base_url}/pet/invalid_id",
            headers=headers
        )
        
        assert response.status_code in [400, 404, 405]
    
    def test_update_nonexistent_pet(self, base_url, headers):
        """Test updating a non-existent pet"""
        nonexistent_pet = generate_pet_data(pet_id=999999999)
        
        response = requests.put(
            f"{base_url}/pet",
            headers=headers,
            json=nonexistent_pet
        )
        
        # API may return 404 or 200 (create new)
        assert response.status_code in [200, 404, 400]
