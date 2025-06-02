import pytest
import logging
import allure
from utils.config import Config

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BaseTest:
    """Base class for all test cases"""
    
    @pytest.fixture(autouse=True)
    def setup(self, driver, config):
        """Setup for each test case"""
        self.driver = driver
        self.config = config
        self.logger = logger
        self.base_url = config.base_url
        
        self.logger.info(f"Starting test with browser: {config.browser}")
        self.logger.info(f"Testing environment: {config.env}")
        self.logger.info(f"Base URL: {self.base_url}")
        
        # Add allure environment info if using allure
        try:
            allure.attach(
                f"Browser: {config.browser}\nEnvironment: {config.env}\nBase URL: {self.base_url}",
                name="Environment Info",
                attachment_type=allure.attachment_type.TEXT
            )
        except Exception:
            # Allure might not be available
            pass
        
        yield
        
        # Teardown actions
        self.logger.info("Test completed")
    
    def take_screenshot(self, name="screenshot"):
        """Take a screenshot and attach to allure report"""
        try:
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name=name,
                attachment_type=allure.attachment_type.PNG
            )
        except Exception as e:
            self.logger.error(f"Failed to take screenshot: {e}")
    
    def log_step(self, description):
        """Log a test step with description"""
        self.logger.info(f"Step: {description}")
        try:
            allure.step(description)
        except Exception:
            # Allure might not be available
            pass