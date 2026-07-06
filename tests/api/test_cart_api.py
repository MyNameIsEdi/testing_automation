import os
import pytest
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")

@pytest.fixture
def auth_headers(auth_headers):
    # This is slightly redundant but reusing the fixture from conftest
    return auth_headers

@pytest.mark.sanity
def test_get_cart(auth_headers):
    """Verify that an authenticated user can get their cart."""
    response = requests.get(f"{BASE_URL}/api/cart", headers=auth_headers)
    assert response.status_code == 200
    
    body = response.json()
    assert isinstance(body, dict)

@pytest.mark.regression
def test_update_cart(auth_headers):
    """Verify that a user can update their cart."""
    # Assuming cart items payload is a list of objects or a specific dictionary format.
    # The Postman export was truncated, let's assume a standard schema format or empty.
    # Typically PUT /api/cart updates the whole cart items.
    payload = {
        "items": []
    }
    response = requests.put(f"{BASE_URL}/api/cart", json=payload, headers=auth_headers)
    assert response.status_code == 200

@pytest.mark.errors_handling
def test_cart_no_auth():
    """Verify that unauthenticated user cannot access cart."""
    response = requests.get(f"{BASE_URL}/api/cart")
    assert response.status_code in [401, 403, 422]
