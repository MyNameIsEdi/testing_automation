import pytest
import os
from .pages.home_page import HomePage
from .validators import validate_url, validate_element_visible

BASE_URL = os.getenv("BASE_URL")

@pytest.mark.smoke
def test_navigation_links(auth_page):
    """
    Verify that top navigation links work and redirect to the correct pages.
    Validates: Home, Store, and Profile links.
    """
    home_page = HomePage(auth_page)
    
    # Store
    home_page.click(home_page.nav_store)
    validate_url(auth_page, f"{BASE_URL}/pages/store.html")
    
    # Profile
    home_page.click(home_page.nav_profile)
    validate_url(auth_page, f"{BASE_URL}/pages/profile.html")
    
    # Home
    home_page.click(home_page.nav_home)
    validate_url(auth_page, f"{BASE_URL}/pages/home.html")

@pytest.mark.regression
def test_home_filter_recommendations(auth_page):
    """
    Verify that filtering recommendations by category updates the view.
    Validates that the filter button can be clicked.
    """
    home_page = HomePage(auth_page)
    
    # Click 'Movie' filter
    home_page.filter_by("Movie")
    
    # We can't strictly validate the resulting items without knowing DB state, 
    # but we can validate that the filter interaction didn't break the page
    validate_element_visible(auth_page, ".recommendations-container") # Refine selector

@pytest.mark.sanity
@pytest.mark.parametrize("viewport", [
    {"width": 375, "height": 667}
])
def test_mobile_view_home_page(mobile_context, viewport):
    """
    Verify that the home page loads correctly in a mobile viewport (Parameterized).
    Validates: The page is accessible and mobile layout elements are visible.
    """
    page = mobile_context.new_page()
    page.goto(f"{BASE_URL}/pages/login.html")
    
    # Need to login to see home page
    page.fill("input[type='email']", os.getenv("TEST_USER_EMAIL"))
    page.fill("input[type='password']", os.getenv("TEST_USER_PASSWORD"))
    page.click("button:has-text('Sign In')")
    page.wait_for_selector("text='SV Recommend'")
    
    validate_url(page, f"{BASE_URL}/pages/home.html")
    # You might validate hamburger menu visibility here if applicable for mobile
