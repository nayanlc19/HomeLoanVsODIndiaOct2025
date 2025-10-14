# Deploy Home Loan App with Razorpay on Render

This guide will help you deploy your Streamlit app with Razorpay payment integration on Render.

## Prerequisites

1. **Razorpay Account**
   - Sign up at https://razorpay.com/
   - Get your API keys from https://dashboard.razorpay.com/app/keys
   - You'll get:
     - Test Key: `rzp_test_...` (for testing)
     - Live Key: `rzp_live_...` (for production)

2. **GitHub Account**
   - Your code should be pushed to GitHub

3. **Render Account**
   - Sign up at https://render.com/

## Step 1: Setup Razorpay

1. Go to https://dashboard.razorpay.com/
2. Navigate to **Settings** > **API Keys**
3. Copy your `Key ID` and `Key Secret`
4. For testing, use **Test Mode** keys
5. For production, generate **Live Mode** keys (requires KYC verification)

### Important: Razorpay KYC for Live Keys
- Test keys work immediately for testing
- Live keys require business verification (PAN, GST, bank details)
- Takes 1-2 business days for approval

## Step 2: Deploy on Render

### Method 1: One-Click Deploy (Easiest)

1. Fork or push this repository to your GitHub
2. Go to https://render.com/
3. Click **New** > **Web Service**
4. Connect your GitHub repository
5. Render will auto-detect the `render.yaml` configuration
6. Click **Create Web Service**

### Method 2: Manual Setup

1. Go to https://dashboard.render.com/
2. Click **New** > **Web Service**
3. Connect your GitHub repository: `https://github.com/nayanlc19/HomeLoanVsODIndiaOct2025`
4. Configure:
   - **Name**: `home-loan-comparison`
   - **Region**: Singapore (or your preferred)
   - **Branch**: `master`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run app/home_loan_with_payment.py --server.port $PORT --server.address 0.0.0.0`
   - **Plan**: Free (or paid for better performance)

## Step 3: Add Environment Variables in Render

1. In Render dashboard, go to your web service
2. Click **Environment** tab
3. Add these environment variables:

```
RAZORPAY_KEY_ID = rzp_test_YOUR_KEY_HERE
RAZORPAY_KEY_SECRET = YOUR_SECRET_HERE
```

4. Click **Save Changes**
5. Your app will automatically redeploy

## Step 4: Test Payment Flow

1. Open your Render app URL (e.g., `https://home-loan-comparison.onrender.com`)
2. You should see the payment wall
3. Click "Pay ₹49"
4. Use Razorpay test cards:
   - **Card Number**: `4111 1111 1111 1111`
   - **CVV**: Any 3 digits (e.g., `123`)
   - **Expiry**: Any future date (e.g., `12/25`)
   - **Name**: Any name

5. Complete the payment
6. You should get access to the full app

## Step 5: Go Live (Production)

When ready to accept real payments:

1. Complete Razorpay KYC verification
2. Get your Live API keys
3. Update environment variables in Render:
   ```
   RAZORPAY_KEY_ID = rzp_live_YOUR_LIVE_KEY
   RAZORPAY_KEY_SECRET = YOUR_LIVE_SECRET
   ```
4. Test with real payment (you can refund yourself)
5. Launch!

## Pricing

### Render Pricing
- **Free Plan**: Good for testing, app sleeps after 15 min inactivity
- **Starter Plan** ($7/month): Always on, better performance
- **Standard Plan** ($25/month): Production-ready

### Razorpay Pricing
- **Setup**: Free
- **Transaction Fee**: 2% per successful transaction
- **For ₹49 payment**: You get ₹48.02 (₹0.98 fee)

## Troubleshooting

### App Not Loading
- Check Render logs: Dashboard > Logs
- Verify Python version (should be 3.11+)
- Check if all dependencies installed

### Payment Not Working
- Verify Razorpay keys in environment variables
- Check browser console for errors
- Ensure you're using correct test/live keys

### App Sleeps on Free Plan
- Upgrade to Starter plan ($7/month)
- Or use a service like UptimeRobot to ping every 14 minutes

## Custom Domain (Optional)

1. Buy a domain (e.g., from Namecheap, GoDaddy)
2. In Render dashboard, go to **Settings** > **Custom Domain**
3. Add your domain
4. Update DNS records as per Render's instructions
5. Enable HTTPS (automatic with Render)

## Monitoring & Analytics

Add Google Analytics to track:
- Page views
- Payment conversions
- User behavior

Add in your Streamlit app:
```python
st.components.v1.html("""
<!-- Google Analytics code -->
""")
```

## Support

- **Razorpay Support**: https://razorpay.com/support/
- **Render Docs**: https://render.com/docs
- **Issues**: Open an issue on GitHub

## Security Notes

1. Never commit `.streamlit/secrets.toml` to Git
2. Always use environment variables for API keys
3. Enable HTTPS (Render does this automatically)
4. Regularly rotate your Razorpay secrets

---

**Ready to Deploy?** Follow the steps above and you'll have your app live in 10 minutes!
