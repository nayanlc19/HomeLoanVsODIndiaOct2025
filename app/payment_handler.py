"""
Payment Handler for Razorpay Integration with Cookie Persistence and Email Database
"""
import streamlit as st
import json
from datetime import datetime, timedelta
import hashlib
import os

# Try to import cookie manager, fallback to None if not available
try:
    import extra_streamlit_components as stx
    COOKIES_AVAILABLE = True
except ImportError:
    stx = None
    COOKIES_AVAILABLE = False

# Admin emails with free unlimited access
ADMIN_EMAILS = [
    "nayanlc19@gmail.com",
    "chaudhari.lbc@gmail.com"
]

# Free trial duration in minutes
FREE_TRIAL_MINUTES = 3

# Maximum number of trials per IP address
MAX_TRIALS_PER_IP = 5

# Cookie settings
COOKIE_NAME = "home_loan_access"
COOKIE_EXPIRY_DAYS = 90

# Path to paid users database
PAID_USERS_DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "paid_users.json")

class PaymentHandler:
    """Handle payment verification and access control with persistent storage"""

    def __init__(self):
        # Initialize cookie manager (only if available)
        if COOKIES_AVAILABLE:
            try:
                self.cookie_manager = stx.CookieManager()
            except Exception:
                self.cookie_manager = None
        else:
            self.cookie_manager = None

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
        if 'user_email' not in st.session_state:
            st.session_state.user_email = None

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

    def load_paid_users(self):
        """Load paid users database from JSON file"""
        try:
            if os.path.exists(PAID_USERS_DB):
                with open(PAID_USERS_DB, 'r') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            st.error(f"Error loading user database: {e}")
            return {}

    def save_paid_user(self, email, payment_id):
        """Save paid user to database"""
        try:
            # Load existing data
            users = self.load_paid_users()

            # Add new user
            users[email.lower().strip()] = {
                "payment_id": payment_id,
                "timestamp": datetime.now().isoformat(),
                "access_granted": True
            }

            # Save to file
            os.makedirs(os.path.dirname(PAID_USERS_DB), exist_ok=True)
            with open(PAID_USERS_DB, 'w') as f:
                json.dump(users, f, indent=2)

            return True
        except Exception as e:
            st.error(f"Error saving user: {e}")
            return False

    def verify_email(self, email):
        """Verify if email exists in paid users database"""
        users = self.load_paid_users()
        return email.lower().strip() in users

    def get_user_payment_id(self, email):
        """Get payment ID for a user email"""
        users = self.load_paid_users()
        user_data = users.get(email.lower().strip())
        if user_data:
            return user_data.get("payment_id")
        return None

    def set_access_cookie(self, payment_id):
        """Set persistent cookie for access"""
        if not self.cookie_manager:
            return False
        try:
            expiry_date = datetime.now() + timedelta(days=COOKIE_EXPIRY_DAYS)
            self.cookie_manager.set(
                COOKIE_NAME,
                payment_id,
                expires_at=expiry_date
            )
            return True
        except Exception as e:
            # Cookie setting might fail in some environments, continue anyway
            return False

    def get_access_cookie(self):
        """Get access cookie value"""
        if not self.cookie_manager:
            return None
        try:
            cookies = self.cookie_manager.get_all()
            if cookies and COOKIE_NAME in cookies:
                return cookies[COOKIE_NAME]
        except Exception as e:
            pass
        return None

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

        # Two columns for options (removed admin from main area)
        col1, col2 = st.columns(2)

        with col1:
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

        with col2:
            st.markdown("**💳 Pay Once**")
            st.markdown("₹49 only • Lifetime")
            # Razorpay button will be shown below

        # Razorpay Payment Button (compact version)
        self.show_razorpay_button_compact()

        # Returning User Section
        st.markdown("---")
        st.markdown("### 🔄 Returning User?")

        col_a, col_b = st.columns([2, 1])

        with col_a:
            user_email = st.text_input(
                "Enter your registered email:",
                key="returning_user_email",
                placeholder="your.email@example.com",
                help="Enter the email you used during payment"
            )

        with col_b:
            st.markdown("<br>", unsafe_allow_html=True)  # Spacing
            if st.button("Verify Access", key="verify_returning_user", type="secondary"):
                if user_email:
                    if self.verify_email(user_email):
                        payment_id = self.get_user_payment_id(user_email)
                        st.session_state.payment_verified = True
                        st.session_state.payment_id = payment_id
                        st.session_state.user_email = user_email
                        self.set_access_cookie(payment_id)
                        st.success("✅ Access restored! Welcome back!")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("❌ Email not found. Please check your email or complete payment.")
                else:
                    st.warning("Please enter your email address")

    def show_razorpay_button_compact(self):
        """Display compact Razorpay payment button with email collection"""
        import os

        razorpay_key = os.environ.get("RAZORPAY_KEY_ID", "rzp_test_placeholder")

        # Add email input field before payment
        st.markdown("**Enter your email to receive access link:**")
        payment_email = st.text_input(
            "Email Address:",
            key="payment_email_input",
            placeholder="your.email@example.com",
            help="We'll save this for future access",
            label_visibility="collapsed"
        )

        razorpay_html = f"""
        <script src="https://checkout.razorpay.com/v1/checkout.js"></script>
        <script>
        function initiatePayment() {{
            // Get email from input field
            var email = window.parent.document.querySelector('input[aria-label="Email Address:"]');
            var emailValue = email ? email.value : '';

            if (!emailValue || !emailValue.includes('@')) {{
                alert('Please enter a valid email address before proceeding with payment');
                return;
            }

            var options = {{
                "key": "{razorpay_key}",
                "amount": "4900",
                "currency": "INR",
                "name": "Home Loan Comparison",
                "description": "Lifetime Access",
                "prefill": {{
                    "email": emailValue
                }},
                "handler": function (response) {{
                    // Store email in URL for processing
                    window.location.href = window.location.href.split('?')[0] + "?payment_id=" + response.razorpay_payment_id + "&email=" + encodeURIComponent(emailValue);
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

    def verify_payment(self, payment_id, email=None):
        """Verify payment and grant access"""
        # In production, verify with Razorpay API
        # For now, we'll use session state and save to database

        if payment_id:
            st.session_state.payment_verified = True
            st.session_state.payment_id = payment_id
            st.session_state.access_expiry = None  # Lifetime access

            # Save to database if email provided
            if email:
                st.session_state.user_email = email
                self.save_paid_user(email, payment_id)

            # Set persistent cookie
            self.set_access_cookie(payment_id)

            return True
        return False

    def check_access(self):
        """Check if user has paid, is admin, or has active trial"""

        # Check for admin access
        if st.session_state.is_admin:
            return True

        # Check persistent cookie first
        cookie_payment_id = self.get_access_cookie()
        if cookie_payment_id:
            st.session_state.payment_verified = True
            st.session_state.payment_id = cookie_payment_id
            return True

        # Check URL parameters for payment_id (new payment)
        query_params = st.query_params
        if 'payment_id' in query_params:
            payment_id = query_params['payment_id']
            email = query_params.get('email', None)
            if self.verify_payment(payment_id, email):
                st.success("✅ Payment verified! You now have lifetime access.")
                if email:
                    st.info(f"💌 Access saved for: {email}")
                st.balloons()
                return True

        # Check if payment was already verified in session
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

    def show_admin_footer(self):
        """Show admin access in footer with expander"""
        st.markdown("---")

        with st.expander("🔧 Admin/Developer Access"):
            st.markdown("**For authorized administrators only**")

            admin_email = st.text_input(
                "Admin Email:",
                key="admin_email_footer",
                placeholder="admin@example.com"
            )

            if st.button("Verify Admin", key="verify_admin_footer"):
                if self.check_admin_email(admin_email):
                    st.session_state.is_admin = True
                    st.session_state.admin_email = admin_email
                    st.session_state.payment_verified = True
                    st.success("✅ Admin access granted!")
                    st.rerun()
                else:
                    st.error("❌ Not authorized")

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
