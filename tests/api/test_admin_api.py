import os
import pytest
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")

@pytest.mark.regression
def test_get_all_users_admin(admin_headers):
    """Verify that an admin can get a list of all users."""
    response = requests.get(f"{BASE_URL}/api/admin/users", headers=admin_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.errors_handling
def test_get_all_users_non_admin(auth_headers):
    """Verify that a regular user cannot access the users list."""
    response = requests.get(f"{BASE_URL}/api/admin/users", headers=auth_headers)
    assert response.status_code in [401, 403]

@pytest.mark.regression
def test_ban_and_unban_user(admin_headers):
    """Verify that an admin can ban and unban a user."""
    # First get a user to ban (e.g. the first one)
    users_resp = requests.get(f"{BASE_URL}/api/admin/users", headers=admin_headers)
    users = users_resp.json()
    if not users:
        pytest.skip("No users available to ban")
    
    user_id = users[0]['id']
    
    # Ban
    ban_resp = requests.post(f"{BASE_URL}/api/admin/users/{user_id}/ban", headers=admin_headers)
    assert ban_resp.status_code == 200
    
    # Unban
    unban_resp = requests.post(f"{BASE_URL}/api/admin/users/{user_id}/unban", headers=admin_headers)
    assert unban_resp.status_code == 200

@pytest.mark.sanity
def test_get_admin_settings(admin_headers):
    """Verify admin can get settings."""
    response = requests.get(f"{BASE_URL}/api/admin/settings", headers=admin_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), (dict, list))

@pytest.mark.regression
def test_toggle_recommendations_setting(admin_headers):
    """Verify admin can toggle recommendations setting."""
    # Turn off
    off_resp = requests.put(f"{BASE_URL}/api/admin/settings/recommendations_enabled", json={"value": "false"}, headers=admin_headers)
    assert off_resp.status_code == 200
    
    # Turn on
    on_resp = requests.put(f"{BASE_URL}/api/admin/settings/recommendations_enabled", json={"value": "true"}, headers=admin_headers)
    assert on_resp.status_code == 200

@pytest.mark.sanity
def test_get_blacklist(admin_headers):
    """Verify admin can get blacklist."""
    response = requests.get(f"{BASE_URL}/api/admin/blacklist", headers=admin_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.regression
def test_blacklist_add_and_remove(admin_headers):
    """Verify admin can add and remove an email from the blacklist."""
    email = "test-blacklist-123@svcollege.co.il"
    
    # Add to blacklist
    add_resp = requests.post(f"{BASE_URL}/api/admin/blacklist", json={"email": email}, headers=admin_headers)
    assert add_resp.status_code == 201
    entry_id = add_resp.json().get("id") or add_resp.json().get("entry_id")
    
    # Verify we got an ID back
    assert entry_id is not None
    
    # Remove from blacklist (Cleanup)
    # The endpoint might be DELETE /api/admin/blacklist/{entry_id}
    del_resp = requests.delete(f"{BASE_URL}/api/admin/blacklist/{entry_id}", headers=admin_headers)
    # The spec in Postman mentions DELETE /api/admin/blacklist/{entry_id}
    # It doesn't explicitly test the DELETE, but we can assume 200 or 204
    assert del_resp.status_code in [200, 204]

@pytest.mark.errors_handling
def test_non_admin_cannot_blacklist(auth_headers):
    """Verify standard user gets 401/403 when trying to blacklist."""
    response = requests.post(f"{BASE_URL}/api/admin/blacklist", json={"email": "hacked@test.com"}, headers=auth_headers)
    assert response.status_code in [401, 403]
