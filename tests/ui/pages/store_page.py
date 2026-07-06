from .base_page import BasePage
import re

class StorePage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        # Assuming there are buttons like "Add to cart"
        self.add_to_cart_btns = "button:has-text('Add to cart')"
        self.cart_icon = ".cart-icon" # Will need to verify

    def add_item_to_cart(self, index=0):
        self.page.locator(self.add_to_cart_btns).nth(index).click()

    def go_to_cart(self):
        self.click(self.cart_icon)

class CartPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.increase_qty_btn = "button:has-text('+')"
        self.decrease_qty_btn = "button:has-text('-')"
        self.remove_btn = "button:has-text('Remove')"
        self.proceed_to_payment_btn = "button:has-text('Proceed to Payment')"
        self.total_price_locator = ".total-price" # Refine later

    def increase_quantity(self, index=0):
        self.page.locator(self.increase_qty_btn).nth(index).click()

    def decrease_quantity(self, index=0):
        self.page.locator(self.decrease_qty_btn).nth(index).click()

    def remove_item(self, index=0):
        self.page.locator(self.remove_btn).nth(index).click()

    def go_to_payment(self):
        self.click(self.proceed_to_payment_btn)

class PaymentPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.full_name_input = "input[placeholder*='Full Name']"
        self.address_input = "input[placeholder*='Address']"
        self.credit_card_input = "input[placeholder*='Credit Card']"
        self.cvv_input = "input[placeholder*='CVV']"
        self.expiration_input = "input[type='date']" # or placeholder
        self.place_order_btn = "button:has-text('Place Order')"

    def fill_payment_info(self, name, address, card, cvv, expiry):
        self.fill(self.full_name_input, name)
        self.fill(self.address_input, address)
        self.fill(self.credit_card_input, card)
        self.fill(self.cvv_input, cvv)
        # Using string format for date, might need adjustment based on field type
        self.page.locator(self.expiration_input).fill(expiry)
        
    def submit_payment(self):
        self.click(self.place_order_btn)
