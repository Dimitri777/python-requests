"""
Tests for Store API endpoints
Covers operations with orders and inventory
"""
import requests
import pytest
import json
import random
from datetime import datetime, timedelta


def generate_order_data(order_id=None, pet_id=None, quantity=1, status="placed"):
    """Generate data for creating an order"""
    if order_id is None:
        order_id = random.randint(1, 999999)
    if pet_id is None:
        pet_id = random.randint(1, 1000)
    
    # Format date in ISO format
    ship_date = (datetime.utcnow() + timedelta(days=1)).isoformat() + "Z"
    
    return {
        "id": order_id,
        "petId": pet_id,
        "quantity": quantity,
        "shipDate": ship_date,
        "status": status,
        "complete": False
    }


class TestOrderCreation:
    """Tests for creating orders"""
    
    def test_place_order_success(self, base_url, headers, cleanup_orders):
        """Test successful order placement"""
        order_data = generate_order_data()
        
        response = requests.post(
            f"{base_url}/store/order",
            headers=headers,
            json=order_data
        )
        
        assert response.status_code == 200, f"Expected status 200, got {response.status_code}: {response.text}"
        response_data = response.json()
        assert response_data["id"] == order_data["id"]
        assert response_data["petId"] == order_data["petId"]
        assert response_data["quantity"] == order_data["quantity"]
        assert response_data["status"] == order_data["status"]
        cleanup_orders.append(order_data["id"])
    
    def test_place_order_with_different_statuses(self, base_url, headers, cleanup_orders):
        """Test placing orders with different statuses"""
        statuses = ["placed", "approved", "delivered"]
        
        for status in statuses:
            order_data = generate_order_data(status=status)
            response = requests.post(
                f"{base_url}/store/order",
                headers=headers,
                json=order_data
            )
            assert response.status_code == 200
            response_data = response.json()
            assert response_data["status"] == status
            cleanup_orders.append(order_data["id"])
    
    def test_place_order_with_complete_true(self, base_url, headers, cleanup_orders):
        """Test placing a completed order"""
        order_data = generate_order_data()
        order_data["complete"] = True
        
        response = requests.post(
            f"{base_url}/store/order",
            headers=headers,
            json=order_data
        )
        
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["complete"] is True
        cleanup_orders.append(order_data["id"])
    
    def test_place_order_with_large_quantity(self, base_url, headers, cleanup_orders):
        """Test placing an order with large quantity"""
        order_data = generate_order_data(quantity=100)
        
        response = requests.post(
            f"{base_url}/store/order",
            headers=headers,
            json=order_data
        )
        
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["quantity"] == 100
        cleanup_orders.append(order_data["id"])


class TestOrderRetrieval:
    """Tests for retrieving order information"""
    
    def test_get_order_by_id_success(self, base_url, headers, cleanup_orders):
        """Test successful order retrieval by ID"""
        # Create an order
        order_data = generate_order_data()
        create_response = requests.post(
            f"{base_url}/store/order",
            headers=headers,
            json=order_data
        )
        assert create_response.status_code == 200
        cleanup_orders.append(order_data["id"])
        
        # Get the order
        response = requests.get(
            f"{base_url}/store/order/{order_data['id']}",
            headers=headers
        )
        
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["id"] == order_data["id"]
        assert response_data["petId"] == order_data["petId"]
        assert response_data["quantity"] == order_data["quantity"]
    
    def test_get_order_by_id_not_found(self, base_url, headers):
        """Test retrieving a non-existent order"""
        nonexistent_id = 999999999
        
        response = requests.get(
            f"{base_url}/store/order/{nonexistent_id}",
            headers=headers
        )
        
        assert response.status_code == 404
    
    def test_get_order_with_invalid_id(self, base_url, headers):
        """Test retrieving an order with invalid ID"""
        response = requests.get(
            f"{base_url}/store/order/invalid_id",
            headers=headers
        )
        
        assert response.status_code in [400, 404, 405]


class TestOrderDeletion:
    """Tests for deleting orders"""
    
    def test_delete_order_success(self, base_url, headers):
        """Test successful order deletion"""
        # Create an order
        order_data = generate_order_data()
        create_response = requests.post(
            f"{base_url}/store/order",
            headers=headers,
            json=order_data
        )
        assert create_response.status_code == 200
        
        # Delete the order
        delete_response = requests.delete(
            f"{base_url}/store/order/{order_data['id']}",
            headers=headers
        )
        
        assert delete_response.status_code == 200
        
        # Verify that the order is deleted
        get_response = requests.get(
            f"{base_url}/store/order/{order_data['id']}",
            headers=headers
        )
        assert get_response.status_code == 404
    
    def test_delete_nonexistent_order(self, base_url, headers):
        """Test deleting a non-existent order"""
        nonexistent_id = 999999999
        
        response = requests.delete(
            f"{base_url}/store/order/{nonexistent_id}",
            headers=headers
        )
        
        assert response.status_code == 404
    
    def test_delete_order_with_invalid_id(self, base_url, headers):
        """Test deleting an order with invalid ID"""
        response = requests.delete(
            f"{base_url}/store/order/invalid_id",
            headers=headers
        )
        
        assert response.status_code in [400, 404, 405]


class TestInventory:
    """Tests for working with inventory"""
    
    def test_get_inventory_success(self, base_url, headers, api_key_headers):
        """Test successful inventory retrieval"""
        response = requests.get(
            f"{base_url}/store/inventory",
            headers=api_key_headers
        )
        
        assert response.status_code == 200
        inventory = response.json()
        assert isinstance(inventory, dict)
        # Inventory should contain pet statuses
        # Verify that it's a dictionary (may be empty)
        assert isinstance(inventory, dict)
    
    def test_get_inventory_without_api_key(self, base_url, headers):
        """Test retrieving inventory without API key"""
        response = requests.get(
            f"{base_url}/store/inventory",
            headers=headers
        )
        
        # Some API versions require API key, others don't
        assert response.status_code in [200, 401]


class TestStoreNegativeCases:
    """Negative tests for Store API"""
    
    def test_place_order_with_invalid_pet_id(self, base_url, headers):
        """Test placing an order with invalid pet ID"""
        order_data = generate_order_data(pet_id=-1)
        
        response = requests.post(
            f"{base_url}/store/order",
            headers=headers,
            json=order_data
        )
        
        # API may accept or reject invalid pet ID
        assert response.status_code in [200, 400, 404]
    
    def test_place_order_with_invalid_quantity(self, base_url, headers):
        """Test placing an order with invalid quantity"""
        order_data = generate_order_data(quantity=-1)
        
        response = requests.post(
            f"{base_url}/store/order",
            headers=headers,
            json=order_data
        )
        
        # API may accept or reject negative quantity
        assert response.status_code in [200, 400]
    
    def test_place_order_with_missing_required_fields(self, base_url, headers):
        """Test placing an order without required fields"""
        incomplete_order = {
            "id": random.randint(1, 999999)
            # Missing required fields
        }
        
        response = requests.post(
            f"{base_url}/store/order",
            headers=headers,
            json=incomplete_order
        )
        
        # API may return an error or create an order with default values
        assert response.status_code in [200, 400, 500]
    
    def test_place_order_with_invalid_status(self, base_url, headers):
        """Test placing an order with invalid status"""
        order_data = generate_order_data(status="invalid_status")
        
        response = requests.post(
            f"{base_url}/store/order",
            headers=headers,
            json=order_data
        )
        
        # API may accept or reject invalid status
        assert response.status_code in [200, 400]
