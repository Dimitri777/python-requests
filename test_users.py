"""
Tests for User API endpoints
Covers CRUD operations for users
"""
import requests
import pytest
import json
import random
import string


def generate_username(length=8):
    """Generate a unique username"""
    letters = string.ascii_lowercase
    numbers = string.digits
    return ''.join(random.choice(letters + numbers) for _ in range(length))


def generate_user_data(username=None, user_id=None):
    """Generate data for creating a user"""
    if username is None:
        username = f"testuser_{generate_username()}"
    if user_id is None:
        user_id = random.randint(1, 999999)
    
    return {
        "id": user_id,
        "username": username,
        "firstName": "John",
        "lastName": "Doe",
        "email": f"{username}@example.com",
        "password": "SecurePassword123!",
        "phone": "+1-555-123-4567",
        "userStatus": 1
    }


class TestUserCreation:
    """Tests for creating users"""
    
    def test_create_user_success(self, base_url, headers, cleanup_users):
        """Test successful user creation"""
        user_data = generate_user_data()
        
        response = requests.post(
            f"{base_url}/user",
            headers=headers,
            json=user_data
        )
        
        assert response.status_code == 200, f"Expected status 200, got {response.status_code}: {response.text}"
        cleanup_users.append(user_data["username"])
        
        # Verify that the user is created
        get_response = requests.get(
            f"{base_url}/user/{user_data['username']}",
            headers=headers
        )
        assert get_response.status_code == 200
        created_user = get_response.json()
        assert created_user["username"] == user_data["username"]
        assert created_user["email"] == user_data["email"]
    
    def test_create_user_with_minimal_data(self, base_url, headers, cleanup_users):
        """Test creating a user with minimal data"""
        minimal_user = {
            "id": random.randint(1, 999999),
            "username": f"minimal_{generate_username()}",
            "email": f"minimal_{generate_username()}@example.com"
        }
        
        response = requests.post(
            f"{base_url}/user",
            headers=headers,
            json=minimal_user
        )
        
        assert response.status_code == 200
        cleanup_users.append(minimal_user["username"])
    
    def test_create_users_with_list(self, base_url, headers, cleanup_users):
        """Test creating multiple users via list"""
        users = [
            generate_user_data(username=f"listuser1_{generate_username()}"),
            generate_user_data(username=f"listuser2_{generate_username()}"),
            generate_user_data(username=f"listuser3_{generate_username()}")
        ]
        
        response = requests.post(
            f"{base_url}/user/createWithList",
            headers=headers,
            json=users
        )
        
        assert response.status_code == 200
        
        # Add to cleanup
        for user in users:
            cleanup_users.append(user["username"])
        
        # Verify that users are created
        for user in users:
            get_response = requests.get(
                f"{base_url}/user/{user['username']}",
                headers=headers
            )
            assert get_response.status_code == 200
    
    def test_create_users_with_array(self, base_url, headers, cleanup_users):
        """Test creating multiple users via array"""
        users = [
            generate_user_data(username=f"arrayuser1_{generate_username()}"),
            generate_user_data(username=f"arrayuser2_{generate_username()}")
        ]
        
        response = requests.post(
            f"{base_url}/user/createWithArray",
            headers=headers,
            json=users
        )
        
        assert response.status_code == 200
        
        # Add to cleanup
        for user in users:
            cleanup_users.append(user["username"])


class TestUserRetrieval:
    """Tests for retrieving user information"""
    
    def test_get_user_by_username_success(self, base_url, headers, cleanup_users):
        """Test successful user retrieval by username"""
        # Create a user
        user_data = generate_user_data()
        create_response = requests.post(
            f"{base_url}/user",
            headers=headers,
            json=user_data
        )
        assert create_response.status_code == 200
        cleanup_users.append(user_data["username"])
        
        # Get the user
        response = requests.get(
            f"{base_url}/user/{user_data['username']}",
            headers=headers
        )
        
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["username"] == user_data["username"]
        assert response_data["email"] == user_data["email"]
        assert response_data["firstName"] == user_data["firstName"]
    
    def test_get_user_by_username_not_found(self, base_url, headers):
        """Test retrieving a non-existent user"""
        nonexistent_username = f"nonexistent_{generate_username()}"
        
        response = requests.get(
            f"{base_url}/user/{nonexistent_username}",
            headers=headers
        )
        
        assert response.status_code == 404


