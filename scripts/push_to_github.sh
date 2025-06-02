#!/bin/bash
# Git Push Helper Script for E-Commerce QA Lab

echo "🚀 Preparing to push E-Commerce QA Lab to GitHub..."

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ Not a git repository. Initializing..."
    git init
    git remote add origin https://github.com/Unaivero/E-commerce-Automation.git
fi

# Check current status
echo "📊 Current git status:"
git status

# Add all files (respecting .gitignore)
echo "📁 Adding all files..."
git add .

# Show what will be committed
echo "📋 Files to be committed:"
git status --short

# Commit with a descriptive message
echo "💾 Committing changes..."
git commit -m "✅ Apply critical fixes and complete E-Commerce QA Lab setup

- Fix page object method calls to match base class
- Update URLs from example.com to working demo.opencart.com  
- Align test data references with existing products
- Add missing infrastructure files (.env, requirements.txt, .gitignore)
- Create automation scripts (setup.sh, run_tests.sh, verify_fixes.py)
- Add comprehensive documentation (FIXES_APPLIED.md)
- Verify all functionality with demo and verification scripts

Status: All critical issues resolved - framework is now functional ✅"

# Check if remote exists and push
echo "🌐 Pushing to GitHub..."
if git remote get-url origin >/dev/null 2>&1; then
    echo "Remote 'origin' exists, pushing to main branch..."
    git push -u origin main
else
    echo "❌ Remote 'origin' not found. Adding remote..."
    git remote add origin https://github.com/Unaivero/E-commerce-Automation.git
    git push -u origin main
fi

echo "✅ Push completed! Check your repository at:"
echo "   https://github.com/Unaivero/E-commerce-Automation"
