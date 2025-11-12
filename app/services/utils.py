from typing import Tuple
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
    

def convert_date_range_format(date_str: str, year: int) -> Tuple[str, str]:
    """Convert date range string from 'MMM D-MMM D' OR 'MMM D-D' OR 'MMM D' format to 'YYYY-MM-DD' format as a range."""
    if "—" in date_str:
        date_parts = date_str.split("—")
    elif "-" in date_str:
        date_parts = date_str.split("-")
    else:
        single_date = datetime.strptime(f"{date_str.strip()} {year}", "%b %d %Y")
        formatted_date = single_date.strftime("%Y-%m-%d")
        return formatted_date, formatted_date
    
    if len(date_parts) != 2:
        return "N/A", "N/A"
    
    start_str = date_parts[0].strip()
    end_str = date_parts[1].strip()

    if len(end_str) <= 2:  # Only day is provided in end date
        start_month = start_str.split(" ")[0]
        end_str = f"{start_month} {end_str}"

    start_date = datetime.strptime(f"{start_str} {year}", "%b %d %Y")
    end_date = datetime.strptime(f"{end_str} {year}", "%b %d %Y")
        
    return start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")
