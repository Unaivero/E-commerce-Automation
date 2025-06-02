from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from .base_page import BasePage
import allure

class SearchResultsPage(BasePage):
    # Locators
    _search_results_container = (By.ID, "search-results-container") # Main container for all results
    _product_item = (By.CSS_SELECTOR, ".product-item") # General selector for a single product item
    _product_name = (By.CSS_SELECTOR, ".product-name") # Selector for product name within an item
    _product_price = (By.CSS_SELECTOR, ".product-price") # Selector for product price
    _no_results_message = (By.ID, "no-results-message")
    _sort_options_dropdown = (By.ID, "sort-options")
    _filter_category_button = (By.XPATH, "//button[contains(text(), 'Category')]")

    def __init__(self, driver: WebDriver, config):
        super().__init__(driver, config)
        self.config = config

    @allure.step("Verify search results page is loaded")
    def is_results_page_loaded(self, timeout=10):
        """Verifies if the search results container is visible."""
        return self.is_element_visible(self._search_results_container, timeout=timeout)

    @allure.step("Get number of search results displayed")
    def get_results_count(self):
        """Returns the number of product items displayed on the page."""
        if not self.is_element_visible(self._search_results_container):
            return 0
        results = self.find_elements(self._product_item)
        return len(results)

    @allure.step("Get product names from search results")
    def get_product_names(self):
        """Returns a list of product names from the search results."""
        names = []
        product_elements = self.find_elements(self._product_item)
        for elem in product_elements:
            try:
                name_element = elem.find_element(*self._product_name)
                names.append(self.get_element_text(name_element))
            except Exception:
                # Handle cases where a product item might not have a name or structure is different
                pass # Or log a warning
        return names

    @allure.step("Verify if product '{product_name}' is listed in search results")
    def is_product_listed(self, product_name: str):
        """Checks if a product with the given name is present in the search results."""
        product_names = self.get_product_names()
        return product_name.lower() in [name.lower() for name in product_names]

    @allure.step("Click on product '{product_name}' from search results")
    def click_product_by_name(self, product_name: str):
        """Clicks on a product link/image from the search results based on its name."""
        product_elements = self.find_elements(self._product_item)
        for elem in product_elements:
            try:
                name_element = elem.find_element(*self._product_name)
                if self.get_element_text(name_element).lower() == product_name.lower():
                    self.click_element(elem) # Click the whole product item container
                    # Or click a specific link within the item: self.click_element(name_element)
                    return True
            except Exception:
                pass
        allure.attach(f"Product '{product_name}' not found to click.", name="ClickProductError", attachment_type=allure.attachment_type.TEXT)
        return False

    @allure.step("Verify 'no results found' message is displayed")
    def is_no_results_message_displayed(self, timeout=5):
        """Checks if the 'no results found' message is visible."""
        return self.is_element_visible(self._no_results_message, timeout=timeout)

    @allure.step("Select sort option: {option_text}")
    def select_sort_option(self, option_text: str):
        """Selects an option from the sort dropdown (e.g., 'Price: Low to High')."""
        if self.is_element_visible(self._sort_options_dropdown):
            self.select_dropdown_option_by_visible_text(self._sort_options_dropdown, option_text)
            allure.attach(f"Selected sort option: {option_text}", name="SortSelection", attachment_type=allure.attachment_type.TEXT)
        else:
            allure.attach("Sort options dropdown not found.", name="SortSelectionError", attachment_type=allure.attachment_type.TEXT)

    @allure.step("Apply category filter: {category_name}")
    def apply_category_filter(self, category_name: str):
        """Applies a category filter. Assumes filters are links or buttons."""
        # This is a placeholder; actual filter interaction can be complex
        # Example: Click a main filter button, then select a category
        if self.is_element_visible(self._filter_category_button):
            self.click_element(self._filter_category_button)
            # Add logic to find and click the specific category_name filter
            # category_filter_locator = (By.LINK_TEXT, category_name) # Example
            # self.click_element(category_filter_locator)
            allure.attach(f"Attempted to apply category filter: {category_name}", name="FilterSelection", attachment_type=allure.attachment_type.TEXT)
        else:
            allure.attach("Category filter button not found.", name="FilterSelectionError", attachment_type=allure.attachment_type.TEXT)

    def get_search_result_item_details(self, product_name: str):
        """Retrieves details (e.g., name, price) for a specific product in search results."""
        product_elements = self.find_elements(self._product_item)
        for elem in product_elements:
            try:
                name_element = elem.find_element(*self._product_name)
                current_product_name = self.get_element_text(name_element)
                if current_product_name.lower() == product_name.lower():
                    price_element = elem.find_element(*self._product_price)
                    price = self.get_element_text(price_element)
                    return {"name": current_product_name, "price": price}
            except Exception:
                pass
        return None
