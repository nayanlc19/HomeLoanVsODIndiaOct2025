"""
Rate Loader - Load bank interest rates from JSON file with fallback to defaults
"""
import json
import os
from datetime import datetime

# Fallback default rates if JSON file not available or fails to load
DEFAULT_RATES = {
    "last_updated": "2025-10-14",
    "rates": {
        "regular_loans": {
            "HDFC Bank": {"base_rate": 8.60, "range": "8.40-8.80", "processing_fee": 0.50, "min_processing": 3000, "prepayment_charge": 0.0},
            "ICICI Bank": {"base_rate": 8.75, "range": "8.60-8.90", "processing_fee": 0.50, "min_processing": 3500, "prepayment_charge": 0.0},
            "SBI": {"base_rate": 8.50, "range": "8.35-8.65", "processing_fee": 0.00, "min_processing": 0, "prepayment_charge": 0.0},
            "Axis Bank": {"base_rate": 8.75, "range": "8.60-8.90", "processing_fee": 1.00, "min_processing": 10000, "prepayment_charge": 0.0},
            "Bank of Baroda": {"base_rate": 8.40, "range": "8.25-8.55", "processing_fee": 0.50, "min_processing": 7500, "prepayment_charge": 0.0},
            "PNB": {"base_rate": 8.55, "range": "8.40-8.70", "processing_fee": 0.50, "min_processing": 5000, "prepayment_charge": 0.0}
        },
        "od_loans": {
            "SBI MaxGain": {"base_rate": 8.75, "range": "8.60-9.05", "processing_fee": 0.00, "min_processing": 0, "od_charge": 10000, "min_loan": 2000000},
            "ICICI Home Overdraft": {"base_rate": 9.00, "range": "8.85-9.15", "processing_fee": 0.50, "min_processing": 3500, "od_charge": 0, "min_loan": 2500000},
            "HDFC Overdraft": {"base_rate": 8.85, "range": "8.70-9.00", "processing_fee": 0.50, "min_processing": 3000, "od_charge": 5000, "min_loan": 2000000},
            "BoB Home Advantage": {"base_rate": 8.65, "range": "8.50-8.80", "processing_fee": 0.50, "min_processing": 7500, "od_charge": 5000, "min_loan": 1500000}
        }
    }
}


def load_bank_rates(json_path=None):
    """
    Load bank interest rates from JSON file or use defaults

    Args:
        json_path (str, optional): Path to JSON file. If None, looks in app/data/bank_rates.json

    Returns:
        dict: Bank rates data with structure matching DEFAULT_RATES
    """

    if json_path is None:
        # Try to find the JSON file relative to this script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(script_dir, '..', 'data', 'bank_rates.json')

    try:
        # Try to load from JSON file
        if os.path.exists(json_path):
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Validate structure
            if 'rates' in data and 'regular_loans' in data['rates'] and 'od_loans' in data['rates']:
                return data
            else:
                print(f"Warning: Invalid JSON structure in {json_path}, using defaults")
                return DEFAULT_RATES
        else:
            print(f"Info: Bank rates JSON not found at {json_path}, using defaults")
            return DEFAULT_RATES

    except Exception as e:
        print(f"Error loading bank rates from {json_path}: {e}. Using defaults.")
        return DEFAULT_RATES


def get_bank_data_for_app(use_personalized=False, user_profile=None):
    """
    Get bank data in the format expected by the main app

    Args:
        use_personalized (bool): Whether to apply personalized rate adjustments
        user_profile (dict, optional): User profile for personalized rates

    Returns:
        dict: Bank data in BANK_DATA format for the app
    """

    rates_data = load_bank_rates()

    # Convert to app format
    bank_data = {
        "Regular Home Loan (EMI)": {},
        "Home Loan with Overdraft": {}
    }

    # Process regular loans
    for bank_name, rate_info in rates_data['rates']['regular_loans'].items():
        base_rate = rate_info['base_rate']

        # Apply personalization if requested
        if use_personalized and user_profile:
            from .rate_calculator import calculate_personalized_rate
            result = calculate_personalized_rate(base_rate, user_profile)
            final_rate = result['final_rate']
        else:
            final_rate = base_rate

        bank_data["Regular Home Loan (EMI)"][bank_name] = {
            "interest_rate": final_rate,
            "base_rate": base_rate,
            "processing_fee": rate_info.get('processing_fee', 0.50),
            "min_processing": rate_info.get('min_processing', 3000),
            "prepayment_charge": rate_info.get('prepayment_charge', 0.0)
        }

    # Process OD loans
    for bank_name, rate_info in rates_data['rates']['od_loans'].items():
        base_rate = rate_info['base_rate']

        # Apply personalization if requested
        if use_personalized and user_profile:
            from .rate_calculator import calculate_personalized_rate
            result = calculate_personalized_rate(base_rate, user_profile)
            final_rate = result['final_rate']
        else:
            final_rate = base_rate

        bank_data["Home Loan with Overdraft"][bank_name] = {
            "interest_rate": final_rate,
            "base_rate": base_rate,
            "processing_fee": rate_info.get('processing_fee', 0.50),
            "min_processing": rate_info.get('min_processing', 3000),
            "od_charge": rate_info.get('od_charge', 5000),
            "min_loan": rate_info.get('min_loan', 2000000)
        }

    return bank_data, rates_data.get('last_updated', 'Unknown')


def get_days_since_update(last_updated_str):
    """
    Calculate days since rates were last updated

    Args:
        last_updated_str (str): Date string in format "YYYY-MM-DD"

    Returns:
        int: Number of days since update
    """

    try:
        last_updated = datetime.strptime(last_updated_str, "%Y-%m-%d")
        days_diff = (datetime.now() - last_updated).days
        return days_diff
    except:
        return -1


def get_update_status_message(last_updated_str):
    """
    Get a user-friendly message about when rates were last updated

    Args:
        last_updated_str (str): Date string in format "YYYY-MM-DD"

    Returns:
        tuple: (message, color) where color is 'green', 'orange', or 'red'
    """

    days = get_days_since_update(last_updated_str)

    if days == -1:
        return ("Rates update status unknown", "gray")
    elif days == 0:
        return ("Rates updated today", "green")
    elif days == 1:
        return ("Rates updated yesterday", "green")
    elif days <= 7:
        return (f"Rates updated {days} days ago", "green")
    elif days <= 14:
        return (f"Rates updated {days} days ago (consider checking bank websites)", "orange")
    else:
        return (f"Rates updated {days} days ago (please verify with banks)", "red")
