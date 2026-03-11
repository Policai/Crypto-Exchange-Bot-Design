import random
import string


def generate_telegram_code() -> str:
    return "".join(random.choices(string.digits, k=6))


def unique_comment() -> str:
    return "".join(random.choices(string.digits, k=6))
