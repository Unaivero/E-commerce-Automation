from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):
    """Page object for the login page"""
    
    # Locators
    EMAIL_INPUT = (By.ID, "email")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    FORGOT_PASSWORD_LINK = (By.LINK_TEXT, "Forgot Password?")
    REGISTER_LINK = (By.LINK_TEXT, "Register")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".alert-danger")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".alert-success")
    
    def __init__(self, driver, config):
        super().__init__(driver, config)
        # base_url is already set in BasePage.__init__
    
    def open(self):
        """Open the login page"""
        self.navigate_to("/login")
        return self
    
    def login(self, email, password):
        """Login with the provided credentials"""
        self.enter_text(self.EMAIL_INPUT, email)
        self.enter_text(self.PASSWORD_INPUT, password)
        self.click_element(self.LOGIN_BUTTON)
        return self
    
    def click_forgot_password(self):
        """Click on the forgot password link"""
        self.click_element(self.FORGOT_PASSWORD_LINK)
        return self
    
    def click_register(self):
        """Click on the register link"""
        self.click_element(self.REGISTER_LINK)
        return self
    
    def get_error_message(self):
        """Get the error message text"""
        if self.is_element_visible(self.ERROR_MESSAGE):
            return self.get_element_text(self.ERROR_MESSAGE)
        return None
    
    def get_success_message(self):
        """Get the success message text"""
        if self.is_element_visible(self.SUCCESS_MESSAGE):
            return self.get_element_text(self.SUCCESS_MESSAGE)
        return None
    
    def is_logged_in(self):
        """Check if user is logged in by verifying URL change"""
        current_url = self.get_current_url()
        return "/account" in current_url or "/dashboard" in current_url