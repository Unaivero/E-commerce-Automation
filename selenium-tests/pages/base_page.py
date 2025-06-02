from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By # Added for search locators
from selenium.webdriver.common.keys import Keys # Added for search submit
import allure

class BasePage:
    # Default timeout for explicit waits
    TIMEOUT = 10

    # Common locators (e.g., for header elements like search bar)
    _search_input = (By.ID, "search-input")  # Example ID, adjust as needed
    _search_submit_button = (By.XPATH, "//button[@type='submit' and contains(@aria-label, 'Search')]") # Example XPath

    def __init__(self, driver: WebDriver, config):
        self.driver = driver
        self.config = config
        self.base_url = config.base_url
        # Use the default TIMEOUT for explicit waits, or could use config.implicit_wait
        self.timeout = self.TIMEOUT

    @allure.step("Navigate to URL: {url}")
    def navigate_to_url(self, url: str):
        """Navigates the browser to the specified URL."""
        try:
            self.driver.get(url)
            allure.attach(self.driver.current_url, name="Current URL after navigation", attachment_type=allure.attachment_type.URI_LIST)
        except Exception as e:
            allure.attach(f"Error navigating to {url}: {str(e)}", name="NavigationError", attachment_type=allure.attachment_type.TEXT)
            raise
            
    @allure.step("Navigate to path: {path}")
    def navigate_to(self, path: str):
        """Navigates to a path using the base_url. If path is a full URL, it will be used as is."""
        if path.startswith('http'):
            self.navigate_to_url(path)
        else:
            self.navigate_to_url(f"{self.base_url}{path}")
        return self

    @allure.step("Find element with locator: {locator}")
    def find_element(self, locator: tuple, timeout: int = None):
        """Finds and returns a web element, waiting until it's present."""
        wait_timeout = timeout if timeout is not None else self.timeout
        try:
            return WebDriverWait(self.driver, wait_timeout).until(
                EC.presence_of_element_located(locator)
            )
        except TimeoutException:
            allure.attach(f"Element with locator {locator} not found within {wait_timeout}s.", name="ElementNotFoundError", attachment_type=allure.attachment_type.TEXT)
            self.capture_screenshot(f"element_not_found_{locator[0]}_{locator[1]}".replace(' ','_'))
            raise NoSuchElementException(f"Element with locator {locator} not found within {wait_timeout}s.")

    @allure.step("Find multiple elements with locator: {locator}")
    def find_elements(self, locator: tuple, timeout: int = None):
        """Finds and returns a list of web elements, waiting until they are present."""
        wait_timeout = timeout if timeout is not None else self.timeout
        try:
            return WebDriverWait(self.driver, wait_timeout).until(
                EC.presence_of_all_elements_located(locator)
            )
        except TimeoutException:
            allure.attach(f"Elements with locator {locator} not found within {wait_timeout}s.", name="ElementsNotFoundError", attachment_type=allure.attachment_type.TEXT)
            return [] # Return empty list if no elements found

    @allure.step("Click element with locator: {locator}")
    def click_element(self, locator: tuple, timeout: int = None):
        """Waits for an element to be clickable and then clicks it."""
        wait_timeout = timeout if timeout is not None else self.timeout
        try:
            element = WebDriverWait(self.driver, wait_timeout).until(
                EC.element_to_be_clickable(locator)
            )
            element.click()
            allure.attach(f"Clicked element with locator: {locator}", name="ElementClicked", attachment_type=allure.attachment_type.TEXT)
        except ElementClickInterceptedException:
            allure.attach(f"Element click intercepted for locator {locator}. Trying JavaScript click.", name="ClickIntercepted", attachment_type=allure.attachment_type.TEXT)
            element = self.find_element(locator, timeout=wait_timeout) 
            self.js_click(element)
        except TimeoutException:
            allure.attach(f"Element with locator {locator} not clickable within {wait_timeout}s.", name="ElementNotClickableError", attachment_type=allure.attachment_type.TEXT)
            self.capture_screenshot(f"element_not_clickable_{locator[0]}_{locator[1]}".replace(' ','_'))
            raise

    @allure.step("Enter text '{text}' into element with locator: {locator}")
    def enter_text(self, locator: tuple, text: str, timeout: int = None):
        """Finds an element, clears it, and then types text into it."""
        try:
            element = self.find_element(locator, timeout=timeout)
            element.clear()
            element.send_keys(text)
            allure.attach(f"Entered text '{text}' into element {locator}", name="TextEntered", attachment_type=allure.attachment_type.TEXT)
        except Exception as e:
            allure.attach(f"Error entering text into {locator}: {str(e)}", name="EnterTextError", attachment_type=allure.attachment_type.TEXT)
            self.capture_screenshot(f"enter_text_error_{locator[0]}_{locator[1]}".replace(' ','_'))
            raise

    @allure.step("Get text from element: {locator_or_element}")
    def get_element_text(self, locator_or_element, timeout: int = None):
        """Retrieves the text content of an element."""
        try:
            if isinstance(locator_or_element, tuple): 
                element = self.find_element(locator_or_element, timeout=timeout)
            else: 
                element = locator_or_element
            text = element.text
            allure.attach(f"Retrieved text '{text}' from element {locator_or_element}", name="GetText", attachment_type=allure.attachment_type.TEXT)
            return text
        except Exception as e:
            allure.attach(f"Error getting text from {locator_or_element}: {str(e)}", name="GetTextError", attachment_type=allure.attachment_type.TEXT)
            raise

    @allure.step("Check if element with locator {locator} is visible")
    def is_element_visible(self, locator: tuple, timeout: int = None):
        """Checks if an element is visible on the page."""
        wait_timeout = timeout if timeout is not None else self.timeout
        try:
            WebDriverWait(self.driver, wait_timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    @allure.step("Check if element with locator {locator} is present")
    def is_element_present(self, locator: tuple, timeout: int = None):
        """Checks if an element is present in the DOM (may not be visible)."""
        wait_timeout = timeout if timeout is not None else self.timeout
        try:
            WebDriverWait(self.driver, wait_timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    @allure.step("Wait for element with locator {locator} to disappear")
    def wait_for_element_to_disappear(self, locator: tuple, timeout: int = None):
        """Waits for an element to become invisible or not present."""
        wait_timeout = timeout if timeout is not None else self.timeout
        try:
            WebDriverWait(self.driver, wait_timeout).until(
                EC.invisibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False 

    @allure.step("Get current URL")
    def get_current_url(self):
        """Returns the current URL of the browser."""
        return self.driver.current_url

    @allure.step("Get page title")
    def get_page_title(self):
        """Returns the title of the current page."""
        return self.driver.title

    @allure.step("Accept alert")
    def accept_alert(self, timeout: int = None):
        """Waits for an alert and accepts it."""
        wait_timeout = timeout if timeout is not None else self.timeout
        try:
            WebDriverWait(self.driver, wait_timeout).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            alert_text = alert.text
            alert.accept()
            allure.attach(f"Accepted alert with text: {alert_text}", name="AlertAccepted", attachment_type=allure.attachment_type.TEXT)
            return alert_text
        except TimeoutException:
            allure.attach("No alert present to accept.", name="AlertError", attachment_type=allure.attachment_type.TEXT)
            raise

    @allure.step("Dismiss alert")
    def dismiss_alert(self, timeout: int = None):
        """Waits for an alert and dismisses it."""
        wait_timeout = timeout if timeout is not None else self.timeout
        try:
            WebDriverWait(self.driver, wait_timeout).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            alert_text = alert.text
            alert.dismiss()
            allure.attach(f"Dismissed alert with text: {alert_text}", name="AlertDismissed", attachment_type=allure.attachment_type.TEXT)
            return alert_text
        except TimeoutException:
            allure.attach("No alert present to dismiss.", name="AlertError", attachment_type=allure.attachment_type.TEXT)
            raise

    @allure.step("Switch to iframe with locator: {locator}")
    def switch_to_iframe(self, locator: tuple, timeout: int = None):
        """Switches focus to an iframe."""
        wait_timeout = timeout if timeout is not None else self.timeout
        try:
            WebDriverWait(self.driver, wait_timeout).until(
                EC.frame_to_be_available_and_switch_to_it(locator)
            )
            allure.attach(f"Switched to iframe: {locator}", name="IframeSwitch", attachment_type=allure.attachment_type.TEXT)
        except TimeoutException:
            allure.attach(f"Iframe with locator {locator} not found.", name="IframeError", attachment_type=allure.attachment_type.TEXT)
            raise

    @allure.step("Switch back to default content from iframe")
    def switch_to_default_content(self):
        """Switches focus back to the main document from an iframe."""
        self.driver.switch_to.default_content()
        allure.attach("Switched back to default content.", name="IframeSwitchBack", attachment_type=allure.attachment_type.TEXT)

    @allure.step("Execute JavaScript: {script}")
    def execute_script(self, script: str, *args):
        """Executes JavaScript in the current window/frame."""
        try:
            return self.driver.execute_script(script, *args)
        except Exception as e:
            allure.attach(f"Error executing JavaScript: {script}, Error: {str(e)}", name="JavaScriptError", attachment_type=allure.attachment_type.TEXT)
            raise

    @allure.step("Scroll to element: {element_or_locator}")
    def scroll_to_element(self, element_or_locator):
        """Scrolls the page to bring the specified element into view."""
        try:
            if isinstance(element_or_locator, tuple):
                element = self.find_element(element_or_locator)
            else:
                element = element_or_locator
            self.execute_script("arguments[0].scrollIntoView(true);", element)
            allure.attach(f"Scrolled to element: {element_or_locator}", name="ScrollToElement", attachment_type=allure.attachment_type.TEXT)
        except Exception as e:
            allure.attach(f"Error scrolling to element {element_or_locator}: {str(e)}", name="ScrollError", attachment_type=allure.attachment_type.TEXT)
            raise

    @allure.step("Perform JavaScript click on element: {element_or_locator}")
    def js_click(self, element_or_locator):
        """Performs a click using JavaScript, useful for intercepted elements."""
        try:
            if isinstance(element_or_locator, tuple):
                element = self.find_element(element_or_locator)
            else:
                element = element_or_locator
            self.execute_script("arguments[0].click();", element)
            allure.attach(f"JavaScript click on element: {element_or_locator}", name="JSClick", attachment_type=allure.attachment_type.TEXT)
        except Exception as e:
            allure.attach(f"Error performing JavaScript click on {element_or_locator}: {str(e)}", name="JSClickError", attachment_type=allure.attachment_type.TEXT)
            raise

    @allure.step("Select dropdown option by visible text: '{text}' from locator: {locator}")
    def select_dropdown_option_by_visible_text(self, locator: tuple, text: str, timeout: int = None):
        """Selects an option from a dropdown by its visible text."""
        try:
            select_element = self.find_element(locator, timeout=timeout)
            select = Select(select_element)
            select.select_by_visible_text(text)
            allure.attach(f"Selected '{text}' from dropdown {locator}", name="DropdownSelect", attachment_type=allure.attachment_type.TEXT)
        except Exception as e:
            allure.attach(f"Error selecting '{text}' from dropdown {locator}: {str(e)}", name="DropdownError", attachment_type=allure.attachment_type.TEXT)
            raise

    @allure.step("Select dropdown option by value: '{value}' from locator: {locator}")
    def select_dropdown_option_by_value(self, locator: tuple, value: str, timeout: int = None):
        """Selects an option from a dropdown by its value attribute."""
        try:
            select_element = self.find_element(locator, timeout=timeout)
            select = Select(select_element)
            select.select_by_value(value)
            allure.attach(f"Selected option with value '{value}' from dropdown {locator}", name="DropdownSelectByValue", attachment_type=allure.attachment_type.TEXT)
        except Exception as e:
            allure.attach(f"Error selecting option with value '{value}' from dropdown {locator}: {str(e)}", name="DropdownError", attachment_type=allure.attachment_type.TEXT)
            raise

    @allure.step("Hover over element with locator: {locator}")
    def hover_over_element(self, locator: tuple, timeout: int = None):
        """Hovers the mouse cursor over an element."""
        try:
            element = self.find_element(locator, timeout=timeout)
            ActionChains(self.driver).move_to_element(element).perform()
            allure.attach(f"Hovered over element {locator}", name="HoverElement", attachment_type=allure.attachment_type.TEXT)
        except Exception as e:
            allure.attach(f"Error hovering over element {locator}: {str(e)}", name="HoverError", attachment_type=allure.attachment_type.TEXT)
            raise

    @allure.step("Capture screenshot: {name}")
    def capture_screenshot(self, name: str = "screenshot"):
        """Captures a screenshot and attaches it to the Allure report."""
        try:
            safe_name = "".join([c if c.isalnum() else "_" for c in name])
            allure.attach(self.driver.get_screenshot_as_png(), 
                          name=safe_name, 
                          attachment_type=allure.attachment_type.PNG)
        except Exception as e:
            allure.attach(f"Failed to capture screenshot: {str(e)}", name="ScreenshotError", attachment_type=allure.attachment_type.TEXT)
            print(f"Error capturing screenshot '{name}': {e}")

    @allure.step("Perform search for term: {search_term}")
    def perform_search(self, search_term: str):
        """Enters text into the search bar and submits the search."""
        from .search_results_page import SearchResultsPage # Local import to avoid circular dependency
        try:
            self.enter_text(self._search_input, search_term)
            search_input_element = self.find_element(self._search_input)
            search_input_element.send_keys(Keys.RETURN)
            allure.attach(f"Performed search for: {search_term}", name="SearchPerformed", attachment_type=allure.attachment_type.TEXT)
            return SearchResultsPage(self.driver, self.config) 
        except Exception as e:
            allure.attach(f"Error performing search for '{search_term}': {str(e)}", name="SearchError", attachment_type=allure.attachment_type.TEXT)
            self.capture_screenshot(f"search_error_{search_term}".replace(' ','_'))
            raise
