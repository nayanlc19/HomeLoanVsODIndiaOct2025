"""
Payment Handler for Razorpay Integration with Admin Bypass and Free Trial
"""
import streamlit as st
import json
from datetime import datetime, timedelta
import hashlib

# Admin emails with free unlimited access
ADMIN_EMAILS = [
    "nayanlc19@gmail.com",
    "chaudhari.lbc@gmail.com"
]

# Free trial duration in minutes
FREE_TRIAL_MINUTES = 3

# Maximum number of trials per IP address
MAX_TRIALS_PER_IP = 5

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
        if 'trial_count' not in st.session_state:
            st.session_state.trial_count = 0
        if 'trial_history' not in st.session_state:
            st.session_state.trial_history = []  # Store completed trial timestamps

    def check_admin_email(self, email):
        """Check if email is in admin list"""
        return email.lower().strip() in [e.lower() for e in ADMIN_EMAILS]

    def can_start_trial(self):
        """Check if user can start a new trial"""
        return st.session_state.trial_count < MAX_TRIALS_PER_IP

    def get_remaining_trials(self):
        """Get number of trials remaining"""
        return MAX_TRIALS_PER_IP - st.session_state.trial_count

    def start_free_trial(self):
        """Start the 3-minute free trial"""
        if self.can_start_trial() and st.session_state.trial_start_time is None:
            st.session_state.trial_start_time = datetime.now()
            return True
        return False

    def end_trial(self):
        """End current trial and increment counter"""
        if st.session_state.trial_start_time is not None:
            st.session_state.trial_history.append(st.session_state.trial_start_time)
            st.session_state.trial_count += 1
            st.session_state.trial_start_time = None

    def get_trial_time_remaining(self):
        """Get remaining trial time in seconds"""
        if st.session_state.trial_start_time is None:
            return 0

        elapsed = (datetime.now() - st.session_state.trial_start_time).total_seconds()
        remaining = (FREE_TRIAL_MINUTES * 60) - elapsed

        # Auto-end trial if time expired
        if remaining <= 0:
            self.end_trial()
            return 0

        return max(0, remaining)

    def is_trial_active(self):
        """Check if free trial is still active"""
        if st.session_state.trial_start_time is None:
            return False

        remaining = self.get_trial_time_remaining()
        if remaining <= 0:
            return False

        return True

    def show_payment_wall(self):
        """Display compact payment wall for unpaid users"""
        st.markdown("""
        <style>
        .compact-payment {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 1.5rem;
            border-radius: 0.75rem;
            color: white;
            margin: 1rem 0;
        }
        .compact-price {
            font-size: 1.2rem;
            font-weight: 600;
            display: inline-block;
            margin: 0;
        }
        </style>
        """, unsafe_allow_html=True)

        st.markdown('<div class="compact-payment">', unsafe_allow_html=True)
        st.markdown('<p style="color: white; margin-bottom: 0.5rem;">🔒 <strong>Unlock Full Access</strong> to compare all banks, see detailed breakdowns, tax strategies & save lakhs!</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Three columns for options
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("**🔓 Admin Access**")
            admin_email = st.text_input("Email:", key="admin_email_input", label_visibility="collapsed", placeholder="Admin email")
            if st.button("Verify", key="verify_admin"):
                if self.check_admin_email(admin_email):
                    st.session_state.is_admin = True
                    st.session_state.admin_email = admin_email
                    st.session_state.payment_verified = True
                    st.success("✅ Access granted!")
                    st.rerun()
                else:
                    st.error("❌ Not authorized")

        with col2:
            st.markdown("**🎁 Free Trials**")
            trial_remaining = self.get_trial_time_remaining()
            trials_left = self.get_remaining_trials()

            if trial_remaining > 0:
                minutes = int(trial_remaining // 60)
                seconds = int(trial_remaining % 60)
                st.info(f"⏱️ {minutes}m {seconds}s left")
            else:
                if trials_left > 0:
                    if st.button(f"Start Trial ({trials_left}/5 left)", key="start_trial", type="primary"):
                        if self.start_free_trial():
                            st.success(f"✅ Trial {st.session_state.trial_count + 1} started!")
                            st.rerun()
                else:
                    st.error("No trials left")

        with col3:
            st.markdown("**💳 Pay Once**")
            st.markdown("₹49 only • Lifetime")
            # Razorpay button will be shown below

        # Razorpay Payment Button (compact version)
        self.show_razorpay_button_compact()

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

    def show_razorpay_button_compact(self):
        """Display compact Razorpay payment button"""
        import os

        razorpay_key = os.environ.get("RAZORPAY_KEY_ID", "rzp_test_placeholder")

        razorpay_html = f"""
        <script src="https://checkout.razorpay.com/v1/checkout.js"></script>
        <script>
        function initiatePayment() {{
            var options = {{
                "key": "{razorpay_key}",
                "amount": "4900",
                "currency": "INR",
                "name": "Home Loan Comparison",
                "description": "Lifetime Access",
                "handler": function (response) {{
                    window.location.href = window.location.href + "?payment_id=" + response.razorpay_payment_id;
                }},
                "theme": {{"color": "#2E7D32"}}
            }};
            var rzp = new Razorpay(options);
            rzp.open();
        }}
        </script>
        <div style="text-align: center; margin: 0.5rem 0;">
            <button onclick="initiatePayment()" style="background: #2E7D32; color: white; border: none; padding: 0.5rem 1.5rem; border-radius: 0.5rem; cursor: pointer; font-size: 1rem;">
                Pay ₹49 Now
            </button>
        </div>
        """

        st.components.v1.html(razorpay_html, height=80)

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
            # Show countdown timer in sidebar (without auto-refresh)
            remaining = self.get_trial_time_remaining()
            minutes = int(remaining // 60)
            seconds = int(remaining % 60)

            # Display timer in sidebar
            st.sidebar.success(f"⏱️ Trial: {minutes}m {seconds}s left")

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
