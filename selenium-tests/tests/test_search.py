import pytest
import allure
from .base_test import BaseTest # Assuming BaseTest handles setup and teardown
from pages.base_page import BasePage # Import BasePage
from pages.login_page import LoginPage # To ensure we are on a page with a search bar
from pages.search_results_page import SearchResultsPage
from test_data.products import get_product_by_name # To get test data

@allure.epic("E-Commerce Application")
@allure.feature("Search Functionality")
class TestSearch(BaseTest):

    @allure.story("Search for Existing Product")
    @allure.title("Test searching for a product that exists")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_search_existing_product(self, driver, config):
        allure.dynamic.description(
            "This test verifies that a user can search for an existing product "
            "and the product is displayed in the search results."
        )
        driver.get(self.base_url) # Start at the homepage or a page with search
        
        # For this example, let's assume the search bar is available on the login page or homepage
        # If login is required to search, perform login first
        # login_page = LoginPage(driver, config)
        # login_page.login("valid_user@example.com", "password123") # Example credentials
        # self.take_screenshot("after_login_before_search")

        # Using BasePage's perform_search, assuming search bar is globally accessible
        # If search is on a specific page, instantiate that page first
        base_page = BasePage(driver, config) # Or any page object that inherits BasePage
        
        searchable_product = get_product_by_name("Premium Wireless Headphones") # Get a product from test data
        if not searchable_product:
            pytest.fail("Test data 'Premium Wireless Headphones' not found for search test.")
        
        search_term = searchable_product['name']
        
        with allure.step(f"Perform search for product: {search_term}"):
            search_results_page = base_page.perform_search(search_term)
            self.take_screenshot(f"search_results_for_{search_term}")

        with allure.step("Verify search results page is loaded"):
            assert search_results_page.is_results_page_loaded(), "Search results page did not load."
        
        with allure.step(f"Verify product '{search_term}' is listed in results"):
            assert search_results_page.is_product_listed(search_term), \
                f"Product '{search_term}' was not found in search results."
            product_details = search_results_page.get_search_result_item_details(search_term)
            assert product_details is not None, f"Could not retrieve details for {search_term} from results"
            assert product_details['name'].lower() == search_term.lower(), "Product name in results does not match"
            # Add more assertions if needed, e.g., price, image

    @allure.story("Search for Non-Existent Product")
    @allure.title("Test searching for a product that does not exist")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_search_non_existent_product(self, driver, config):
        allure.dynamic.description(
            "This test verifies that searching for a non-existent product displays a 'no results' message."
        )
        driver.get(self.base_url)
        base_page = BasePage(driver, config)
        search_term = "NonExistentProductXYZ123"

        with allure.step(f"Perform search for non-existent product: {search_term}"):
            search_results_page = base_page.perform_search(search_term)
            self.take_screenshot(f"search_results_for_{search_term}")

        with allure.step("Verify 'no results found' message is displayed"):
            assert search_results_page.is_no_results_message_displayed(), \
                "'No results found' message was not displayed for a non-existent product."
            assert search_results_page.get_results_count() == 0, \
                "Search results count should be 0 for a non-existent product."

    @allure.story("Search with Partial Term")
    @allure.title("Test searching using a partial product name")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_search_partial_term(self, driver, config):
        allure.dynamic.description(
            "This test verifies that searching with a partial term returns relevant products."
        )
        driver.get(self.base_url)
        base_page = BasePage(driver, config)
        
        # Assuming 'Premium Wireless Headphones' and 'Smart Fitness Watch' exist from products.json
        partial_search_term = "Wireless"
        expected_product1 = "Premium Wireless Headphones"
        expected_product2 = "Smart Fitness Watch"

        with allure.step(f"Perform search for partial term: {partial_search_term}"):
            search_results_page = base_page.perform_search(partial_search_term)
            self.take_screenshot(f"search_results_for_{partial_search_term}")

        with allure.step("Verify search results page is loaded"):
            assert search_results_page.is_results_page_loaded(), "Search results page did not load."
        
        with allure.step(f"Verify products matching '{partial_search_term}' are listed"):
            results_count = search_results_page.get_results_count()
            assert results_count > 0, f"No results found for partial term '{partial_search_term}'."
            product_names = search_results_page.get_product_names()
            assert any(expected_product1.lower() in name.lower() for name in product_names), \
                f"Expected product '{expected_product1}' not found for partial search '{partial_search_term}'."
            assert any(expected_product2.lower() in name.lower() for name in product_names), \
                f"Expected product '{expected_product2}' not found for partial search '{partial_search_term}'."

    @allure.story("Search with Empty Term")
    @allure.title("Test searching with an empty search term")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.regression
    def test_search_empty_term(self, driver, config):
        allure.dynamic.description(
            "This test verifies the application's behavior when an empty search term is submitted. "
            "(e.g., stays on the page, shows a message, or shows all products - depends on app behavior)"
        )
        driver.get(self.base_url)
        initial_url = driver.current_url
        base_page = BasePage(driver, config)
        search_term = ""

        with allure.step(f"Perform search with empty term"):
            search_results_page = base_page.perform_search(search_term)
            self.take_screenshot(f"search_results_for_empty_term")

        # Behavior for empty search can vary. Assert based on expected behavior.
        # Option 1: Stays on the same page without error or specific message
        with allure.step("Verify behavior for empty search (e.g., stays on current page or shows specific message)"):
            # Example: Assert current URL is still the initial URL or a search results page (if it defaults to all products)
            # assert driver.current_url == initial_url, "URL changed unexpectedly after empty search."
            # Or, if it shows a 'please enter search term' message:
            # assert base_page.is_element_visible((By.ID, "search-term-required-message")), "Empty search term message not shown."
            # Or, if it shows all products or a default results page:
            assert search_results_page.is_results_page_loaded(timeout=5), \
                "Search results page (or a default view) did not load after empty search."
            # This assertion depends heavily on how the application handles empty searches.
            # For this example, let's assume it might show the results page, possibly empty or with all items.
            # Adjust assertions based on actual application behavior.
            pass # Placeholder for specific assertion based on app behavior

    # You might need to add a helper in products.json or a new test data file for search terms
    # For now, using get_product_by_name from existing products.json
