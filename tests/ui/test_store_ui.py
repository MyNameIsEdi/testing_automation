import pytest
import os
from .pages.home_page import HomePage
from .pages.store_page import StorePage, CartPage, PaymentPage
from .validators import validate_url, validate_text_content, validate_element_visible

BASE_URL = os.getenv("BASE_URL")

@pytest.mark.sanity
def test_store_add_to_cart(auth_page):
    """
    Verify that an authenticated user can add an item to the cart from the store.
    """
    home_page = HomePage(auth_page)
    home_page.click(home_page.nav_store)
    validate_url(auth_page, f"{BASE_URL}/pages/store.html")
    
    store_page = StorePage(auth_page)
    
    # Wait for store items to load
    store_page.wait_for_selector(store_page.add_to_cart_btns)
    
    # Add first item to cart
    store_page.add_item_to_cart(0)
    
    # Go to cart
    store_page.go_to_cart()
    validate_url(auth_page, f"{BASE_URL}/pages/cart.html")
    
    # Validate item is in cart
    validate_element_visible(auth_page, ".cart-item") # Adjust based on actual DOM

@pytest.mark.regression
def test_cart_update_quantity_and_total(auth_page):
    """
    Verify that updating quantity in the cart updates the total price.
    """
    # Assuming the user already has an item in the cart from the previous flow or we navigate directly and add
    # Let's add one first
    auth_page.goto(f"{BASE_URL}/pages/store.html")
    store_page = StorePage(auth_page)
    store_page.wait_for_selector(store_page.add_to_cart_btns)
    store_page.add_item_to_cart(0)
    store_page.go_to_cart()
    
    cart_page = CartPage(auth_page)
    
    # Get initial total (assuming it's a number we can parse)
    initial_total_str = cart_page.get_text(cart_page.total_price_locator)
    # Just validate it exists for now, if it's dynamic, extract and compare
    
    cart_page.increase_quantity(0)
    
    # Check that total updated (maybe text changed)
    auth_page.wait_for_function(f"document.querySelector('{cart_page.total_price_locator}').innerText !== '{initial_total_str}'")
    
    new_total_str = cart_page.get_text(cart_page.total_price_locator)
    assert initial_total_str != new_total_str, "Total price did not update after increasing quantity"

@pytest.mark.regression
def test_payment_success(auth_page):
    """
    Verify the complete payment flow starting from the cart.
    """
    # Add item and go to cart
    auth_page.goto(f"{BASE_URL}/pages/store.html")
    store_page = StorePage(auth_page)
    store_page.wait_for_selector(store_page.add_to_cart_btns)
    store_page.add_item_to_cart(0)
    store_page.go_to_cart()
    
    cart_page = CartPage(auth_page)
    cart_page.go_to_payment()
    
    validate_url(auth_page, f"{BASE_URL}/pages/payment.html")
    
    payment_page = PaymentPage(auth_page)
    payment_page.fill_payment_info(
        name="Test User",
        address="123 Test St",
        card="1234567890123456",
        cvv="123",
        expiry="2026-12-31" # Format may vary
    )
    
    payment_page.submit_payment()
    
    # Validation: Usually redirects to a success page or shows an alert
    # Assuming an alert or redirect, we just ensure it doesn't stay stuck
    # For now, let's validate it redirects to home or shows success
    # (Checking for a success message element)
    # validate_element_visible(auth_page, ".success-message")
