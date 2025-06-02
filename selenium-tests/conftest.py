import pytest
import os
import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from utils.config import Config


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="Browser to run tests: chrome or firefox")
    parser.addoption("--env", action="store", default="qa", help="Environment to run tests: dev, qa, or prod")


@pytest.fixture(scope="session")
def config(request):
    browser = request.config.getoption("--browser")
    env = request.config.getoption("--env")
    return Config(browser, env)


@pytest.fixture(scope="function")
def driver(config, request):
    browser = config.browser.lower()
    
    if browser == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        # options.add_argument("--headless")  # Uncomment for headless execution
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    elif browser == "firefox":
        options = webdriver.FirefoxOptions()
        options.add_argument("--start-maximized")
        # options.add_argument("--headless")  # Uncomment for headless execution
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
    else:
        raise ValueError(f"Browser {browser} is not supported")
    
    driver.implicitly_wait(10)
    
    # Add test name to the driver for logging purposes
    test_name = request.node.name
    setattr(driver, "test_name", test_name)
    
    yield driver
    
    driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call":
        driver = item.funcargs.get("driver")
        if driver and report.failed:
            # Take screenshot on test failure
            try:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                test_name = getattr(driver, "test_name", "unknown_test")
                screenshot_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "reports", "screenshots")
                os.makedirs(screenshot_dir, exist_ok=True)
                screenshot_path = os.path.join(screenshot_dir, f"{test_name}_{timestamp}.png")
                driver.save_screenshot(screenshot_path)
                print(f"Screenshot saved to {screenshot_path}")
                
                # Attach screenshot to Allure report if Allure is being used
                try:
                    import allure
                    allure.attach(
                        driver.get_screenshot_as_png(),
                        name=f"{test_name}_{timestamp}",
                        attachment_type=allure.attachment_type.PNG
                    )
                except ImportError:
                    # Allure not available, skip attachment
                    pass
            except Exception as e:
                print(f"Failed to take screenshot: {e}")