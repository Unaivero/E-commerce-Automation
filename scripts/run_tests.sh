#!/bin/bash
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if virtual environment is activated
check_venv() {
    if [[ "$VIRTUAL_ENV" == "" ]]; then
        print_warning "Virtual environment not activated. Activating..."
        if [ -f "venv/bin/activate" ]; then
            source venv/bin/activate
            print_success "Virtual environment activated"
        else
            print_error "Virtual environment not found. Run ./scripts/setup.sh first"
            exit 1
        fi
    else
        print_success "Virtual environment is active: $VIRTUAL_ENV"
    fi
}

# Function to run UI tests
run_ui_tests() {
    print_status "🖥️ Running UI Tests..."
    cd selenium-tests
    
    # Create reports directory if it doesn't exist
    mkdir -p ../reports/{allure,screenshots}
    
    # Run tests with various options
    pytest -v \
        --alluredir=../reports/allure \
        --html=../reports/ui-test-report.html \
        --self-contained-html \
        --tb=short \
        tests/
    
    local exit_code=$?
    cd ..
    
    if [ $exit_code -eq 0 ]; then
        print_success "UI tests completed successfully"
    else
        print_warning "Some UI tests failed (exit code: $exit_code)"
    fi
    
    return $exit_code
}

# Function to run specific test
run_specific_test() {
    local test_path=$1
    print_status "🎯 Running specific test: $test_path"
    cd selenium-tests
    
    pytest -v \
        --alluredir=../reports/allure \
        --tb=short \
        "$test_path"
    
    local exit_code=$?
    cd ..
    return $exit_code
}

# Function to run smoke tests
run_smoke_tests() {
    print_status "💨 Running Smoke Tests..."
    cd selenium-tests
    
    pytest -v \
        -m smoke \
        --alluredir=../reports/allure \
        --tb=short \
        tests/
    
    local exit_code=$?
    cd ..
    
    if [ $exit_code -eq 0 ]; then
        print_success "Smoke tests passed"
    else
        print_warning "Some smoke tests failed"
    fi
    
    return $exit_code
}

# Function to run API tests (if Newman is available)
run_api_tests() {
    print_status "🔌 Running API Tests..."
    
    if command -v newman &> /dev/null; then
        mkdir -p reports/api
        
        newman run postman-tests/E-Commerce_API_Tests.postman_collection.json \
            -e postman-tests/environments/qa.postman_environment.json \
            -r cli,junit,htmlextra \
            --reporter-junit-export reports/api/newman-results.xml \
            --reporter-htmlextra-export reports/api/newman-report.html \
            --color on
        
        if [ $? -eq 0 ]; then
            print_success "API tests completed successfully"
        else
            print_warning "Some API tests failed"
        fi
    else
        print_warning "Newman not found. Skipping API tests."
        print_status "Install Newman with: npm install -g newman newman-reporter-htmlextra"
    fi
}

# Function to generate reports
generate_reports() {
    print_status "📊 Generating test reports..."
    
    # Check if Allure is available
    if command -v allure &> /dev/null; then
        if [ -d "reports/allure" ] && [ "$(ls -A reports/allure)" ]; then
            allure generate reports/allure -o reports/allure-report --clean
            print_success "Allure report generated: reports/allure-report/index.html"
        else
            print_warning "No Allure results found to generate report"
        fi
    else
        print_warning "Allure not found. Install with: npm install -g allure-commandline"
    fi
    
    # List all available reports
    print_status "Available reports:"
    [ -f "reports/ui-test-report.html" ] && echo "  📋 UI Test Report: reports/ui-test-report.html"
    [ -f "reports/api/newman-report.html" ] && echo "  🔌 API Test Report: reports/api/newman-report.html"
    [ -d "reports/allure-report" ] && echo "  📈 Allure Report: reports/allure-report/index.html"
    [ -d "reports/screenshots" ] && [ "$(ls -A reports/screenshots)" ] && echo "  📸 Screenshots: reports/screenshots/"
}

# Function to clean reports
clean_reports() {
    print_status "🧹 Cleaning old reports..."
    rm -rf reports/allure/*
    rm -rf reports/allure-report/*
    rm -f reports/*.html
    rm -rf reports/api/*
    rm -f reports/screenshots/*
    print_success "Reports cleaned"
}

# Function to show usage
show_usage() {
    echo "Usage: $0 {ui|smoke|api|all|clean|specific} [test_path]"
    echo ""
    echo "Commands:"
    echo "  ui         Run all UI tests"
    echo "  smoke      Run smoke tests only"
    echo "  api        Run API tests (requires Newman)"
    echo "  all        Run all tests and generate reports"
    echo "  clean      Clean old reports"
    echo "  specific   Run a specific test (requires test_path)"
    echo ""
    echo "Examples:"
    echo "  $0 ui                                    # Run all UI tests"
    echo "  $0 smoke                                 # Run smoke tests"
    echo "  $0 specific tests/test_login.py          # Run specific test file"
    echo "  $0 specific tests/test_login.py::TestLogin::test_successful_login"
    echo ""
}

# Main execution
main() {
    print_status "🚀 E-Commerce QA Lab Test Runner"
    
    # Check virtual environment
    check_venv
    
    case "${1:-all}" in
        ui)
            run_ui_tests
            generate_reports
            ;;
        smoke)
            run_smoke_tests
            generate_reports
            ;;
        api)
            run_api_tests
            ;;
        specific)
            if [ -z "$2" ]; then
                print_error "Test path required for specific test"
                show_usage
                exit 1
            fi
            run_specific_test "$2"
            ;;
        clean)
            clean_reports
            ;;
        all)
            clean_reports
            run_smoke_tests
            run_ui_tests
            run_api_tests
            generate_reports
            print_success "✅ All tests completed!"
            ;;
        help|--help|-h)
            show_usage
            ;;
        *)
            print_error "Unknown command: $1"
            show_usage
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"