import os
import pytest
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")

@pytest.fixture
def created_recommendation(auth_headers):
    """
    Fixture that creates a recommendation before a test and deletes it after.
    Returns the recommendation ID.
    """
    payload = {
        "category": "Book",
        "name": "Test Automation Guide",
        "your_name": "QA Automator",
        "description": "A great book for learning automation",
        "website_url": "https://example.com"
    }
    response = requests.post(f"{BASE_URL}/api/recommendations", json=payload, headers=auth_headers)
    assert response.status_code == 201, "Failed to create setup recommendation"
    rec_id = response.json().get("id")
    
    yield rec_id
    
    # Teardown
    delete_resp = requests.delete(f"{BASE_URL}/api/recommendations/{rec_id}", headers=auth_headers)
    # 200 or 404 is fine (if test already deleted it)

@pytest.mark.sanity
def test_get_all_recommendations():
    """
    Verify that an unauthenticated user can fetch the list of recommendations.
    Validates: Status code 200, Response is a list.
    """
    response = requests.get(f"{BASE_URL}/api/recommendations")
    
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"
    
    body = response.json()
    assert isinstance(body, list), "Response body should be a JSON list"

@pytest.mark.sanity
def test_create_recommendation(auth_headers):
    """
    Verify that an authenticated user can create a new recommendation.
    Validates: Status code 201, Response body contains the created data.
    """
    payload = {
        "category": "Movie",
        "name": "The Matrix",
        "your_name": "Neo",
        "description": "A classic sci-fi movie",
        "website_url": "https://example.com/matrix"
    }
    
    response = requests.post(f"{BASE_URL}/api/recommendations", json=payload, headers=auth_headers)
    
    assert response.status_code == 201, f"Expected 201 Created, got {response.status_code}"
    body = response.json()
    assert "id" in body, "Response body missing 'id'"
    assert body["name"] == payload["name"], "Recommendation name mismatch"
    
    # Cleanup
    requests.delete(f"{BASE_URL}/api/recommendations/{body['id']}", headers=auth_headers)

@pytest.mark.errors_handling
def test_create_recommendation_missing_fields(auth_headers):
    """
    Verify that creating a recommendation with missing required fields fails.
    Validates: Status code 422 (Unprocessable Entity).
    """
    payload = {
        "category": "Movie",
        "your_name": "Neo"
        # Missing 'name' field
    }
    
    response = requests.post(f"{BASE_URL}/api/recommendations", json=payload, headers=auth_headers)
    
    assert response.status_code == 422, f"Expected 422 Unprocessable Entity, got {response.status_code}"

@pytest.mark.regression
def test_get_specific_recommendation(created_recommendation):
    """
    Verify that a specific recommendation can be fetched by ID.
    Validates: Status code 200, returned ID matches requested ID.
    """
    response = requests.get(f"{BASE_URL}/api/recommendations/{created_recommendation}")
    
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"
    body = response.json()
    assert body["id"] == created_recommendation, "Fetched recommendation ID does not match"

@pytest.mark.regression
def test_delete_recommendation(auth_headers, created_recommendation):
    """
    Verify that an authenticated user can delete their own recommendation.
    Validates: Status code 200 on delete, 404 on subsequent get.
    """
    # Delete
    del_response = requests.delete(f"{BASE_URL}/api/recommendations/{created_recommendation}", headers=auth_headers)
    assert del_response.status_code == 200, f"Expected 200 OK, got {del_response.status_code}"
    
    # Verify it's gone
    get_response = requests.get(f"{BASE_URL}/api/recommendations/{created_recommendation}")
    assert get_response.status_code == 404, f"Expected 404 Not Found, got {get_response.status_code}"
