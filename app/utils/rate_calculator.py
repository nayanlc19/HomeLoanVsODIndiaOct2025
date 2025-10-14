"""
Rate Calculator - Calculate personalized interest rates based on user profile
"""

def calculate_personalized_rate(base_rate, user_profile):
    """
    Calculate personalized interest rate based on user profile factors

    Args:
        base_rate (float): Base interest rate from bank
        user_profile (dict): User profile with keys:
            - credit_score: str ('750+', '700-749', '650-699', '<650')
            - age: int (23-62)
            - gender: str ('Male', 'Female', 'Other')
            - employment: str ('Salaried-Govt', 'Salaried-MNC', 'Salaried-Other', 'Self-Employed')
            - loan_amount: float (in ₹)
            - property_location: str ('Metro Tier-1', 'Tier-2', 'Tier-3')

    Returns:
        dict: {
            'final_rate': float,
            'adjustments': dict (breakdown of each adjustment),
            'total_adjustment': float
        }
    """

    adjustments = {}

    # 1. Credit Score Adjustment
    credit_score = user_profile.get('credit_score', '750+')
    if credit_score == '750+':
        adjustments['credit_score'] = -0.25
    elif credit_score == '700-749':
        adjustments['credit_score'] = 0.0
    elif credit_score == '650-699':
        adjustments['credit_score'] = 0.35
    else:  # <650
        adjustments['credit_score'] = 0.75

    # 2. Age Adjustment
    age = user_profile.get('age', 35)
    if 25 <= age <= 35:
        adjustments['age'] = -0.10
    elif 36 <= age <= 45:
        adjustments['age'] = 0.0
    elif 46 <= age <= 55:
        adjustments['age'] = 0.10
    else:  # 56-62
        adjustments['age'] = 0.20

    # 3. Gender Adjustment (Women get concession)
    gender = user_profile.get('gender', 'Male')
    if gender == 'Female':
        adjustments['gender'] = -0.05
    else:
        adjustments['gender'] = 0.0

    # 4. Employment Type Adjustment
    employment = user_profile.get('employment', 'Salaried-Other')
    if employment == 'Salaried-Govt':
        adjustments['employment'] = -0.15
    elif employment == 'Salaried-MNC':
        adjustments['employment'] = -0.10
    elif employment == 'Salaried-Other':
        adjustments['employment'] = 0.0
    else:  # Self-Employed
        adjustments['employment'] = 0.25

    # 5. Loan Amount Adjustment
    loan_amount = user_profile.get('loan_amount', 5000000)
    if loan_amount >= 7500000:  # ≥75L
        adjustments['loan_amount'] = -0.10
    elif loan_amount <= 2000000:  # ≤20L
        adjustments['loan_amount'] = 0.15
    else:
        adjustments['loan_amount'] = 0.0

    # 6. Property Location Adjustment
    location = user_profile.get('property_location', 'Metro Tier-1')
    if location == 'Metro Tier-1':
        adjustments['location'] = 0.0
    elif location == 'Tier-2':
        adjustments['location'] = 0.10
    else:  # Tier-3
        adjustments['location'] = 0.15

    # Calculate final rate
    total_adjustment = sum(adjustments.values())
    final_rate = base_rate + total_adjustment

    # Ensure rate doesn't go below 7.0% or above 15.0%
    final_rate = max(7.0, min(15.0, final_rate))

    return {
        'final_rate': round(final_rate, 2),
        'adjustments': adjustments,
        'total_adjustment': round(total_adjustment, 2)
    }


def get_adjustment_description(adjustment_key, adjustment_value, user_profile):
    """
    Get human-readable description for each adjustment

    Args:
        adjustment_key (str): Key like 'credit_score', 'age', etc.
        adjustment_value (float): Adjustment value
        user_profile (dict): User profile data

    Returns:
        str: Human-readable description
    """

    if adjustment_key == 'credit_score':
        score = user_profile.get('credit_score', '750+')
        if adjustment_value < 0:
            return f"Excellent credit score ({score})"
        elif adjustment_value == 0:
            return f"Good credit score ({score})"
        else:
            return f"Lower credit score ({score})"

    elif adjustment_key == 'age':
        age = user_profile.get('age', 35)
        if adjustment_value < 0:
            return f"Young applicant (Age {age})"
        elif adjustment_value == 0:
            return f"Mid-age applicant (Age {age})"
        else:
            return f"Senior applicant (Age {age})"

    elif adjustment_key == 'gender':
        gender = user_profile.get('gender', 'Male')
        if adjustment_value < 0:
            return f"Women borrower concession"
        else:
            return f"Gender: {gender}"

    elif adjustment_key == 'employment':
        emp = user_profile.get('employment', 'Salaried-Other')
        return f"Employment: {emp}"

    elif adjustment_key == 'loan_amount':
        amount = user_profile.get('loan_amount', 5000000)
        if adjustment_value < 0:
            return f"High loan amount (₹{amount/100000:.0f}L+)"
        elif adjustment_value > 0:
            return f"Lower loan amount (₹{amount/100000:.0f}L)"
        else:
            return f"Standard loan amount (₹{amount/100000:.0f}L)"

    elif adjustment_key == 'location':
        loc = user_profile.get('property_location', 'Metro Tier-1')
        return f"Property Location: {loc}"

    return ""


def get_profile_impact_summary(adjustments, user_profile):
    """
    Generate a formatted summary of how user profile affects rates

    Args:
        adjustments (dict): Adjustment breakdown
        user_profile (dict): User profile data

    Returns:
        list: List of tuples (description, adjustment_value, emoji)
    """

    summary = []

    for key, value in adjustments.items():
        if value == 0:
            continue  # Skip neutral adjustments

        description = get_adjustment_description(key, value, user_profile)

        if value < 0:
            emoji = "✅"
        else:
            emoji = "⚠️"

        summary.append((description, value, emoji))

    return summary
