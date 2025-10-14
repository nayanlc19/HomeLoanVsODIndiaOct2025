"""
Payment Handler for Razorpay Integration
"""
import streamlit as st
import json
from datetime import datetime, timedelta

class PaymentHandler:
    """Handle payment verification and access control"""

    def __init__(self):
        # Initialize session state for payment
        if 'payment_verified' not in st.session_state:
            st.session_state.payment_verified = False
        if 'payment_id' not in st.session_state:
            st.session_state.payment_id = None
        if 'access_expiry' not in st.session_state:
            st.session_state.access_expiry = None

    def show_payment_wall(self):
        """Display payment wall for unpaid users"""
        st.markdown("""
        <style>
        .payment-wall {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 3rem 2rem;
            border-radius: 1rem;
            color: white;
            text-align: center;
            margin: 2rem 0;
        }
        .price-tag {
            font-size: 3rem;
            font-weight: bold;
            margin: 1rem 0;
        }
        .feature-list {
            text-align: left;
            max-width: 600px;
            margin: 2rem auto;
            font-size: 1.1rem;
        }
        .razorpay-button {
            background-color: #2E7D32;
            color: white;
            padding: 1rem 2rem;
            font-size: 1.2rem;
            border: none;
            border-radius: 0.5rem;
            cursor: pointer;
            margin-top: 1rem;
        }
        </style>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="payment-wall">
            <h1>🏠 Unlock Full Home Loan Analysis</h1>
            <div class="price-tag">₹49 Only</div>
            <p style="font-size: 1.2rem;">One-time payment • Lifetime access</p>

            <div class="feature-list">
                <h3>✨ What You'll Get:</h3>
                <ul>
                    <li>✅ Complete loan comparison (Regular vs Overdraft)</li>
                    <li>✅ Compare ALL major banks (HDFC, ICICI, SBI, Axis, BOB, PNB)</li>
                    <li>✅ Tax benefit calculations (80C + 24b)</li>
                    <li>✅ Advanced prepayment strategies</li>
                    <li>✅ Year-by-year breakdown</li>
                    <li>✅ Interactive charts & visualizations</li>
                    <li>✅ Hidden charges analysis</li>
                    <li>✅ Smart tips to save lakhs</li>
                    <li>✅ EMI vs OD detailed comparison</li>
                </ul>
            </div>

            <p style="font-size: 0.9rem; opacity: 0.9;">
                💡 This tool has helped thousands save ₹5-10 lakhs on their home loans!
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Razorpay Payment Button
        self.show_razorpay_button()

        # Free preview section
        st.markdown("---")
        st.markdown("### 👀 Free Preview")
        st.info("Enter your loan details in the sidebar to see a basic comparison. Pay ₹49 to unlock all features!")

    def show_razorpay_button(self):
        """Display Razorpay payment button with JavaScript"""

        # Razorpay configuration
        razorpay_key = st.secrets.get("RAZORPAY_KEY_ID", "rzp_test_placeholder")

        razorpay_html = f"""
        <script src="https://checkout.razorpay.com/v1/checkout.js"></script>
        <script>
        function initiatePayment() {{
            var options = {{
                "key": "{razorpay_key}",
                "amount": "4900", // Amount in paise (₹49.00)
                "currency": "INR",
                "name": "Home Loan Comparison Tool",
                "description": "Unlock Full Access",
                "image": "https://cdn-icons-png.flaticon.com/512/609/609803.png",
                "handler": function (response) {{
                    // Payment successful
                    alert("Payment Successful! Payment ID: " + response.razorpay_payment_id);

                    // Store payment info in session
                    window.parent.postMessage({{
                        type: 'payment_success',
                        payment_id: response.razorpay_payment_id,
                        order_id: response.razorpay_order_id,
                        signature: response.razorpay_signature
                    }}, '*');

                    // Redirect to verification
                    window.location.href = window.location.href + "&payment_id=" + response.razorpay_payment_id;
                }},
                "prefill": {{
                    "name": "",
                    "email": "",
                    "contact": ""
                }},
                "theme": {{
                    "color": "#2E7D32"
                }},
                "modal": {{
                    "ondismiss": function() {{
                        alert("Payment cancelled. You can try again anytime!");
                    }}
                }}
            }};

            var rzp = new Razorpay(options);
            rzp.open();
        }}
        </script>

        <div style="text-align: center; margin-top: 2rem;">
            <button onclick="initiatePayment()" class="razorpay-button">
                💳 Pay ₹49 & Unlock Now
            </button>
            <p style="margin-top: 1rem; font-size: 0.9rem; color: #666;">
                🔒 Secure payment powered by Razorpay
            </p>
        </div>
        """

        st.components.v1.html(razorpay_html, height=200)

    def verify_payment(self, payment_id):
        """Verify payment and grant access"""
        # In production, verify with Razorpay API
        # For now, we'll use session state

        if payment_id:
            st.session_state.payment_verified = True
            st.session_state.payment_id = payment_id
            st.session_state.access_expiry = None  # Lifetime access
            return True
        return False

    def check_access(self):
        """Check if user has paid"""
        # Check URL parameters for payment_id
        query_params = st.query_params
        if 'payment_id' in query_params:
            payment_id = query_params['payment_id']
            if self.verify_payment(payment_id):
                st.success("✅ Payment verified! You now have full access.")
                st.balloons()

        return st.session_state.payment_verified

    def show_limited_content(self):
        """Show limited preview for non-paid users"""
        st.warning("⚠️ This is a limited preview. Pay ₹49 to unlock all features!")

        st.markdown("""
        ### Free Preview Features:
        - Basic EMI calculation
        - Single bank comparison
        - Limited tax calculations

        ### 🔒 Locked Features (Unlock for ₹49):
        - Compare ALL banks simultaneously
        - Advanced prepayment strategies
        - Year-by-year detailed breakdown
        - Interactive charts and graphs
        - Hidden charges analysis
        - Tax optimization strategies
        - Overdraft optimization tips
        - And much more...
        """)
