import pytest
import allure
import json
import os
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from tests.base_test import BaseTest


@allure.feature("Product")
@allure.story("Product Details and Cart Operations")
class TestProduct(BaseTest):
    """Test cases for product details and cart operations"""
    
    @pytest.fixture
    def product_data(self):
        """Load product test data from JSON file"""
        test_data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'test_data', 'products.json')
        try:
            with open(test_data_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Return default test data if file not found
            return {
                "products": [
                    {
                        "id": "1",
                        "name": "Test Product 1",
                        "price": 29.99,
                        "description": "This is a test product description"
                    }
                ]
            }
    
    @allure.title("View product details")
    @allure.severity(allure.severity_level.NORMAL)
    def test_view_product_details(self, driver, config, product_data):
        """Test viewing product details"""
        product_id = product_data["products"][0]["id"]
        expected_name = product_data["products"][0]["name"]
        
        self.log_step(f"Open product page for product ID: {product_id}")
        product_page = ProductPage(driver, config).open_product(product_id)
        
        self.log_step("Verify product title")
        actual_title = product_page.get_product_title()
        assert expected_name in actual_title, f"Expected product title to contain '{expected_name}', got '{actual_title}'"
        
        self.log_step("Verify product description is displayed")
        description = product_page.get_product_description()
        assert description, "Product description should be displayed"
        
        self.log_step("Verify product price is displayed")
        price = product_page.get_product_price()
        assert price > 0, f"Product price should be greater than 0, got {price}"
        
        self.take_screenshot("product_details")
    
    @allure.title("Add product to cart")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_add_product_to_cart(self, driver, config, product_data):
        """Test adding a product to the cart"""
        product_id = product_data["products"][0]["id"]
        
        self.log_step(f"Open product page for product ID: {product_id}")
        product_page = ProductPage(driver, config).open_product(product_id)
        
        self.log_step("Set quantity to 2")
        product_page.set_quantity(2)
        
        self.log_step("Add product to cart")
        product_page.add_to_cart()
        
        self.log_step("Verify success message is displayed")
        assert product_page.is_add_to_cart_success_displayed(), "Add to cart success message should be displayed"
        
        self.log_step("Navigate to cart page")
        cart_page = CartPage(driver, config).open()
        
        self.log_step("Verify cart is not empty")
        assert not cart_page.is_cart_empty(), "Cart should not be empty"
        
        self.log_step("Verify item count in cart")
        assert cart_page.get_cart_items_count() > 0, "Cart should contain at least one item"
        
        self.log_step("Verify item quantity")
        assert cart_page.get_item_quantity(0) == 2, f"Item quantity should be 2, got {cart_page.get_item_quantity(0)}"
        
        self.take_screenshot("product_added_to_cart")

    @allure.title("Add product to wishlist")
    @allure.severity(allure.severity_level.NORMAL)
    def test_add_to_wishlist(self, driver, config, product_data):
        """Test adding a product to the wishlist"""
        product_id = product_data["products"][0]["id"]
        expected_product_name = product_data["products"][0]["name"]

        self.log_step(f"Open product page for product ID: {product_id}")
        product_page = ProductPage(driver, config).open_product(product_id)

        self.log_step(f"Add product '{expected_product_name}' to wishlist")
        product_page.add_to_wishlist()

        self.log_step("Verify wishlist success message is displayed")
        assert product_page.is_add_to_wishlist_success_displayed(), \
            "Wishlist success message should be displayed after adding to wishlist"
        
        # Optional: Verify the content of the success message if needed
        # self.log_step("Verify wishlist success message content")
        # success_message = product_page.get_wishlist_success_message()
        # assert "added to your wishlist" in success_message.lower(), \
        #     f"Unexpected wishlist success message: '{success_message}'"

        self.take_screenshot("product_added_to_wishlist")
    
    @allure.title("Update product quantity in cart")
    @allure.severity(allure.severity_level.NORMAL)
    def test_update_product_quantity_in_cart(self, driver, config, product_data):
        """Test updating product quantity in the cart"""
        product_id = product_data["products"][0]["id"]
        
        self.log_step(f"Open product page for product ID: {product_id}")
        product_page = ProductPage(driver, config).open_product(product_id)
        
        self.log_step("Add product to cart")
        product_page.add_to_cart()
        
        self.log_step("Navigate to cart page")
        cart_page = CartPage(driver, config).open()
        
        self.log_step("Update item quantity to 3")
        cart_page.set_item_quantity(3, 0)
        cart_page.update_cart()
        
        self.log_step("Verify updated quantity")
        assert cart_page.get_item_quantity(0) == 3, f"Item quantity should be 3, got {cart_page.get_item_quantity(0)}"
        
        self.take_screenshot("updated_cart_quantity")
    
    @allure.title("Remove product from cart")
    @allure.severity(allure.severity_level.NORMAL)
    def test_remove_product_from_cart(self, driver, config, product_data):
        """Test removing a product from the cart"""
        product_id = product_data["products"][0]["id"]
        
        self.log_step(f"Open product page for product ID: {product_id}")
        product_page = ProductPage(driver, config).open_product(product_id)
        
        self.log_step("Add product to cart")
        product_page.add_to_cart()
        
        self.log_step("Navigate to cart page")
        cart_page = CartPage(driver, config).open()
        
        initial_count = cart_page.get_cart_items_count()
        self.log_step(f"Initial cart items count: {initial_count}")
        
        self.log_step("Remove item from cart")
        cart_page.remove_item(0)
        
        self.log_step("Verify item was removed")
        if initial_count > 1:
            assert cart_page.get_cart_items_count() == initial_count - 1, "Cart should have one less item"
        else:
            assert cart_page.is_cart_empty(), "Cart should be empty"
        
        self.take_screenshot("removed_from_cart")
    
    @allure.title("Proceed to checkout from cart")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_proceed_to_checkout(self, driver, config, product_data):
        """Test proceeding to checkout from the cart"""
        product_id = product_data["products"][0]["id"]
        
        self.log_step(f"Open product page for product ID: {product_id}")
        product_page = ProductPage(driver, config).open_product(product_id)
        
        self.log_step("Add product to cart")
        product_page.add_to_cart()
        
        self.log_step("Navigate to cart page")
        cart_page = CartPage(driver, config).open()
        
        self.log_step("Proceed to checkout")
        cart_page.proceed_to_checkout()
        
        self.log_step("Verify navigation to checkout page")
        current_url = driver.current_url
        assert "checkout" in current_url, f"Should navigate to checkout page, got URL: {current_url}"
        
        self.take_screenshot("proceed_to_checkout")
