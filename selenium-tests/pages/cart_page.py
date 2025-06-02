from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CartPage(BasePage):
    """Page object for the shopping cart page"""
    
    # Locators
    CART_ITEMS = (By.CSS_SELECTOR, ".cart-item")
    CART_ITEM_NAME = (By.CSS_SELECTOR, ".cart-item-name")
    CART_ITEM_PRICE = (By.CSS_SELECTOR, ".cart-item-price")
    CART_ITEM_QUANTITY = (By.CSS_SELECTOR, ".cart-item-quantity input")
    CART_ITEM_TOTAL = (By.CSS_SELECTOR, ".cart-item-total")
    CART_ITEM_REMOVE = (By.CSS_SELECTOR, ".cart-item-remove")
    UPDATE_CART_BUTTON = (By.CSS_SELECTOR, ".update-cart-btn")
    CONTINUE_SHOPPING_BUTTON = (By.CSS_SELECTOR, ".continue-shopping-btn")
    CHECKOUT_BUTTON = (By.CSS_SELECTOR, ".checkout-btn")
    SUBTOTAL = (By.CSS_SELECTOR, ".cart-subtotal .amount")
    TAX = (By.CSS_SELECTOR, ".cart-tax .amount")
    SHIPPING = (By.CSS_SELECTOR, ".cart-shipping .amount")
    TOTAL = (By.CSS_SELECTOR, ".cart-total .amount")
    EMPTY_CART_MESSAGE = (By.CSS_SELECTOR, ".empty-cart-message")
    PROMO_CODE_INPUT = (By.ID, "promo-code")
    APPLY_PROMO_BUTTON = (By.CSS_SELECTOR, ".apply-promo-btn")
    PROMO_SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".promo-success")
    PROMO_ERROR_MESSAGE = (By.CSS_SELECTOR, ".promo-error")
    
    def __init__(self, driver, config):
        super().__init__(driver, config)
        # base_url is already set in BasePage.__init__
    
    def open(self):
        """Open the shopping cart page"""
        self.navigate_to("/cart")
        return self
    
    def get_cart_items_count(self):
        """Get the number of items in the cart"""
        cart_items = self.find_elements(self.CART_ITEMS)
        return len(cart_items)
    
    def is_cart_empty(self):
        """Check if the cart is empty"""
        return self.is_element_visible(self.EMPTY_CART_MESSAGE)
    
    def get_item_name(self, index=0):
        """Get the name of an item in the cart by index"""
        cart_items = self.find_elements(self.CART_ITEMS)
        if index < len(cart_items):
            item = cart_items[index]
            name_element = item.find_element(*self.CART_ITEM_NAME)
            return self.get_element_text((None, name_element))
        return None
    
    def get_item_price(self, index=0):
        """Get the price of an item in the cart by index"""
        cart_items = self.find_elements(self.CART_ITEMS)
        if index < len(cart_items):
            item = cart_items[index]
            price_element = item.find_element(*self.CART_ITEM_PRICE)
            price_text = self.get_element_text((None, price_element))
            return float(price_text.replace("$", "").replace(",", "").strip())
        return None
    
    def get_item_quantity(self, index=0):
        """Get the quantity of an item in the cart by index"""
        cart_items = self.find_elements(self.CART_ITEMS)
        if index < len(cart_items):
            item = cart_items[index]
            quantity_input = item.find_element(*self.CART_ITEM_QUANTITY)
            return int(quantity_input.get_attribute("value"))
        return None
    
    def set_item_quantity(self, quantity, index=0):
        """Set the quantity of an item in the cart by index"""
        cart_items = self.find_elements(self.CART_ITEMS)
        if index < len(cart_items):
            item = cart_items[index]
            quantity_input = item.find_element(*self.CART_ITEM_QUANTITY)
            # Clear and set new quantity
            quantity_input.clear()
            quantity_input.send_keys(str(quantity))
        return self
    
    def remove_item(self, index=0):
        """Remove an item from the cart by index"""
        cart_items = self.find_elements(self.CART_ITEMS)
        if index < len(cart_items):
            item = cart_items[index]
            remove_button = item.find_element(*self.CART_ITEM_REMOVE)
            remove_button.click()
        return self
    
    def update_cart(self):
        """Click the update cart button"""
        self.click_element(self.UPDATE_CART_BUTTON)
        return self
    
    def continue_shopping(self):
        """Click the continue shopping button"""
        self.click_element(self.CONTINUE_SHOPPING_BUTTON)
        return self
    
    def proceed_to_checkout(self):
        """Click the checkout button"""
        self.click_element(self.CHECKOUT_BUTTON)
        return self
    
    def get_subtotal(self):
        """Get the subtotal amount"""
        subtotal_text = self.get_element_text(self.SUBTOTAL)
        return float(subtotal_text.replace("$", "").replace(",", "").strip())
    
    def get_tax(self):
        """Get the tax amount"""
        tax_text = self.get_element_text(self.TAX)
        return float(tax_text.replace("$", "").replace(",", "").strip())
    
    def get_shipping(self):
        """Get the shipping amount"""
        shipping_text = self.get_element_text(self.SHIPPING)
        return float(shipping_text.replace("$", "").replace(",", "").strip())
    
    def get_total(self):
        """Get the total amount"""
        total_text = self.get_element_text(self.TOTAL)
        return float(total_text.replace("$", "").replace(",", "").strip())
    
    def apply_promo_code(self, code):
        """Apply a promo code"""
        self.enter_text(self.PROMO_CODE_INPUT, code)
        self.click_element(self.APPLY_PROMO_BUTTON)
        return self
    
    def is_promo_success_displayed(self):
        """Check if promo success message is displayed"""
        return self.is_element_visible(self.PROMO_SUCCESS_MESSAGE)
    
    def is_promo_error_displayed(self):
        """Check if promo error message is displayed"""
        return self.is_element_visible(self.PROMO_ERROR_MESSAGE)