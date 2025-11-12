import logging
from datetime import datetime

def cleanup_text(text: str) -> str:
    return (text
            .replace("\n", "")
            .replace("\t", "")
            .strip(" ")
            .strip("(")
            .strip(")")
            .lower())


def safe_int(value: str, default: int = 0) -> int:
    try:
        return int(value)
    except (ValueError, TypeError):
        logging.warning(
            f"Could not convert value '{value}' to int. (safe_int)")
        return default
    
def convert_date_format(date_str: str, year: int) -> str:
    """Convert date string from 'Jan 1' format to 'YYYY-MM-DD' format."""
    try:
        # Parse the date string with the year appended
        date_obj = datetime.strptime(f"{date_str} {year}", "%b %d %Y")
        return date_obj.strftime("%Y-%m-%d")
    except ValueError:
        return "N/A"
