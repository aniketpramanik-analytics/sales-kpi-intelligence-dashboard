def format_currency(value: float) -> str:
    return f"${value:,.2f}"

def format_percentage(value: float) -> str:
    return f"{value:+.1f}%"

def format_number(value: float) -> str:
    return f"{value:,.0f}"