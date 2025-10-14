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

# Check if user has paid
has_access = payment.check_access()

if not has_access:
    # Show payment wall for non-paid users
    st.markdown('<div class="main-header">🏠 Home Loan: EMI vs Overdraft Comparison</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Professional Tool to Compare Regular Home Loans with Overdraft Facilities</div>', unsafe_allow_html=True)

    payment.show_payment_wall()
    payment.show_limited_content()

    st.stop()  # Stop execution here if not paid

# If user has paid, load the full app
app_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "home_loan_comparison_app.py")
with open(app_path, 'r', encoding='utf-8') as f:
    exec(f.read())
