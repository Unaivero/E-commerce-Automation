#!/bin/bash
set -e

echo "🚀 Setting up E-Commerce QA Lab..."

# Check if we're in the right directory
if [ ! -f "requirements.txt" ]; then
    echo "❌ Please run this script from the project root directory"
    exit 1
fi

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "Please install Python 3.8+ and try again."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
else
    echo "📦 Virtual environment already exists"
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Create reports directories
echo "📁 Creating reports directories..."
mkdir -p reports/{screenshots,allure,jmeter,html}

# Verify Selenium setup
echo "🌐 Verifying Selenium setup..."
python -c "
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

print('Installing/updating ChromeDriver...')
service = Service(ChromeDriverManager().install())
print('✅ ChromeDriver setup complete')
"

# Check if .env exists, if not copy from template
if [ ! -f ".env" ]; then
    echo "⚙️ Environment file not found. Please check the .env file and customize it for your needs."
else
    echo "✅ Environment file found"
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Customize the .env file if needed"
echo "3. Run a simple test: cd selenium-tests && pytest tests/test_login.py::TestLogin::test_successful_login -v"
echo ""
echo "For more information, see the README.md file"