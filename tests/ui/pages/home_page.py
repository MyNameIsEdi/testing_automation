from .base_page import BasePage

class HomePage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.nav_home = "text='SV Recommend'"
        self.nav_help = "text='Help'"
        self.nav_about = "text='About'"
        self.nav_store = "text='Store'"
        self.nav_profile = "text='My Profile'"
        self.nav_system = "text='System'"
        self.nav_logout = "text='Logout'"
        self.nav_add_recommendation = "text='+ Add Recommendation'"
        
        self.filter_all = "text='All'"
        self.filter_book = "text='Book'"
        self.filter_movie = "text='Movie'"
        self.filter_series = "text='Series'"
        self.filter_activity = "text='Activity'"
        self.filter_other = "text='Other'"
        
        self.recommendation_cards = ".recommendation-card" # Need to verify actual class later, or use role

    def go_to_add_recommendation(self):
        self.click(self.nav_add_recommendation)
        
    def filter_by(self, category_name):
        self.click(f"text='{category_name}'")
