import os
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for test environment settings"""
    
    def __init__(self, browser, env):
        self.browser = browser
        self.env = env
        self._config = self._load_config()
        
    def _load_config(self):
        """Load configuration from config.json file"""
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')
        
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Return default config if file not found
            return {
                "environments": {
                    "dev": {
                        "base_url": "http://dev-ecommerce.example.com",
                        "api_url": "http://dev-api.example.com"
                    },
                    "qa": {
                        "base_url": "http://qa-ecommerce.example.com",
                        "api_url": "http://qa-api.example.com"
                    },
                    "prod": {
                        "base_url": "http://ecommerce.example.com",
                        "api_url": "http://api.example.com"
                    }
                },
                "timeouts": {
                    "implicit_wait": 10,
                    "page_load": 30,
                    "script": 30
                },
                "test_data": {
                    "admin_user": {
                        "username": "admin@example.com",
                        "password": "admin123"
                    }
                }
            }
    
    @property
    def base_url(self):
        """Get base URL for the current environment"""
        return os.getenv('BASE_URL') or self._config['environments'][self.env]['base_url']
    
    @property
    def api_url(self):
        """Get API URL for the current environment"""
        return os.getenv('API_URL') or self._config['environments'][self.env]['api_url']
    
    @property
    def implicit_wait(self):
        """Get implicit wait timeout"""
        return int(os.getenv('IMPLICIT_WAIT') or self._config['timeouts']['implicit_wait'])
    
    @property
    def page_load_timeout(self):
        """Get page load timeout"""
        return int(os.getenv('PAGE_LOAD_TIMEOUT') or self._config['timeouts']['page_load'])
    
    @property
    def script_timeout(self):
        """Get script timeout"""
        return int(os.getenv('SCRIPT_TIMEOUT') or self._config['timeouts']['script'])
    
    def get_credentials(self, user_type='admin_user'):
        """Get credentials for the specified user type"""
        username = os.getenv(f'{user_type.upper()}_USERNAME') or self._config['test_data'][user_type]['username']
        password = os.getenv(f'{user_type.upper()}_PASSWORD') or self._config['test_data'][user_type]['password']
        return {'username': username, 'password': password}