@echo off
echo ========================================
echo Home Loan App Deployment Script
echo ========================================
echo.

cd /d D:\Claude\home_loan_comparison_tool

echo Step 1: Authenticating with GitHub...
echo.
gh auth login
echo.

echo Step 2: Creating repository and pushing code...
echo.
gh repo create HomeLoanVsODIndiaOct2025 --public --description "Comprehensive Home Loan Comparison Tool for India - Regular EMI vs Overdraft. Real bank data Oct 2025" --source=. --remote=origin --push
echo.

echo ========================================
echo SUCCESS! Your code is now on GitHub!
echo ========================================
echo.

echo Repository URL:
gh repo view --json url --jq .url
echo.

echo ========================================
echo NEXT STEP: Deploy to Streamlit Cloud
echo ========================================
echo.
echo 1. Go to: https://share.streamlit.io
echo 2. Click "Sign in" with GitHub
echo 3. Click "New app"
echo 4. Fill in:
echo    - Repository: HomeLoanVsODIndiaOct2025
echo    - Branch: main
echo    - Main file: app/home_loan_comparison_app.py
echo 5. Click "Deploy!"
echo.
echo Your app will be live at:
echo https://HomeLoanVsODIndiaOct2025.streamlit.app
echo.

echo Opening Streamlit Cloud in browser...
start https://share.streamlit.io
echo.

pause
