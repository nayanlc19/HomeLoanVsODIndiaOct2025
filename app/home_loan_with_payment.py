"""
Home Loan Comparison Tool with Razorpay Payment Integration
"""
import streamlit as st
import sys
import os

# Add the app directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from payment_handler import PaymentHandler

# Page configuration
st.set_page_config(
    page_title="Home Loan: EMI vs Overdraft Comparison",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize payment handler
payment = PaymentHandler()

# Check if user has paid (but don't block - just track)
has_full_access = payment.check_access()

# ALWAYS load the full app first - let users explore
app_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "home_loan_comparison_app.py")
with open(app_path, 'r', encoding='utf-8') as f:
    exec(f.read())

# Show payment prompt at the END if user doesn't have access
if not has_full_access:
    st.markdown("---")
    st.markdown("## 🎉 Enjoying the tool? Unlock Premium Features!")

    payment.show_payment_wall()
