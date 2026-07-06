from .base_page import BasePage

class RecommendationPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.delete_btn = "button:has-text('Delete')"
        self.comment_input = "input[placeholder*='comment']" # Will refine locator
        self.star_rating = ".star-rating" # Will refine
        self.submit_comment_btn = "button:has-text('Submit')"

    def delete_recommendation(self):
        self.click(self.delete_btn)

class AddRecommendationPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.category_select = "select"
        self.name_input = "input[placeholder*='Recommendation Name']"
        self.your_name_input = "input[placeholder*='Your Name']"
        self.description_input = "textarea"
        self.website_link_input = "input[placeholder*='Website Link']"
        self.image_input = "input[type='file']"
        self.submit_btn = "button:has-text('Add Recommendation')"

    def add_recommendation(self, category, name, your_name, desc="", link=""):
        self.page.select_option(self.category_select, label=category)
        self.fill(self.name_input, name)
        self.fill(self.your_name_input, your_name)
        if desc:
            self.fill(self.description_input, desc)
        if link:
            self.fill(self.website_link_input, link)
        self.click(self.submit_btn)
