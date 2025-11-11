import logging


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
