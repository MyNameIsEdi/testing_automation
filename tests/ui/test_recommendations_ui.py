import pytest
import os
import uuid
from .pages.home_page import HomePage
from .pages.recommendation_page import RecommendationPage, AddRecommendationPage
from .validators import validate_url, validate_text_content

BASE_URL = os.getenv("BASE_URL")

@pytest.mark.sanity
def test_add_recommendation_success(auth_page):
    """
    Verify that an authenticated user can add a recommendation successfully.
    """
    home_page = HomePage(auth_page)
    home_page.go_to_add_recommendation()
    
    validate_url(auth_page, f"{BASE_URL}/pages/add-recommendation.html")
    
    add_page = AddRecommendationPage(auth_page)
    unique_name = f"Test Movie {uuid.uuid4().hex[:6]}"
    
    add_page.add_recommendation(
        category="Movie",
        name=unique_name,
        your_name="Automated Tester",
        desc="A great automated recommendation"
    )
    
    # Wait for redirect back to home page
    auth_page.wait_for_url(f"{BASE_URL}/pages/home.html")
    validate_url(auth_page, f"{BASE_URL}/pages/home.html")
    
    # We could optionally validate that the new recommendation appears in the list

@pytest.mark.errors_handling
def test_add_recommendation_missing_fields(auth_page):
    """
    Verify validation when adding a recommendation with missing required fields.
    """
    home_page = HomePage(auth_page)
    home_page.go_to_add_recommendation()
    
    add_page = AddRecommendationPage(auth_page)
    # Leave name empty
    add_page.add_recommendation(
        category="Book",
        name="",
        your_name="Automated Tester"
    )
    
    # Check for HTML5 required validation or JS error (Assuming JS error message as per SRS)
    validate_text_content(auth_page, ".error-message", "Recommendation name is required.") # Adjust selector

@pytest.mark.regression
def test_add_comment(auth_page):
    """
    Verify that an authenticated user can add a comment to a recommendation.
    """
    home_page = HomePage(auth_page)
    
    # Wait for recommendations to load
    home_page.wait_for_selector(home_page.recommendation_cards)
    
    # Click on the first recommendation
    auth_page.locator(home_page.recommendation_cards).first.click()
    
    rec_page = RecommendationPage(auth_page)
    
    comment_text = f"Great recommendation! {uuid.uuid4().hex[:6]}"
    rec_page.fill(rec_page.comment_input, comment_text)
    
    # Assuming there's a 5 star rating, clicking the 5th star
    # Note: DOM might differ, assuming standard implementation
    auth_page.locator(rec_page.star_rating).locator("span").nth(4).click()
    
    rec_page.click(rec_page.submit_comment_btn)
    
    # Validate comment appears on the page
    validate_text_content(auth_page, f"text='{comment_text}'", comment_text)
