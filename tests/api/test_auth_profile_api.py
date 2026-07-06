import os
import pytest
import requests
import uuid
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
TEST_USER_EMAIL = os.getenv("TEST_USER_EMAIL")
TEST_USER_PASSWORD = os.getenv("TEST_USER_PASSWORD")

@pytest.fixture
def random_email():
    return f"test_{uuid.uuid4().hex[:8]}@example.com"

@pytest.mark.sanity
def test_register_success(random_email):
    """
    Verify that a new user can successfully register.
    Validates: Status code 201, Body matches UserOut schema.
    """
    payload = {
        "name": "Automated Tester",
        "email": random_email,
        "password": TEST_USER_PASSWORD
    }
    response = requests.post(f"{BASE_URL}/auth/register?skip_captcha=true", json=payload)
    assert response.status_code == 201, f"Expected 201 Created, got {response.status_code}"
    
    body = response.json()
    assert "id" in body
    assert body.get("email") == random_email
    assert isinstance(body.get("access_token"), str)

@pytest.mark.errors_handling
def test_register_duplicate_email():
    """
    Verify that registering with an already existing email returns an error.
    """
    payload = {
        "name": "Duplicate User",
        "email": TEST_USER_EMAIL,
        "password": TEST_USER_PASSWORD
    }
    response = requests.post(f"{BASE_URL}/auth/register?skip_captcha=true", json=payload)
    assert 400 <= response.status_code < 500, f"Expected 4xx error for duplicate email, got {response.status_code}"
    
    body = response.json()
    assert "detail" in body or "message" in body or "error" in body, "Expected error details in response"

@pytest.mark.errors_handling
def test_register_missing_required_field(random_email):
    """
    Verify that missing the 'name' field returns 422 Unprocessable Entity.
    """
    payload = {
        "email": random_email,
        "password": TEST_USER_PASSWORD
    }
    response = requests.post(f"{BASE_URL}/auth/register?skip_captcha=true", json=payload)
    assert response.status_code == 422, f"Expected 422 Unprocessable, got {response.status_code}"

@pytest.mark.sanity
def test_login_success():
    """
    Verify that a user can successfully log in and receive a valid access token.
    Validates: Status code 200, Response body contains 'access_token'.
    """
    payload = {
        "email": TEST_USER_EMAIL,
        "password": TEST_USER_PASSWORD
    }
    response = requests.post(f"{BASE_URL}/auth/login", json=payload)
    
    # Create the user if it doesn't exist (test setup behavior)
    if response.status_code != 200:
        requests.post(f"{BASE_URL}/auth/register?skip_captcha=true", json={"name": "Test User", "email": TEST_USER_EMAIL, "password": TEST_USER_PASSWORD})
        response = requests.post(f"{BASE_URL}/auth/login", json=payload)

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"
    
    body = response.json()
    assert "access_token" in body, "Response body missing 'access_token'"
    assert isinstance(body["access_token"], str) and len(body["access_token"]) > 0

@pytest.mark.errors_handling
def test_login_wrong_password():
    """
    Verify login failures with invalid password.
    Validates: 401 status code, no access_token returned.
    """
    payload = {"email": TEST_USER_EMAIL, "password": "WRONG_PASSWORD_XYZ"}
    response = requests.post(f"{BASE_URL}/auth/login", json=payload)
    
    assert response.status_code == 401, f"Expected 401, got {response.status_code}"
    assert "access_token" not in response.json()

@pytest.mark.sanity
def test_get_profile(auth_headers):
    """
    Verify that an authenticated user can fetch their profile details.
    """
    response = requests.get(f"{BASE_URL}/api/profile/me", headers=auth_headers)
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"
    
    body = response.json()
    assert isinstance(body, dict), "Response body should be an object"
    if "email" in body:
        assert body["email"] == TEST_USER_EMAIL

@pytest.mark.sanity
def test_get_bearer_token(auth_headers):
    """
    Verify getting the bearer token metadata.
    """
    response = requests.get(f"{BASE_URL}/api/profile/token", headers=auth_headers)
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"
    assert isinstance(response.json(), dict)

@pytest.mark.sanity
def test_password_recover():
    """
    Verify requesting a password reset email.
    """
    payload = {"email": TEST_USER_EMAIL, "redirect_to": ""}
    response = requests.post(f"{BASE_URL}/auth/recover", json=payload)
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"

@pytest.mark.regression
def test_change_password_and_relogin(auth_headers):
    """
    Verify that the user can change their password and log back in with the new password.
    """
    new_password = TEST_USER_PASSWORD + "_new"
    
    # Change password
    payload = {"new_password": new_password}
    change_resp = requests.put(f"{BASE_URL}/api/profile/password", json=payload, headers=auth_headers)
    assert change_resp.status_code == 204, f"Expected 204 No Content, got {change_resp.status_code}"
    
    # Login with new password
    login_payload = {"email": TEST_USER_EMAIL, "password": new_password}
    login_resp = requests.post(f"{BASE_URL}/auth/login", json=login_payload)
    assert login_resp.status_code == 200
    
    # Revert password back (Cleanup)
    new_auth_headers = {"Authorization": f"Bearer {login_resp.json()['access_token']}", "Content-Type": "application/json"}
    requests.put(f"{BASE_URL}/api/profile/password", json={"new_password": TEST_USER_PASSWORD}, headers=new_auth_headers)