class TestUserUpdate:
    """Tests for updating users"""
    
    def test_update_user_success(self, base_url, headers, cleanup_users):
        """Test successful user update"""
        # Create a user
        user_data = generate_user_data()
        create_response = requests.post(
            f"{base_url}/user",
            headers=headers,
            json=user_data
        )
        assert create_response.status_code == 200
        cleanup_users.append(user_data["username"])
        
        # Update the user
        user_data["firstName"] = "Jane"
        user_data["lastName"] = "Smith"
        user_data["email"] = "jane.smith@example.com"
        
        update_response = requests.put(
            f"{base_url}/user/{user_data['username']}",
            headers=headers,
            json=user_data
        )
        
        assert update_response.status_code == 200
        
        # Verify the update
        get_response = requests.get(
            f"{base_url}/user/{user_data['username']}",
            headers=headers
        )
        assert get_response.status_code == 200
        updated_user = get_response.json()
        assert updated_user["firstName"] == "Jane"
        assert updated_user["lastName"] == "Smith"
    
    def test_update_nonexistent_user(self, base_url, headers):
        """Test updating a non-existent user"""
        nonexistent_user = generate_user_data(username=f"nonexistent_{generate_username()}")
        
        response = requests.put(
            f"{base_url}/user/{nonexistent_user['username']}",
            headers=headers,
            json=nonexistent_user
        )
        
        # API may create a new user or return an error
        assert response.status_code in [200, 404]


class TestUserDeletion:
    """Tests for deleting users"""
    
    def test_delete_user_success(self, base_url, headers):
        """Test successful user deletion"""
        # Create a user
        user_data = generate_user_data()
        create_response = requests.post(
            f"{base_url}/user",
            headers=headers,
            json=user_data
        )
        assert create_response.status_code == 200
        
        # Delete the user
        delete_response = requests.delete(
            f"{base_url}/user/{user_data['username']}",
            headers=headers
        )
        
        assert delete_response.status_code == 200
        
        # Verify that the user is deleted
        get_response = requests.get(
            f"{base_url}/user/{user_data['username']}",
            headers=headers
        )
        assert get_response.status_code == 404
    
    def test_delete_nonexistent_user(self, base_url, headers):
        """Test deleting a non-existent user"""
        nonexistent_username = f"nonexistent_{generate_username()}"
        
        response = requests.delete(
            f"{base_url}/user/{nonexistent_username}",
            headers=headers
        )
        
        assert response.status_code == 404


class TestUserLogin:
    """Tests for user login"""
    
    def test_user_login_success(self, base_url, headers, cleanup_users):
        """Test successful user login"""
        # Create a user
        user_data = generate_user_data()
        create_response = requests.post(
            f"{base_url}/user",
            headers=headers,
            json=user_data
        )
        assert create_response.status_code == 200
        cleanup_users.append(user_data["username"])
        
        # Perform login
        params = {
            "username": user_data["username"],
            "password": user_data["password"]
        }
        
        response = requests.get(
            f"{base_url}/user/login",
            headers=headers,
            params=params
        )
        
        assert response.status_code == 200
        response_data = response.json()
        # API returns a message about successful login
        assert "message" in response_data or "logged in" in str(response_data).lower()
    
    def test_user_login_invalid_credentials(self, base_url, headers):
        """Test login with invalid credentials"""
        params = {
            "username": f"invalid_{generate_username()}",
            "password": "wrongpassword"
        }
        
        response = requests.get(
            f"{base_url}/user/login",
            headers=headers,
            params=params
        )
        
        # API may return 200 with error message or 400
        assert response.status_code in [200, 400]
    
    def test_user_login_missing_credentials(self, base_url, headers):
        """Test login without credentials"""
        response = requests.get(
            f"{base_url}/user/login",
            headers=headers
        )
        
        # API may return an error or message
        assert response.status_code in [200, 400]


class TestUserLogout:
    """Tests for user logout"""
    
    def test_user_logout_success(self, base_url, headers):
        """Test successful user logout"""
        response = requests.get(
            f"{base_url}/user/logout",
            headers=headers
        )
        
        assert response.status_code == 200
        response_data = response.json()
        # API returns a message about successful logout
        assert "message" in response_data or "logged out" in str(response_data).lower()


class TestUserNegativeCases:
    """Negative tests for User API"""
    
    def test_create_user_with_invalid_email(self, base_url, headers, cleanup_users):
        """Test creating a user with invalid email"""
        user_data = generate_user_data()
        user_data["email"] = "invalid_email_format"
        
        response = requests.post(
            f"{base_url}/user",
            headers=headers,
            json=user_data
        )
        
        # API may accept or reject invalid email
        assert response.status_code in [200, 400]
        if response.status_code == 200:
            cleanup_users.append(user_data["username"])
    
    def test_create_user_with_duplicate_username(self, base_url, headers, cleanup_users):
        """Test creating a user with duplicate username"""
        user_data = generate_user_data()
        
        # Create the first user
        create_response = requests.post(
            f"{base_url}/user",
            headers=headers,
            json=user_data
        )
        assert create_response.status_code == 200
        cleanup_users.append(user_data["username"])
        
        # Try to create a second user with the same username
        duplicate_user = generate_user_data(username=user_data["username"])
        response = requests.post(
            f"{base_url}/user",
            headers=headers,
            json=duplicate_user
        )
        
        # API may allow or prohibit duplicates
        assert response.status_code in [200, 400, 409]
    
    def test_get_user_with_special_characters(self, base_url, headers):
        """Test retrieving a user with special characters in username"""
        special_username = "user@#$%"
        
        response = requests.get(
            f"{base_url}/user/{special_username}",
            headers=headers
        )
        
        # API may process or return an error
        assert response.status_code in [200, 400, 404]
