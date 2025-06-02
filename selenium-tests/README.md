# E-Commerce QA Lab - Selenium UI Tests

This directory contains UI automation tests for the E-Commerce application using Selenium WebDriver with Python.

## Framework Structure

```
selenium-tests/
├── conftest.py            # Pytest fixtures and configuration
├── config.json            # Test environment configuration
├── pages/                 # Page Object Models
│   ├── base_page.py       # Base class for all page objects
│   ├── cart_page.py       # Shopping cart page object
│   ├── login_page.py      # Login page object
│   ├── product_page.py    # Product page object
│   └── search_results_page.py # Search results page object
├── pytest.ini             # Pytest configuration and markers
├── tests/                 # Test cases
│   ├── base_test.py       # Base test class with common functionality
│   ├── test_login.py      # Login tests
│   ├── test_product.py    # Product and cart tests
│   └── test_search.py     # Search functionality tests
├── test_data/             # Test data files
│   └── products.py        # Product test data
└── utils/                 # Utility modules
    └── config.py          # Configuration handling
```

## Prerequisites

- Python 3.9+
- Chrome browser
- Required Python packages (see requirements.txt in the root directory)

## Setup

1. Install dependencies:
```bash
pip install -r ../requirements.txt
```

2. Configure test environment:
   - Edit `config.json` to set the appropriate URLs and credentials
   - Alternatively, use environment variables to override configuration values

## Running Tests

### Run all UI tests:
```bash
python -m pytest
```

### Run specific test file:
```bash
python -m pytest tests/test_login.py
```

### Run tests with specific marker:
```bash
python -m pytest -m smoke
```

### Run tests with verbose output:
```bash
python -m pytest -v
```

### Generate Allure reports:
```bash
python -m pytest --alluredir=./allure-results
allure serve ./allure-results
```

## Test Categories

- **Smoke Tests**: Basic functionality tests marked with `@pytest.mark.smoke`
- **Regression Tests**: Comprehensive tests marked with `@pytest.mark.regression`

## Page Object Model

This framework follows the Page Object Model design pattern:
- Each page in the application has a corresponding Page Object class
- Page Objects encapsulate page elements and interactions
- Test classes use Page Objects to interact with the application

## Configuration

The framework supports multiple environments (dev, qa, prod) configured in `config.json`.
Environment variables can override configuration values:
- `TEST_ENV`: Environment to use (dev, qa, prod)
- `BASE_URL`: Override the base URL
- `BROWSER`: Browser to use (chrome, firefox)
- `HEADLESS`: Run in headless mode (true, false)

## Screenshots

Screenshots are automatically captured on test failures and attached to Allure reports.