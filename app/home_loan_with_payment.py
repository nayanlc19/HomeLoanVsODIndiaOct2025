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

# Check if user has paid or has active trial
has_access = payment.check_access()

if not has_access:
    # BLOCK ACCESS - Show payment wall first with screenshot preview
    st.markdown('<div class="main-header">🏠 Home Loan: EMI vs Overdraft Comparison</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Professional Tool to Compare Regular Home Loans with Overdraft Facilities</div>', unsafe_allow_html=True)

    # Add custom CSS for styling
    st.markdown("""
    <style>
        .main-header {
            font-size: 2.5rem;
            font-weight: bold;
            color: #2E7D32;
            text-align: center;
            margin-bottom: 1rem;
        }
        .sub-header {
            font-size: 1.2rem;
            color: #666;
            text-align: center;
            margin-bottom: 2rem;
        }
    </style>
    """, unsafe_allow_html=True)

    # Show payment wall
    payment.show_payment_wall()

    # Show screenshot preview of the tool
    st.markdown("---")
    st.markdown("## 👀 See What You Get:")

    # Embed screenshot or demo image
    screenshot_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "app_preview.png")

    if os.path.exists(screenshot_path):
        st.image(screenshot_path, use_column_width=True, caption="Full-featured home loan comparison tool")
    else:
        # If no screenshot exists, show feature list
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            ### ✅ What's Included:
            - 🏦 Compare 6+ major banks
            - 💰 Regular EMI vs Overdraft analysis
            - 📊 Year-by-year breakdown
            - 💳 Tax benefit calculations
            - 📈 Interactive charts & graphs
            - 🎯 Prepayment strategies
            """)

        with col2:
            st.markdown("""
            ### 🔥 Advanced Features:
            - 🎯 Custom interest rate testing
            - 💡 Hidden charges analysis
            - ⏱️ Loan process timeline
            - 🚨 Common pitfalls & solutions
            - 💰 Surplus parking optimizer
            - ✅ Smart decision framework
            """)

    st.markdown("---")
    st.info("👆 Choose any option above to unlock full access!")

    # Show admin access in footer
    payment.show_admin_footer()

    # Stop execution - don't load the app
    st.stop()

# User has access - load the full app
app_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "home_loan_comparison_app.py")
with open(app_path, 'r', encoding='utf-8') as f:
    exec(f.read())
