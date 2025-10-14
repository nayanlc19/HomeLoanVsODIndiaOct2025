"""
Number Formatter - Format large numbers with Indian notation and approximations
"""

def format_indian_number(amount, decimals=0):
    """
    Format number in Indian notation with commas

    Args:
        amount: Number to format
        decimals: Number of decimal places

    Returns:
        str: Formatted number like ₹15,00,000
    """
    if amount < 0:
        return f"-₹{format_indian_number(abs(amount), decimals)}"

    # Convert to string and split into integer and decimal parts
    if decimals > 0:
        amount_str = f"{amount:.{decimals}f}"
    else:
        amount_str = f"{int(amount)}"

    # Split integer and decimal parts
    if '.' in amount_str:
        integer_part, decimal_part = amount_str.split('.')
    else:
        integer_part = amount_str
        decimal_part = None

    # Apply Indian comma notation
    if len(integer_part) <= 3:
        formatted = integer_part
    else:
        # Last 3 digits
        last_three = integer_part[-3:]
        remaining = integer_part[:-3]

        # Add commas every 2 digits for the remaining part
        groups = []
        while remaining:
            if len(remaining) <= 2:
                groups.append(remaining)
                break
            groups.append(remaining[-2:])
            remaining = remaining[:-2]

        groups.reverse()
        formatted = ','.join(groups) + ',' + last_three

    # Add decimal part if exists
    if decimal_part:
        formatted += '.' + decimal_part

    return f"₹{formatted}"


def get_approximation(amount):
    """
    Get short approximation for large numbers

    Args:
        amount: Number to approximate

    Returns:
        str: Approximation like "~1.5 Cr", "~15 L", "~5 K"
    """
    abs_amount = abs(amount)

    if abs_amount >= 10000000:  # >= 1 Crore
        crores = abs_amount / 10000000
        if crores >= 10:
            return f"~{crores:.0f} Cr"
        else:
            return f"~{crores:.1f} Cr"
    elif abs_amount >= 100000:  # >= 1 Lakh
        lakhs = abs_amount / 100000
        if lakhs >= 10:
            return f"~{lakhs:.0f} L"
        else:
            return f"~{lakhs:.1f} L"
    elif abs_amount >= 1000:  # >= 1 Thousand
        thousands = abs_amount / 1000
        if thousands >= 10:
            return f"~{thousands:.0f} K"
        else:
            return f"~{thousands:.1f} K"
    else:
        return f"₹{abs_amount:.0f}"


def format_with_approximation(amount, decimals=0):
    """
    Format number with both full value and approximation

    Args:
        amount: Number to format
        decimals: Decimal places for full value

    Returns:
        str: Formatted like "₹15,00,823 (~1.5 Cr)" or "₹1,45,000 (~1.5 L)"
    """
    formatted_full = format_indian_number(amount, decimals)

    abs_amount = abs(amount)

    # Only show approximation for amounts >= 100,000 (1 Lakh)
    if abs_amount >= 100000:
        approx = get_approximation(amount)
        return f"{formatted_full} ({approx})"
    else:
        return formatted_full


def format_currency_compact(amount):
    """
    Compact format for small spaces - just the approximation

    Args:
        amount: Number to format

    Returns:
        str: Compact format like "₹1.5 Cr", "₹15 L"
    """
    abs_amount = abs(amount)
    sign = "-" if amount < 0 else ""

    if abs_amount >= 10000000:  # >= 1 Crore
        crores = abs_amount / 10000000
        if crores >= 10:
            return f"{sign}₹{crores:.0f} Cr"
        else:
            return f"{sign}₹{crores:.1f} Cr"
    elif abs_amount >= 100000:  # >= 1 Lakh
        lakhs = abs_amount / 100000
        if lakhs >= 10:
            return f"{sign}₹{lakhs:.0f} L"
        else:
            return f"{sign}₹{lakhs:.1f} L"
    elif abs_amount >= 1000:  # >= 1 Thousand
        thousands = abs_amount / 1000
        if thousands >= 10:
            return f"{sign}₹{thousands:.0f} K"
        else:
            return f"{sign}₹{thousands:.1f} K"
    else:
        return f"{sign}₹{abs_amount:,.0f}"
