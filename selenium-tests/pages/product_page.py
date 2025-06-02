from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class ProductPage(BasePage):
    """Page object for the product details page"""
    
    # Locators
    PRODUCT_TITLE = (By.CSS_SELECTOR, ".product-title h1")
    PRODUCT_PRICE = (By.CSS_SELECTOR, ".product-price")
    PRODUCT_DESCRIPTION = (By.CSS_SELECTOR, ".product-description")
    PRODUCT_IMAGE = (By.CSS_SELECTOR, ".product-image img")
    QUANTITY_INPUT = (By.ID, "quantity")
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, ".add-to-cart-btn")
    ADD_TO_WISHLIST_BUTTON = (By.CSS_SELECTOR, ".add-to-wishlist-btn")
    PRODUCT_RATING = (By.CSS_SELECTOR, ".product-rating")
    SIZE_OPTIONS = (By.CSS_SELECTOR, ".size-options .size-option")
    COLOR_OPTIONS = (By.CSS_SELECTOR, ".color-options .color-option")
    CART_SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".cart-success")
    REVIEWS_TAB = (By.CSS_SELECTOR, "a[href='#reviews']")
    RELATED_PRODUCTS = (By.CSS_SELECTOR, ".related-products .product-item")
    WISHLIST_SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".wishlist-success-message") # Added for wishlist
    
    def __init__(self, driver, config):
        super().__init__(driver, config)
        # base_url is already set in BasePage.__init__
    
    def open_product(self, product_id):
        """Open a specific product page by ID"""
        self.navigate_to(f"/product/{product_id}")
        return self
    
    def get_product_title(self):
        """Get the product title"""
        return self.get_element_text(self.PRODUCT_TITLE)
    
    def get_product_price(self):
        """Get the product price"""
        price_text = self.get_element_text(self.PRODUCT_PRICE)
        # Remove currency symbol and convert to float
        return float(price_text.replace("$", "").replace(",", "").strip())
    
    def get_product_description(self):
        """Get the product description"""
        return self.get_element_text(self.PRODUCT_DESCRIPTION)
    
    def set_quantity(self, quantity):
        """Set the product quantity"""
        self.enter_text(self.QUANTITY_INPUT, str(quantity))
        return self
    
    def add_to_cart(self):
        """Add the product to cart"""
        self.click_element(self.ADD_TO_CART_BUTTON)
        return self
    
    def add_to_wishlist(self):
        """Add the product to wishlist"""
        self.click_element(self.ADD_TO_WISHLIST_BUTTON)
        return self
    
    def select_size(self, size_text):
        """Select a size option by text"""
        size_elements = self.find_elements(self.SIZE_OPTIONS)
        for size_element in size_elements:
            if size_element.text.strip() == size_text:
                size_element.click()
                return self
        raise ValueError(f"Size option '{size_text}' not found")
    
    def select_color(self, color_name):
        """Select a color option by name"""
        color_elements = self.find_elements(self.COLOR_OPTIONS)
        for color_element in color_elements:
            if color_name.lower() in color_element.get_attribute("title").lower():
                color_element.click()
                return self
        raise ValueError(f"Color option '{color_name}' not found")
    
    def is_add_to_cart_success_displayed(self):
        """Check if add to cart success message is displayed"""
        return self.is_element_visible(self.CART_SUCCESS_MESSAGE)
    
    def get_cart_success_message(self):
        """Get the cart success message"""
        return self.get_element_text(self.CART_SUCCESS_MESSAGE)

    def is_add_to_wishlist_success_displayed(self):
        """Check if add to wishlist success message is displayed"""
        return self.is_element_visible(self.WISHLIST_SUCCESS_MESSAGE)

    def get_wishlist_success_message(self):
        """Get the wishlist success message"""
        return self.get_element_text(self.WISHLIST_SUCCESS_MESSAGE)
    
    def click_reviews_tab(self):
        """Click on the reviews tab"""
        self.click_element(self.REVIEWS_TAB)
        return self
    
    def get_related_products_count(self):
        """Get the count of related products"""
        related_products = self.find_elements(self.RELATED_PRODUCTS)
        return len(related_products)
    
    def click_related_product(self, index=0):
        """Click on a related product by index"""
        related_products = self.find_elements(self.RELATED_PRODUCTS)
        if index < len(related_products):
            related_products[index].click()
            return self
        else:
            raise IndexError(f"Related product index {index} out of range")