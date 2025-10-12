# ⚡ Quick Start Guide (2 Minutes)

## 🚀 Get Started in 3 Steps

### Step 1: Install (30 seconds)

```bash
cd D:/Claude/home_loan_comparison_tool
pip install -r requirements.txt
```

### Step 2: Run (10 seconds)

```bash
streamlit run app/home_loan_comparison_app.py
```

### Step 3: Use (80 seconds)

Browser opens automatically at http://localhost:8501

**In the left sidebar, enter:**

1. **Loan Amount**: Your home loan amount (e.g., ₹50,00,000)
2. **Tenure**: How many years (e.g., 20 years)
3. **Tax Slab**: Your income tax rate (e.g., 30%)
4. **Tax Regime**: Old (if you use 80C) or New
5. **Property Type**: Self-Occupied or Let-Out

**Optional (but recommended):**

6. **Annual Prepayment**: Bonus amount you'll prepay yearly (e.g., ₹1,00,000)
7. **Overdraft Surplus**: Amount you can park initially (e.g., ₹5,00,000)
8. **Monthly Surplus**: Extra savings per month (e.g., ₹20,000)

**That's it!**

The app will show:
- ✅ Which option is cheaper (Regular Loan vs Overdraft)
- ✅ How much you'll save (in lakhs!)
- ✅ Hidden problems to watch out for
- ✅ Smart tips to save even more

---

## 🎯 Example Scenario

**Your Situation:**
- Need ₹50L loan for 20 years
- Annual bonus: ₹1L (can prepay)
- Current savings: ₹10L (can park in OD)
- Monthly surplus: ₹25K

**Input in App:**
- Loan Amount: 5000000
- Tenure: 20 years
- Annual Prepayment: 100000
- Overdraft Surplus: 1000000
- Monthly Surplus: 25000

**Result:**
- Regular Loan: ₹54L interest
- Overdraft: ₹32L interest
- **You save: ₹22 Lakhs!** 🎉

---

## 🆘 Troubleshooting

**App won't start?**
```bash
pip install streamlit pandas plotly numpy
```

**Port already in use?**
```bash
streamlit run app/home_loan_comparison_app.py --server.port 8502
```

**Need help?**
- Read tooltips in the app (hover over ℹ️ icons)
- Check full README.md for detailed guide
- Review the "Tips & Tricks" section in the app

---

## 📖 Want More Details?

See **README.md** for:
- Complete installation guide
- How overdraft really works
- When to choose what
- Tax optimization strategies
- Common mistakes to avoid
- Hidden charges to watch for

---

**Ready? Let's save you some lakhs! 💪💰**
