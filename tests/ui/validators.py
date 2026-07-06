from playwright.sync_api import expect, Page

def validate_url(page: Page, expected_url: str):
    """Validates that the current page URL matches the expected URL."""
    expect(page).to_have_url(expected_url)

def validate_element_visible(page: Page, selector: str):
    """Validates that a specific element is visible on the page."""
    expect(page.locator(selector)).to_be_visible()

def validate_text_content(page: Page, selector: str, expected_text: str):
    """Validates that a specific element contains the expected text."""
    expect(page.locator(selector)).to_have_text(expected_text)

def validate_element_hidden(page: Page, selector: str):
    """Validates that a specific element is not visible on the page."""
    expect(page.locator(selector)).to_be_hidden()
