import os
import pytest
import requests

BASE_URL = os.getenv("BASE_URL")
TEST_USER_EMAIL = os.getenv("TEST_USER_EMAIL")
TEST_USER_PASSWORD = os.getenv("TEST_USER_PASSWORD")

@pytest.mark.sanity
def test_login_success():
    """
    Verify that a user can successfully log in and receive a valid access token and user details.
    Validates: Status code 200, Response body contains 'access_token' and correct 'email'.
    """
    payload = {
        "email": TEST_USER_EMAIL,
        "password": TEST_USER_PASSWORD
    }
    response = requests.post(f"{BASE_URL}/auth/login", json=payload)
    
    # ולידציה לסטטוס
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"
    
    # ולידציה לתוכן התשובה (Response Body)
    body = response.json()
    assert "access_token" in body, "Response body missing 'access_token'"
    assert isinstance(body["access_token"], str) and len(body["access_token"]) > 0
    assert "id" in body, "Response body missing 'id'"
    assert body["email"] == payload["email"], f"Expected email {payload['email']}, got {body.get('email')}"

@pytest.mark.errors_handling
@pytest.mark.parametrize("email, password, expected_status", [
    ("wrong@email.com", TEST_USER_PASSWORD, 401),  # אימייל שגוי
    (TEST_USER_EMAIL, "WrongPass123", 401),        # סיסמה שגויה
    ("", "", 422)                                  # שדות ריקים (Validation Error)
])
def test_login_negative_scenarios(email, password, expected_status):
    """
    Verify login failures with invalid credentials or missing fields using Parameterization.
    Validates: Correct error status codes (401/422) and ensures no token is returned.
    """
    payload = {"email": email, "password": password}
    response = requests.post(f"{BASE_URL}/auth/login", json=payload)
    
    assert response.status_code == expected_status, f"Expected {expected_status}, got {response.status_code}"
    
    body = response.json()
    assert "access_token" not in body, "Access token should not be returned on a failed login"

@pytest.mark.sanity
def test_get_profile(auth_headers):
    """
    Verify that an authenticated user can fetch their profile details.
    Uses the 'auth_headers' fixture to automatically pass the Bearer token.
    Validates: Status code 200, Profile email matches the authenticated user's email.
    """
    response = requests.get(f"{BASE_URL}/api/profile/me", headers=auth_headers)
    
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"
    
    body = response.json()
    assert isinstance(body, dict), "Response body should be a JSON object"
    assert body.get("email") == TEST_USER_EMAIL, "Profile email mismatch"

@pytest.mark.regression
def test_rbac_admin_only_endpoint(admin_headers, auth_headers):
    """
    Verify RBAC (Role-Based Access Control) for an Admin-only endpoint.
    Validates: Admin gets 200 with a list, Standard user gets 401/403.
    """
    endpoint = f"{BASE_URL}/api/admin/users"
    
    # בדיקת קריאה עם הרשאות אדמין (Positive)
    admin_resp = requests.get(endpoint, headers=admin_headers)
    assert admin_resp.status_code == 200, f"Admin should get 200 OK, got {admin_resp.status_code}"
    assert isinstance(admin_resp.json(), list), "Admin response should return a list of users"
    
    # בדיקת קריאה עם הרשאות משתמש רגיל (Negative)
    user_resp = requests.get(endpoint, headers=auth_headers)
    assert user_resp.status_code in [401, 403], f"Standard user should be forbidden (401/403), got {user_resp.status_code}"