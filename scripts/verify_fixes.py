#!/usr/bin/env python3
"""
Verification script to test that the critical fixes are working.
This script validates the basic functionality without running full tests.
"""

import sys
import os
import importlib.util
from pathlib import Path

# Add the selenium-tests directory to the Python path
selenium_tests_dir = Path(__file__).parent.parent / "selenium-tests"
sys.path.insert(0, str(selenium_tests_dir))

def test_imports():
    """Test that all modules can be imported without errors."""
    print("🔍 Testing imports...")
    
    try:
        # Test configuration loading
        from utils.config import Config
        config = Config("chrome", "qa")
        print(f"✅ Config loaded: {config.base_url}")
        
        # Test page objects
        from pages.base_page import BasePage
        from pages.login_page import LoginPage
        from pages.product_page import ProductPage
        from pages.cart_page import CartPage
        from pages.search_results_page import SearchResultsPage
        print("✅ All page objects imported successfully")
        
        # Test test data
        from test_data.products import get_product_by_name, get_all_products
        products = get_all_products()
        print(f"✅ Test data loaded: {len(products)} products found")
        
        # Test specific product
        headphones = get_product_by_name("Premium Wireless Headphones")
        if headphones:
            print(f"✅ Test product found: {headphones['name']}")
        else:
            print("❌ Test product 'Premium Wireless Headphones' not found")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_configuration():
    """Test configuration loading and validation."""
    print("\n🔧 Testing configuration...")
    
    try:
        from utils.config import Config
        
        # Test different environments
        for env in ["dev", "qa", "prod"]:
            config = Config("chrome", env)
            print(f"✅ {env.upper()} environment: {config.base_url}")
            
            # Validate URLs are not example.com
            if "example.com" in config.base_url:
                print(f"❌ {env} still uses example.com URL")
                return False
                
        return True
        
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def test_method_compatibility():
    """Test that page object methods are compatible with base class."""
    print("\n🔗 Testing method compatibility...")
    
    try:
        from pages.base_page import BasePage
        from pages.login_page import LoginPage
        
        # Check that base page has the required methods
        base_methods = [
            'enter_text', 'click_element', 'get_element_text', 
            'is_element_visible', 'find_element', 'navigate_to'
        ]
        
        for method in base_methods:
            if not hasattr(BasePage, method):
                print(f"❌ BasePage missing method: {method}")
                return False
        
        print("✅ All required base methods exist")
        
        # Test that login page methods exist
        login_methods = [
            'login', 'get_error_message', 'is_logged_in', 
            'click_forgot_password', 'click_register'
        ]
        
        for method in login_methods:
            if not hasattr(LoginPage, method):
                print(f"❌ LoginPage missing method: {method}")
                return False
                
        print("✅ All login page methods exist")
        return True
        
    except Exception as e:
        print(f"❌ Method compatibility error: {e}")
        return False

def test_environment_files():
    """Test that required environment files exist."""
    print("\n📁 Testing environment files...")
    
    project_root = Path(__file__).parent.parent
    required_files = [
        ".env",
        "requirements.txt",
        ".gitignore",
        "selenium-tests/config.json"
    ]
    
    all_exist = True
    for file_path in required_files:
        full_path = project_root / file_path
        if full_path.exists():
            print(f"✅ {file_path} exists")
        else:
            print(f"❌ {file_path} missing")
            all_exist = False
    
    return all_exist

def main():
    """Run all verification tests."""
    print("🚀 Running E-Commerce QA Lab Verification Tests\n")
    
    tests = [
        ("Import Tests", test_imports),
        ("Configuration Tests", test_configuration),
        ("Method Compatibility Tests", test_method_compatibility),
        ("Environment Files Tests", test_environment_files)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*50)
    print("📊 VERIFICATION SUMMARY")
    print("="*50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\nResults: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\n🎉 All verification tests passed! Your fixes are working correctly.")
        print("\nNext steps:")
        print("1. Run setup script: ./scripts/setup.sh")
        print("2. Run a simple test: ./scripts/run_tests.sh smoke")
        return 0
    else:
        print(f"\n⚠️ {len(results) - passed} test(s) failed. Please review the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
