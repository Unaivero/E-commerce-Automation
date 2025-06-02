import pytest
import allure
from pages.login_page import LoginPage
from tests.base_test import BaseTest


@allure.feature("Authentication")
@allure.story("User Login")
class TestLogin(BaseTest):
    """Test cases for user login functionality"""
    
    @allure.title("Successful login with valid credentials")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_successful_login(self, driver, config):
        """Test successful login with valid credentials"""
        self.log_step("Open login page")
        login_page = LoginPage(driver, config).open()
        
        self.log_step("Enter valid credentials")
        credentials = config.get_credentials("admin_user")
        login_page.login(credentials["username"], credentials["password"])
        
        self.log_step("Verify successful login")
        assert login_page.is_logged_in(), "User should be logged in successfully"
        self.take_screenshot("successful_login")
    
    @allure.title("Failed login with invalid credentials")
    @allure.severity(allure.severity_level.NORMAL)
    def test_failed_login_invalid_credentials(self, driver, config):
        """Test failed login with invalid credentials"""
        self.log_step("Open login page")
        login_page = LoginPage(driver, config).open()
        
        self.log_step("Enter invalid credentials")
        login_page.login("invalid@example.com", "wrongpassword")
        
        self.log_step("Verify error message")
        error_message = login_page.get_error_message()
        assert error_message is not None, "Error message should be displayed"
        assert "Invalid" in error_message or "incorrect" in error_message.lower(), \
            f"Error message should indicate invalid credentials, got: {error_message}"
        self.take_screenshot("failed_login_invalid_credentials")
    
    @allure.title("Failed login with empty credentials")
    @allure.severity(allure.severity_level.NORMAL)
    def test_failed_login_empty_credentials(self, driver, config):
        """Test failed login with empty credentials"""
        self.log_step("Open login page")
        login_page = LoginPage(driver, config).open()
        
        self.log_step("Submit form without entering credentials")
        login_page.click_element(login_page.LOGIN_BUTTON)
        
        self.log_step("Verify error message")
        error_message = login_page.get_error_message()
        assert error_message is not None, "Error message should be displayed"
        self.take_screenshot("failed_login_empty_credentials")
    
    @allure.title("Navigate to forgot password page")
    @allure.severity(allure.severity_level.MINOR)
    def test_navigate_to_forgot_password(self, driver, config):
        """Test navigation to forgot password page"""
        self.log_step("Open login page")
        login_page = LoginPage(driver, config).open()
        
        self.log_step("Click on forgot password link")
        login_page.click_forgot_password()
        
        self.log_step("Verify navigation to forgot password page")
        assert "forgot-password" in driver.current_url or "reset-password" in driver.current_url, \
            "Should navigate to forgot password page"
        self.take_screenshot("navigate_to_forgot_password")
    
    @allure.title("Navigate to registration page")
    @allure.severity(allure.severity_level.MINOR)
    def test_navigate_to_registration(self, driver, config):
        """Test navigation to registration page"""
        self.log_step("Open login page")
        login_page = LoginPage(driver, config).open()
        
        self.log_step("Click on register link")
        login_page.click_register()
        
        self.log_step("Verify navigation to registration page")
        assert "register" in driver.current_url or "signup" in driver.current_url, \
            "Should navigate to registration page"
        self.take_screenshot("navigate_to_registration")