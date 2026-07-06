import pytest
import os
from .validators import validate_url, validate_text_content, validate_element_hidden

BASE_URL = os.getenv("BASE_URL")

@pytest.mark.errors_handling
def test_admin_page_access_denied_for_regular_user(auth_page):
    """
    Verify that a standard user cannot access the admin system page.
    Validates: The 'System' link is not visible, and navigating directly redirects away or shows an error.
    """
    # Verify the 'System' link is not visible in navigation
    validate_element_hidden(auth_page, "text='System'")
    
    # Try navigating directly
    auth_page.goto(f"{BASE_URL}/pages/admin.html")
    
    # Should redirect back to home or show access denied
    # Let's assume it redirects to home based on standard implementation
    auth_page.wait_for_url(f"{BASE_URL}/pages/home.html")
    validate_url(auth_page, f"{BASE_URL}/pages/home.html")
