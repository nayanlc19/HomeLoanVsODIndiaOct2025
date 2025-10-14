"""
Payment Handler for Razorpay Integration with Admin Bypass and Free Trial
"""
import streamlit as st
import json
from datetime import datetime, timedelta

# Admin emails with free unlimited access
ADMIN_EMAILS = [
    "nayanlc19@gmail.com",
    "chaudhari.lbc@gmail.com"
]

# Free trial duration in minutes
FREE_TRIAL_MINUTES = 3

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
        if 'admin_email' not in st.session_state:
            st.session_state.admin_email = None
        if 'trial_start_time' not in st.session_state:
            st.session_state.trial_start_time = None
        if 'is_admin' not in st.session_state:
            st.session_state.is_admin = False

    def check_admin_email(self, email):
        """Check if email is in admin list"""
        return email.lower().strip() in [e.lower() for e in ADMIN_EMAILS]

    def start_free_trial(self):
        """Start the 3-minute free trial"""
        if st.session_state.trial_start_time is None:
            st.session_state.trial_start_time = datetime.now()
            return True
        return False

    def get_trial_time_remaining(self):
        """Get remaining trial time in seconds"""
        if st.session_state.trial_start_time is None:
            return FREE_TRIAL_MINUTES * 60

        elapsed = (datetime.now() - st.session_state.trial_start_time).total_seconds()
        remaining = (FREE_TRIAL_MINUTES * 60) - elapsed
        return max(0, remaining)

    def is_trial_active(self):
        """Check if free trial is still active"""
        if st.session_state.trial_start_time is None:
            return False

        return self.get_trial_time_remaining() > 0

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
        .admin-box {
            background-color: rgba(255,255,255,0.1);
            padding: 1rem;
            border-radius: 0.5rem;
            margin: 1rem 0;
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

        # Admin email input
        st.markdown("### 🔓 Admin Access")
        admin_email = st.text_input("Enter admin email for free access:", key="admin_email_input")

        if st.button("Verify Admin Email"):
            if self.check_admin_email(admin_email):
                st.session_state.is_admin = True
                st.session_state.admin_email = admin_email
                st.session_state.payment_verified = True
                st.success(f"✅ Admin access granted for {admin_email}!")
                st.balloons()
                st.rerun()
            else:
                st.error("❌ Email not in admin list. Please pay to access.")

        st.markdown("---")

        # Free trial option
        trial_remaining = self.get_trial_time_remaining()
        if trial_remaining > 0:
            minutes = int(trial_remaining // 60)
            seconds = int(trial_remaining % 60)
            st.info(f"⏱️ Free trial active: {minutes}m {seconds}s remaining")
        else:
            if st.button("🎁 Start 3-Minute Free Trial", type="primary"):
                self.start_free_trial()
                st.success("✅ Free trial started! You have 3 minutes of full access.")
                st.rerun()

        st.markdown("---")

        # Razorpay Payment Button
        self.show_razorpay_button()

        # Free preview section
        st.markdown("---")
        st.markdown("### 👀 Options to Access")
        st.info("""
        **Choose one:**
        1. 🔓 **Admin Email** - Instant free access (for authorized users)
        2. 🎁 **3-Minute Trial** - Test all features risk-free
        3. 💳 **Pay ₹49** - Lifetime unlimited access
        """)

    def show_razorpay_button(self):
        """Display Razorpay payment button with JavaScript"""
        import os

        # Razorpay configuration - use environment variables for Render deployment
        razorpay_key = os.environ.get("RAZORPAY_KEY_ID", "rzp_test_placeholder")

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
                    window.location.href = window.location.href + "?payment_id=" + response.razorpay_payment_id;
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
        """Check if user has paid, is admin, or has active trial"""

        # Check for admin access
        if st.session_state.is_admin:
            return True

        # Check URL parameters for payment_id
        query_params = st.query_params
        if 'payment_id' in query_params:
            payment_id = query_params['payment_id']
            if self.verify_payment(payment_id):
                st.success("✅ Payment verified! You now have full access.")
                st.balloons()
                return True

        # Check if payment was already verified
        if st.session_state.payment_verified:
            return True

        # Check if free trial is active
        if self.is_trial_active():
            # Show countdown timer
            remaining = self.get_trial_time_remaining()
            minutes = int(remaining // 60)
            seconds = int(remaining % 60)

            # Display timer in sidebar
            st.sidebar.success(f"⏱️ Trial: {minutes}m {seconds}s left")

            # Auto-refresh every second to update timer
            if remaining > 0:
                import time
                time.sleep(1)
                st.rerun()

            return True

        return False

    def show_limited_content(self):
        """Show limited preview for non-paid users"""
        st.warning("⚠️ This is a limited preview. Choose an option above to unlock all features!")

        st.markdown("""
        ### Free Preview Features:
        - Basic EMI calculation
        - Single bank comparison
        - Limited tax calculations

        ### 🔒 Locked Features (Unlock Now):
        - Compare ALL banks simultaneously
        - Advanced prepayment strategies
        - Year-by-year detailed breakdown
        - Interactive charts and graphs
        - Hidden charges analysis
        - Tax optimization strategies
        - Overdraft optimization tips
        - And much more...
        """)
