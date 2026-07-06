import pytest
import os
import uuid
from .pages.login_page import LoginPage, RegisterPage
from .validators import validate_url, validate_element_visible, validate_text_content

BASE_URL = os.getenv("BASE_URL")
TEST_USER_EMAIL = os.getenv("TEST_USER_EMAIL")
TEST_USER_PASSWORD = os.getenv("TEST_USER_PASSWORD")

@pytest.mark.sanity
def test_login_success(page):
    """
    Verify that a standard user can successfully log in using the UI.
    Navigates to the login page, enters valid credentials, and validates the redirect to the home page.
    """
    login_page = LoginPage(page)
    login_page.navigate(f"{BASE_URL}/pages/login.html")
    
    login_page.login(TEST_USER_EMAIL, TEST_USER_PASSWORD)
    
    # Validation using functions
    validate_url(page, f"{BASE_URL}/pages/home.html")
    validate_element_visible(page, "text='SV Recommend'")

@pytest.mark.errors_handling
def test_login_invalid_credentials(page):
    """
    Verify that an error message is displayed when entering invalid credentials.
    Navigates to the login page, enters wrong credentials, and validates the error text.
    """
    login_page = LoginPage(page)
    login_page.navigate(f"{BASE_URL}/pages/login.html")
    
    login_page.login("wrong@email.com", "wrongpass123")
    
    # Validation
    validate_text_content(page, ".error-message", "Invalid email or password") # Adjust selector based on actual DOM

@pytest.mark.sanity
def test_register_success(page):
    """
    Verify that a new user can successfully register an account.
    Uses dynamic email to prevent collisions.
    """
    register_page = RegisterPage(page)
    register_page.navigate(f"{BASE_URL}/pages/register.html")
    
    # Generate dynamic email
    random_email = f"test_{uuid.uuid4().hex[:6]}@example.com"
    register_page.register("Automated Test User", random_email, "test1234")
    
    # Assuming it redirects to login or logs in automatically
    # Based on SRS, it might just redirect to login with a success message, or login automatically
    # Let's assume it redirects to login (we will see if it fails)
    validate_url(page, f"{BASE_URL}/pages/login.html")

@pytest.mark.errors_handling
def test_register_password_too_short(page):
    """
    Verify validation error when registering with a password less than 6 characters.
    Validates the specific error message required by the SRS.
    """
    register_page = RegisterPage(page)
    register_page.navigate(f"{BASE_URL}/pages/register.html")
    
    register_page.register("Short Password User", "short@example.com", "12345")
    
    # Validation
    validate_text_content(page, ".error-message", "Password should be at least 6 characters.") # Adjust based on actual DOM
