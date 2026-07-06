import os
import pytest
import requests
from dotenv import load_dotenv

# טעינת משתני סביבה מקובץ .env
load_dotenv()

BASE_URL = os.getenv("BASE_URL")
TEST_USER_NAME = os.getenv("TEST_USER_NAME")
TEST_USER_EMAIL = os.getenv("TEST_USER_EMAIL")
TEST_USER_PASSWORD = os.getenv("TEST_USER_PASSWORD")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

@pytest.fixture(scope="session")
def user_token():
    """
    פיקסטצ'ר שמתחבר למערכת פעם אחת בתחילת הריצה ומחזיר טוקן של משתמש רגיל.
    אם המשתמש לא קיים במסד הנתונים, הוא יוצר אותו (Register) ואז מתחבר.
    """
    payload = {
        "email": TEST_USER_EMAIL,
        "password": TEST_USER_PASSWORD
    }
    # ניסיון התחברות
    response = requests.post(f"{BASE_URL}/auth/login", json=payload)
    
    # אם המשתמש לא קיים (שגיאת 401 או אחרת), ניצור אותו לפי חוקיות האפיון
    if response.status_code != 200:
        requests.post(f"{BASE_URL}/auth/register?skip_captcha=true", json={
            "name": TEST_USER_NAME,
            "email": TEST_USER_EMAIL,
            "password": TEST_USER_PASSWORD
        })
        # התחברות מחדש לאחר ההרשמה
        response = requests.post(f"{BASE_URL}/auth/login", json=payload)
    
    # חילוץ ה-Token מתוך התשובה
    return response.json().get("access_token")

@pytest.fixture(scope="session")
def admin_token():
    """
    פיקסטצ'ר המחזיר טוקן של מנהל (Admin) על בסיס משתמש קיים מראש.
    """
    payload = {
        "email": ADMIN_EMAIL,
        "password": ADMIN_PASSWORD
    }
    response = requests.post(f"{BASE_URL}/auth/login", json=payload)
    return response.json().get("access_token")

@pytest.fixture
def auth_headers(user_token):
    """
    מחזיר את ההדרים (Headers) הדרושים לקריאות API מוגנות כמשתמש רגיל.
    """
    return {
        "Authorization": f"Bearer {user_token}",
        "Content-Type": "application/json",
        "accept": "application/json"
    }

@pytest.fixture
def admin_headers(admin_token):
    """
    מחזיר את ההדרים (Headers) הדרושים לקריאות API מוגנות כאדמין.
    """
    return {
        "Authorization": f"Bearer {admin_token}",
        "Content-Type": "application/json",
        "accept": "application/json"
    }

@pytest.fixture
def auth_page(page):
    """
    Fixture to provide an authenticated UI page using standard user credentials.
    Navigates to the app and performs login.
    """
    page.goto(f"{BASE_URL}/pages/login.html")
    page.fill("input[type='email']", TEST_USER_EMAIL)
    page.fill("input[type='password']", TEST_USER_PASSWORD)
    page.click("button:has-text('Sign In')")
    page.wait_for_selector("text='SV Recommend'")
    return page

@pytest.fixture
def admin_page(page):
    """
    Fixture to provide an authenticated UI page using admin credentials.
    """
    page.goto(f"{BASE_URL}/pages/login.html")
    page.fill("input[type='email']", ADMIN_EMAIL)
    page.fill("input[type='password']", ADMIN_PASSWORD)
    page.click("button:has-text('Sign In')")
    page.wait_for_selector("text='System'")
    return page

@pytest.fixture
def mobile_context(browser):
    """
    Provides a browser context configured for a mobile viewport.
    """
    context = browser.new_context(
        viewport={'width': 375, 'height': 667},
        user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1"
    )
    yield context
    context.close()