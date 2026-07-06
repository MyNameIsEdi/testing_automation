from .base_page import BasePage

class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.email_input = "input[type='email']"
        self.password_input = "input[type='password']"
        self.sign_in_btn = "button:has-text('Sign In')"
        self.register_link = "text='Register here'"
        
    def login(self, email, password):
        self.fill(self.email_input, email)
        self.fill(self.password_input, password)
        self.click(self.sign_in_btn)

class RegisterPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.name_input = "input[placeholder='Your full name']"
        self.email_input = "input[type='email']"
        self.password_input = "input[type='password']"
        self.create_account_btn = "button:has-text('Create Account')"
        self.sign_in_link = "text='Sign in'"
        
    def register(self, name, email, password):
        self.fill(self.name_input, name)
        self.fill(self.email_input, email)
        self.fill(self.password_input, password)
        self.click(self.create_account_btn)
