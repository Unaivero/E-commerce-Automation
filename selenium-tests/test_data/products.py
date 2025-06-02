import json
import os
import allure

# Determine the absolute path to products.json relative to this file
_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
_PRODUCTS_JSON_PATH = os.path.join(_CURRENT_DIR, 'products.json')

@allure.step("Load product data from JSON")
def load_products_from_json(file_path=_PRODUCTS_JSON_PATH):
    """Loads product data from the specified JSON file."""
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        if 'products' not in data or not isinstance(data['products'], list):
            allure.attach(f"JSON file at {file_path} is missing 'products' list.", name="ProductDataError", attachment_type=allure.attachment_type.TEXT)
            raise ValueError("Product data JSON must contain a 'products' list.")
        allure.attach(f"Successfully loaded {len(data['products'])} products from {file_path}", name="ProductDataLoaded", attachment_type=allure.attachment_type.TEXT)
        return data['products']
    except FileNotFoundError:
        allure.attach(f"Product data file not found at {file_path}", name="FileNotFoundError", attachment_type=allure.attachment_type.TEXT)
        raise FileNotFoundError(f"Product data file not found: {file_path}")
    except json.JSONDecodeError:
        allure.attach(f"Error decoding JSON from {file_path}", name="JSONDecodeError", attachment_type=allure.attachment_type.TEXT)
        raise json.JSONDecodeError(f"Could not decode JSON from file: {file_path}", "", 0)
    except Exception as e:
        allure.attach(f"An unexpected error occurred while loading products: {str(e)}", name="LoadProductError", attachment_type=allure.attachment_type.TEXT)
        raise

# Load products once when the module is imported
_ALL_PRODUCTS = load_products_from_json()

@allure.step("Get product by name: {product_name}")
def get_product_by_name(product_name: str):
    """Retrieves a product from the loaded list by its name (case-insensitive)."""
    if not _ALL_PRODUCTS:
        allure.attach("Product list is empty. Cannot search by name.", name="EmptyProductList", attachment_type=allure.attachment_type.TEXT)
        return None
        
    for product in _ALL_PRODUCTS:
        if product.get('name', '').lower() == product_name.lower():
            allure.attach(f"Found product: {product_name}", name="ProductFoundByName", attachment_type=allure.attachment_type.JSON)
            return product
    allure.attach(f"Product with name '{product_name}' not found.", name="ProductNotFoundByName", attachment_type=allure.attachment_type.TEXT)
    return None

@allure.step("Get product by ID: {product_id}")
def get_product_by_id(product_id: str):
    """Retrieves a product from the loaded list by its ID."""
    if not _ALL_PRODUCTS:
        allure.attach("Product list is empty. Cannot search by ID.", name="EmptyProductList", attachment_type=allure.attachment_type.TEXT)
        return None

    for product in _ALL_PRODUCTS:
        if product.get('id') == product_id:
            allure.attach(f"Found product with ID: {product_id}", name="ProductFoundById", attachment_type=allure.attachment_type.JSON)
            return product
    allure.attach(f"Product with ID '{product_id}' not found.", name="ProductNotFoundById", attachment_type=allure.attachment_type.TEXT)
    return None

@allure.step("Get all products")
def get_all_products():
    """Returns the full list of loaded products."""
    return _ALL_PRODUCTS

# Example usage (optional, for testing this module directly)
if __name__ == '__main__':
    # This part will only run if you execute products.py directly
    print("Testing product data loading...")
    all_prods = get_all_products()
    print(f"Loaded {len(all_prods)} products.")
    
    product1_name = "Premium Wireless Headphones"
    product1 = get_product_by_name(product1_name)
    if product1:
        print(f"Found '{product1_name}': Price ${product1['price']}")
    else:
        print(f"'{product1_name}' not found.")

    product_id_to_find = "3"
    product3 = get_product_by_id(product_id_to_find)
    if product3:
        print(f"Found product ID '{product_id_to_find}': {product3['name']}")
    else:
        print(f"Product ID '{product_id_to_find}' not found.")

    non_existent_product = "Imaginary Gadget"
    product_ne = get_product_by_name(non_existent_product)
    if not product_ne:
        print(f"'{non_existent_product}' correctly reported as not found.")
