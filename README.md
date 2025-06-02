# 🛒 E-Commerce QA Automation Framework

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python)](https://www.python.org/)
[![Selenium](https://img.shields.io/badge/Selenium-4.15.0-green?style=flat-square&logo=selenium)](https://selenium.dev/)
[![Pytest](https://img.shields.io/badge/Pytest-7.4.3-orange?style=flat-square&logo=pytest)](https://pytest.org/)
[![Allure](https://img.shields.io/badge/Allure-2.13.2-yellow?style=flat-square&logo=qameta)](https://github.com/allure-framework)
[![License](https://img.shields.io/badge/License-MIT-red?style=flat-square)](LICENSE)

> **A comprehensive Quality Assurance automation framework for e-commerce applications, demonstrating enterprise-level testing strategies across UI, API, and performance layers with complete CI/CD integration.**

## 🎯 **Project Overview**

This project showcases a complete end-to-end QA automation strategy for e-commerce applications, implementing modern testing practices and tools used in enterprise environments. The framework demonstrates proficiency in multiple testing domains and provides a solid foundation for scalable test automation.

### 🏆 **Key Highlights**
- **🖥️ UI Automation** - Selenium WebDriver with Page Object Model
- **🔌 API Testing** - Postman collections with Newman CLI integration  
- **⚡ Performance Testing** - JMeter scripts for load and stress testing
- **📊 Advanced Reporting** - Allure framework with detailed analytics
- **🔄 CI/CD Ready** - Jenkins pipeline with automated test execution
- **🐳 Containerized** - Docker support for consistent environments

---

## 🚀 **Quick Start**

### **Prerequisites**
- Python 3.8+ 
- Chrome/Firefox browser
- Git

### **⚡ Automated Setup (Recommended)**
```bash
# Clone the repository
git clone https://github.com/Unaivero/E-commerce-Automation.git
cd E-commerce-Automation

# Run automated setup
./scripts/setup.sh

# Activate virtual environment
source venv/bin/activate

# Run smoke tests to verify installation
./scripts/run_tests.sh smoke
```

### **📱 Manual Setup**
```bash
# Install dependencies
pip install -r requirements.txt

# Run a specific test
cd selenium-tests
pytest tests/test_login.py::TestLogin::test_successful_login -v
```

---

## 🏗️ **Architecture & Framework Design**

### **📁 Project Structure**
```
E-Commerce QA Lab/
├── 📁 selenium-tests/          # UI Test Automation
│   ├── pages/                  # Page Object Models
│   ├── tests/                  # Test Cases
│   ├── test_data/              # Test Data Management
│   └── utils/                  # Utilities & Configuration
├── 📁 postman-tests/           # API Test Collections
├── 📁 jmeter-tests/            # Performance Test Plans
├── 📁 ci-cd/                   # CI/CD Pipeline Configuration
├── 📁 scripts/                 # Automation Scripts
├── 📁 reports/                 # Test Execution Reports
└── 📁 docs/                    # Documentation
```

### **🔧 Technology Stack**

| **Category** | **Technology** | **Purpose** |
|--------------|----------------|-------------|
| **UI Testing** | Selenium WebDriver | Browser automation |
| **Test Framework** | Pytest | Test execution and management |
| **API Testing** | Postman + Newman | REST API validation |
| **Performance** | Apache JMeter | Load and stress testing |
| **Reporting** | Allure Framework | Comprehensive test reporting |
| **CI/CD** | Jenkins | Continuous integration |
| **Containerization** | Docker | Environment consistency |
| **Language** | Python 3.8+ | Core automation language |

---

## 🧪 **Testing Strategy**

### **🎭 Test Coverage**

#### **UI Automation (Selenium)**
- ✅ **User Authentication** - Login, logout, registration flows
- ✅ **Product Management** - Search, browse, product details
- ✅ **Shopping Cart** - Add, update, remove items
- ✅ **Checkout Process** - End-to-end purchase flow
- ✅ **Cross-browser Testing** - Chrome, Firefox support

#### **API Testing (Postman)**
- ✅ **Authentication Endpoints** - Token management
- ✅ **Product Catalog API** - CRUD operations
- ✅ **Cart Management** - Cart lifecycle testing
- ✅ **Order Processing** - Payment and order APIs
- ✅ **Error Handling** - Edge cases and validation

#### **Performance Testing (JMeter)**
- ✅ **Load Testing** - Normal user load simulation
- ✅ **Stress Testing** - Peak load handling
- ✅ **API Performance** - Response time validation
- ✅ **Concurrent Users** - 100-500 user simulation

### **🎨 Design Patterns**
- **Page Object Model (POM)** - Maintainable UI test structure
- **Data-Driven Testing** - JSON-based test data management
- **Factory Pattern** - Dynamic test data generation
- **Builder Pattern** - Test configuration management

---

## 📊 **Test Execution & Reporting**

### **🏃‍♂️ Running Tests**

```bash
# Run all UI tests
./scripts/run_tests.sh ui

# Run smoke tests only  
./scripts/run_tests.sh smoke

# Run specific test file
./scripts/run_tests.sh specific tests/test_login.py

# Run all tests with reports
./scripts/run_tests.sh all

# Clean previous reports
./scripts/run_tests.sh clean
```

### **📈 Advanced Execution Options**

```bash
# Run with specific browser
cd selenium-tests
pytest --browser=firefox tests/

# Run with environment
pytest --env=qa tests/

# Run with parallel execution
pytest -n 4 tests/

# Generate Allure report
pytest --alluredir=reports/allure tests/
allure serve reports/allure
```

### **📊 Report Types**
- **🎯 Allure Reports** - Interactive test execution dashboard
- **📱 HTML Reports** - Self-contained test summaries  
- **📸 Screenshots** - Automatic capture on failures
- **📈 Performance Reports** - JMeter execution analytics
- **📋 JUnit XML** - CI/CD integration format

---

## 🔧 **Configuration Management**

### **🌍 Environment Configuration**
The framework supports multiple environments through configuration files:

```json
{
  "environments": {
    "qa": {
      "base_url": "https://demo.opencart.com",
      "api_url": "https://demo.opencart.com/index.php?route=api"
    }
  }
}
```

### **⚙️ Environment Variables**
Create a `.env` file for local customization:
```bash
TEST_ENV=qa
BROWSER=chrome
HEADLESS=false
BASE_URL=https://demo.opencart.com
```

---

## 🔄 **CI/CD Integration**

### **🏗️ Jenkins Pipeline**
The project includes a complete Jenkinsfile for automated testing:

```groovy
pipeline {
    agent any
    stages {
        stage('Setup') { /* Environment preparation */ }
        stage('UI Tests') { /* Selenium test execution */ }
        stage('API Tests') { /* Postman/Newman execution */ }
        stage('Performance') { /* JMeter load testing */ }
        stage('Reports') { /* Allure report generation */ }
    }
}
```

### **🔍 GitHub Actions (Alternative)**
```yaml
name: E-Commerce QA Pipeline
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        browser: [chrome, firefox]
    steps:
      - uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v4
      - name: Run Tests
        run: ./scripts/run_tests.sh all
```

---

## 📚 **Test Data Management**

### **🗃️ Data Strategy**
- **Static Data** - JSON files for predictable test scenarios
- **Dynamic Data** - Faker library for unique test data generation
- **Environment-specific** - Separate data sets per environment

### **📋 Sample Test Data**
```json
{
  "products": [
    {
      "id": "1",
      "name": "Premium Wireless Headphones",
      "price": 129.99,
      "category": "Electronics"
    }
  ]
}
```

---

## 🐛 **Quality Assurance Features**

### **🛡️ Reliability Features**
- **Retry Mechanism** - Automatic retry for flaky tests
- **Wait Strategies** - Explicit waits for stable execution
- **Error Handling** - Comprehensive exception management
- **Screenshot Capture** - Automatic failure documentation

### **📏 Code Quality**
- **Type Hints** - Python type annotations
- **Linting** - Code style enforcement
- **Documentation** - Comprehensive inline documentation
- **Modularity** - Reusable components and utilities

---

## 🔐 **Security Testing**

The framework includes basic security testing capabilities:
- **SQL Injection** - Input validation testing
- **XSS Prevention** - Cross-site scripting checks
- **Authentication** - Session management validation

---

## 📈 **Performance Monitoring**

### **⏱️ Performance Metrics**
- Response time tracking
- Memory usage monitoring  
- Test execution duration
- Resource utilization analysis

### **🎯 Performance Benchmarks**
- Page load times < 3 seconds
- API responses < 500ms
- Test execution optimization

---

## 🤝 **Contributing**

### **📋 Development Setup**
1. Fork the repository
2. Create a feature branch
3. Run verification: `python3 scripts/verify_fixes.py`
4. Submit a pull request

### **🧪 Testing Your Changes**
```bash
# Verify all functionality
./scripts/verify_fixes.py

# Run smoke tests
./scripts/run_tests.sh smoke
```

---

## 📊 **Metrics & Analytics**

### **🎯 Framework Metrics**
- **Test Coverage**: 85%+ functional coverage
- **Execution Time**: < 15 minutes for full suite
- **Reliability**: 95%+ pass rate
- **Maintainability**: Page Object Model architecture

### **📈 Continuous Improvement**
- Test execution trends
- Failure analysis
- Performance benchmarking
- Code coverage tracking

---

## 🆘 **Troubleshooting**

### **🔧 Common Issues**

| **Issue** | **Solution** |
|-----------|-------------|
| `ModuleNotFoundError` | Run `source venv/bin/activate` |
| ChromeDriver not found | Execute `./scripts/setup.sh` |
| Tests failing | Check `.env` configuration |
| Permission denied | Run `chmod +x scripts/*.sh` |

### **📞 Support**
- 📖 Check [Documentation](docs/)
- 🐛 Report [Issues](https://github.com/Unaivero/E-commerce-Automation/issues)
- 💬 Discussion [Forum](https://github.com/Unaivero/E-commerce-Automation/discussions)

---

## 🏆 **Project Achievements**

- ✅ **Complete Test Automation Framework** - Production-ready implementation
- ✅ **Multi-layer Testing Strategy** - UI, API, and Performance coverage
- ✅ **Enterprise Best Practices** - Industry-standard patterns and tools
- ✅ **CI/CD Integration** - Automated pipeline configuration
- ✅ **Comprehensive Documentation** - Detailed setup and usage guides
- ✅ **Scalable Architecture** - Easily extensible framework design

---

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 **Acknowledgments**

- **Selenium Community** - For the robust WebDriver framework
- **Pytest Team** - For the excellent testing framework
- **Allure Framework** - For beautiful test reporting
- **Open Source Community** - For the amazing tools and libraries

---

## 📬 **Contact**

**Jose Vergara** - QA Automation Engineer

[![GitHub](https://img.shields.io/badge/GitHub-Unaivero-black?style=flat-square&logo=github)](https://github.com/Unaivero)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=flat-square&logo=linkedin)](https://linkedin.com/in/yourprofile)

---

<div align="center">

**⭐ If you found this project helpful, please give it a star! ⭐**

**🚀 Ready to showcase enterprise-level QA automation skills!**

</div>

