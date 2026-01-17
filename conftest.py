"""
Configuration and fixtures for Petstore API tests
"""
import pytest
import requests


# Base API URL
API_BASE_URL = "https://petstore.swagger.io/v2"


@pytest.fixture(scope="session")
def base_url():
    """Base URL for all API requests"""
    return API_BASE_URL


@pytest.fixture(scope="function")
def headers():
    """Base headers for HTTP requests"""
    return {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }


@pytest.fixture(scope="function")
def api_key_headers(headers):
    """Headers with API key for protected endpoints"""
    headers_with_key = headers.copy()
    headers_with_key["api_key"] = "special-key"
    return headers_with_key


@pytest.fixture(scope="function")
def session():
    """HTTP session for connection reuse"""
    session = requests.Session()
    yield session
    session.close()


@pytest.fixture(scope="function")
def cleanup_pets():
    """Fixture for cleaning up created pets after tests"""
    created_pet_ids = []
    yield created_pet_ids
    
    # Cleanup after test
    for pet_id in created_pet_ids:
        try:
            requests.delete(f"{API_BASE_URL}/pet/{pet_id}")
        except Exception:
            pass


@pytest.fixture(scope="function")
def cleanup_orders():
    """Fixture for cleaning up created orders after tests"""
    created_order_ids = []
    yield created_order_ids
    
    # Cleanup after test
    for order_id in created_order_ids:
        try:
            requests.delete(f"{API_BASE_URL}/store/order/{order_id}")
        except Exception:
            pass


@pytest.fixture(scope="function")
def cleanup_users():
    """Fixture for cleaning up created users after tests"""
    created_usernames = []
    yield created_usernames
    
    # Cleanup after test
    for username in created_usernames:
        try:
            requests.delete(f"{API_BASE_URL}/user/{username}")
        except Exception:
            pass
